from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

from fastapi import WebSocket

from app.core.config import Settings
from app.core.events import EventMessage, EventType, PipelineState
from app.core.state_machine import PipelineStateMachine
from app.services.lipsync_service import LipSyncService
from app.services.obs_service import OBSService
from app.services.ollama_service import OllamaService
from app.services.stt_service import STTService
from app.services.tts_service import TTSService

logger = logging.getLogger(__name__)


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
        self._event_bus = event_bus
        self._sm = PipelineStateMachine()
        self._task: asyncio.Task | None = None
        self._timings: dict[str, float] = {}

        self.stt_service = STTService()
        self.ollama_service = OllamaService(settings.ollama_base_url, settings.ollama_model)
        self.tts_service = TTSService(settings.output_dir, settings.tts_voice)
        self.lipsync_service = LipSyncService()
        self.obs_service = OBSService(
            host=settings.obs_host,
            port=settings.obs_port,
            password=settings.obs_password,
            default_scene=settings.obs_scene,
            audio_source=settings.obs_audio_source,
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

    async def _emit(self, event_type: EventType, data: dict[str, Any]) -> None:
        await self._event_bus.broadcast(EventMessage(event_type=event_type, data=data))

    async def _transition(self, next_state: PipelineState) -> None:
        self._sm.transition(next_state)
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
        self._sm = PipelineStateMachine()
        await self._emit(EventType.pipeline_state, {"state": self.state.value})

    async def _run_once(self) -> None:
        cycle_start = time.perf_counter()
        try:
            await self._transition(PipelineState.listening)
            obs = self.obs_service.connect()
            await self._emit(
                EventType.obs_status,
                {"connected": obs.connected, "scenes": obs.scenes, "host": obs.host, "port": obs.port},
            )

            await self._transition(PipelineState.transcribing)
            final_text = ""
            async for chunk in self.stt_service.stream_transcripts():
                if chunk.is_final:
                    final_text = chunk.text
                    await self._emit(EventType.transcript_final, {"text": chunk.text})
                else:
                    await self._emit(EventType.transcript_partial, {"text": chunk.text})

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

            await self._transition(PipelineState.streaming)
            if obs.connected:
                result = self.obs_service.push_audio_file(wav_path)
                await self._emit(EventType.log, {"message": "OBS audio updated", "meta": result})
            else:
                await self._emit(EventType.log, {"message": "OBS not connected; skipping audio push"})

            self._timings["total_seconds"] = round(time.perf_counter() - cycle_start, 3)
            await self._emit(EventType.pipeline_timing, self._timings)

            await self._transition(PipelineState.idle)
        except asyncio.CancelledError:
            logger.info("Pipeline run cancelled")
            raise
        except Exception as exc:
            logger.exception("Pipeline failed: %s", exc)
            self._sm.force_error()
            await self._emit(EventType.error, {"message": str(exc)})
            await self._emit(EventType.pipeline_state, {"state": self.state.value})
