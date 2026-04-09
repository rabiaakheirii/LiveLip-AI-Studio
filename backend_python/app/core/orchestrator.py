from __future__ import annotations

import asyncio
import logging
import shutil
import time
from pathlib import Path
from typing import Any

import httpx
from fastapi import WebSocket

from app.core.config import Settings
from app.core.events import EventMessage, EventType, PipelineState
from app.core.state_machine import PipelineStateMachine
from app.core.storage_paths import StoragePaths
from app.core.stream_pipeline import StreamPipeline
from app.models.diagnostics import CapabilityStatus, DiagnosticsSummary
from app.models.stream_metrics import StreamMetrics
from app.models.webcam import CameraDevice, PreviewChunk
from app.services.lipsync_service import LipSyncService
from app.services.obs_service import OBSService
from app.services.ollama_service import OllamaService
from app.services.remote_worker_client import RemoteWorkerClient
from app.services.render_queue_service import RenderQueueService
from app.services.stt_service import STTService
from app.services.tts_service import TTSService
from app.services.webcam_service import WebcamService
from app.workers.worker_modes import resolve_worker_mode

logger = logging.getLogger(__name__)

_EVENT_MAP = {e.value: e for e in EventType}


class EventBus:
    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections.discard(websocket)

    async def broadcast(self, message: EventMessage) -> None:
        stale: list[WebSocket] = []
        payload = message.model_dump(mode="json")
        for ws in self._connections:
            try:
                await ws.send_json(payload)
            except Exception:
                stale.append(ws)
        for ws in stale:
            self.disconnect(ws)


class PipelineOrchestrator:
    def __init__(self, settings: Settings, event_bus: EventBus):
        self.settings = settings
        self._event_bus = event_bus
        self._sm = PipelineStateMachine()
        self._task: asyncio.Task | None = None
        self._timings: dict[str, float] = {}
        self._paths = StoragePaths(settings.output_dir)

        self.stt_service = STTService()
        self.ollama_service = OllamaService(settings.ollama_base_url, settings.ollama_model)
        self.tts_service = TTSService(str(self._paths.audio), settings.tts_voice)
        self.webcam_service = WebcamService(self._paths.frames, max_devices=settings.webcam_max_devices)
        self.lipsync_service = LipSyncService(
            self._paths.preview,
            engine_name=settings.lipsync_engine,
            experimental_enabled=settings.enable_experimental_engines,
            model_assets_dir=settings.lipsync_model_assets_dir,
        )
        self.render_queue = RenderQueueService(max_history=25)
        self.obs_service = OBSService(
            host=settings.obs_host,
            port=settings.obs_port,
            password=settings.obs_password,
            default_scene=settings.obs_scene,
            audio_source=settings.obs_audio_source,
            video_source=settings.obs_video_source,
        )
        self.remote_worker = RemoteWorkerClient(settings.remote_worker_base_url)
        self.worker_mode_status = resolve_worker_mode(settings.worker_mode, settings.remote_worker_base_url)

        self.stream_pipeline = StreamPipeline(
            webcam_service=self.webcam_service,
            lipsync_service=self.lipsync_service,
            obs_service=self.obs_service,
            event_cb=self._emit_by_name,
            output_dir=self._paths.preview,
            target_fps=settings.stream_target_fps,
            frame_queue_size=settings.stream_frame_queue_size,
            audio_queue_size=settings.stream_audio_queue_size,
            obs_video_mode=settings.obs_video_mode,
            frame_skip_policy=settings.frame_skip_policy,
            adaptive_degraded_mode=settings.adaptive_degraded_mode,
        )

    @property
    def state(self) -> PipelineState:
        return self._sm.state

    @property
    def is_running(self) -> bool:
        return self._task is not None and not self._task.done()

    @property
    def timings(self) -> dict[str, float]:
        return self._timings

    @property
    def preview_dir(self) -> Path:
        return self._paths.preview

    def latest_preview(self) -> PreviewChunk | None:
        return self.render_queue.latest()

    def preview_history(self) -> list[PreviewChunk]:
        return self.render_queue.history()

    def list_cameras(self) -> list[CameraDevice]:
        return self.webcam_service.list_cameras()

    def select_camera(self, index: int) -> CameraDevice:
        return self.webcam_service.select_camera(index)

    def stream_status(self) -> StreamMetrics:
        return self.stream_pipeline.status()

    def performance_metrics(self):
        return self.stream_pipeline.performance_metrics()

    def stream_latest_frame(self) -> bytes | None:
        return self.stream_pipeline.latest_frame()

    async def stream_mjpeg(self):
        async for chunk in self.stream_pipeline.mjpeg_generator():
            yield chunk

    async def _ollama_reachable(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=2) as client:
                r = await client.get(f"{self.settings.ollama_base_url.rstrip('/')}/api/tags")
                return r.status_code < 500
        except Exception:
            return False

    def _obs_reachable(self) -> bool:
        return self.obs_service.is_connected

    async def get_diagnostics_summary(self) -> DiagnosticsSummary:
        cams = self.list_cameras()
        remote_health = await self.remote_worker.health() if self.worker_mode_status.mode == "remote" else {"available": False}
        stream = self.stream_pipeline.status()
        return DiagnosticsSummary(
            app_name=self.settings.app_name,
            environment=self.settings.environment,
            log_level=self.settings.log_level,
            stream_running=self.stream_pipeline.running,
            stream_message=stream.message,
            worker_mode=self.worker_mode_status.mode,
            capability=CapabilityStatus(
                webcam_available=any(c.available for c in cams),
                ffmpeg_available=shutil.which("ffmpeg") is not None,
                ollama_reachable=await self._ollama_reachable(),
                obs_reachable=self._obs_reachable(),
                selected_lipsync_engine=self.lipsync_service.engine_name,
                degraded_mode=self.lipsync_service.degraded_mode,
                engine_capabilities=self.lipsync_service.capabilities(),
                remote_worker_available=remote_health.get("available", False),
            ),
        )

    async def start_stream(self) -> None:
        await self._transition(PipelineState.stream_initializing)
        await self.stream_pipeline.start()
        await self._transition(PipelineState.streaming_live)

    async def stop_stream(self) -> None:
        await self.stream_pipeline.stop()
        if self.state != PipelineState.idle:
            self._sm = PipelineStateMachine()
            await self._emit(EventType.pipeline_state, {"state": self.state.value})

    async def publish_camera_list(self) -> None:
        cameras = [c.model_dump(mode="json") for c in self.list_cameras()]
        await self._emit(EventType.camera_list, {"cameras": cameras, "selected_index": self.webcam_service.selected_index})

    async def publish_camera_selected(self, camera: CameraDevice) -> None:
        await self._emit(EventType.camera_selected, camera.model_dump(mode="json"))

    async def _emit_by_name(self, event_name: str, data: dict) -> None:
        event = _EVENT_MAP.get(event_name)
        if event:
            await self._emit(event, data)

    async def _emit(self, event_type: EventType, data: dict[str, Any]) -> None:
        await self._event_bus.broadcast(EventMessage(event_type=event_type, data=data))

    async def _transition(self, next_state: PipelineState) -> None:
        if self._sm.can_transition(next_state):
            prev = self.state
            self._sm.transition(next_state)
            logger.info("state_transition %s -> %s", prev.value, self.state.value)
            await self._emit(EventType.pipeline_state, {"state": self.state.value})

    async def start(self) -> None:
        self._task = asyncio.create_task(self._run_once(), name="pipeline-run")

    async def stop(self) -> None:
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._task = None
        await self.stop_stream()
        self._sm = PipelineStateMachine()
        await self._emit(EventType.pipeline_state, {"state": self.state.value})

    async def _run_once(self) -> None:
        cycle_start = time.perf_counter()
        try:
            await self._transition(PipelineState.listening)
            obs = self.obs_service.connect()
            await self._emit(EventType.obs_status, {"connected": obs.connected, "scenes": obs.scenes, "host": obs.host, "port": obs.port})
            await self.publish_camera_list()

            await self._transition(PipelineState.transcribing)
            final_text = ""
            stt_start = time.perf_counter()
            async for chunk in self.stt_service.stream_transcripts():
                await self._emit(EventType.transcript_final if chunk.is_final else EventType.transcript_partial, {"text": chunk.text})
                if chunk.is_final:
                    final_text = chunk.text
            self._timings["stt_seconds"] = round(time.perf_counter() - stt_start, 3)

            await self._transition(PipelineState.thinking)
            reply = []
            llm_start = time.perf_counter()
            async for token in self.ollama_service.stream_response(final_text):
                reply.append(token)
                await self._emit(EventType.ai_response_partial, {"text": "".join(reply)})
            full_reply = "".join(reply).strip() or "(empty response)"
            self._timings["ollama_seconds"] = round(time.perf_counter() - llm_start, 3)
            await self._emit(EventType.ai_response_final, {"text": full_reply})

            await self._transition(PipelineState.speaking)
            tts_start = time.perf_counter()
            wav_path = await self.tts_service.synthesize_to_wav(full_reply)
            self._timings["tts_seconds"] = round(time.perf_counter() - tts_start, 3)

            await self._transition(PipelineState.camera_ready)
            frame_path = self.webcam_service.capture_frame()
            await self._transition(PipelineState.rendering_preview)
            preview = await self.lipsync_service.render_chunk(wav_path, frame_path)
            self.render_queue.push(preview)
            await self._emit(EventType.preview_chunk_ready, preview.model_dump(mode="json"))
            await self._emit(EventType.preview_status, {"ready": True, "latest": preview.model_dump(mode="json")})

            await self._transition(PipelineState.streaming)
            if obs.connected:
                await self._emit(EventType.log, {"message": "OBS audio updated", "meta": self.obs_service.push_audio_file(wav_path)})
            self._timings["total_seconds"] = round(time.perf_counter() - cycle_start, 3)
            await self._emit(EventType.pipeline_timing, self._timings)
            await self._transition(PipelineState.idle)
        except asyncio.CancelledError:
            logger.info("Pipeline run cancelled")
            raise
        except Exception as exc:
            logger.exception("Pipeline failed: %s", exc)
            self._sm.force_error()
            await self._emit(EventType.render_error, {"message": str(exc)})
            await self._emit(EventType.error, {"message": str(exc)})
            await self._emit(EventType.pipeline_state, {"state": self.state.value})
