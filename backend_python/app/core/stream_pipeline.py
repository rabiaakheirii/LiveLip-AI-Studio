from __future__ import annotations

import asyncio
import logging
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Awaitable, Callable

from app.core.audio_queue import AudioPacket, AudioQueue
from app.core.av_sync import AVSyncEstimator
from app.core.error_handling import boundary
from app.core.frame_queue import FramePacket, FrameQueue
from app.core.retry import with_retry
from app.core.worker_manager import WorkerManager
from app.models.stream_metrics import StreamMetrics
from app.services.lipsync_service import LipSyncService
from app.services.obs_service import OBSService
from app.services.webcam_service import WebcamService

logger = logging.getLogger(__name__)

EventCallback = Callable[[str, dict], Awaitable[None]]


class StreamPipeline:
    def __init__(
        self,
        webcam_service: WebcamService,
        lipsync_service: LipSyncService,
        obs_service: OBSService,
        event_cb: EventCallback,
        output_dir: Path,
        target_fps: int = 10,
        frame_queue_size: int = 12,
        audio_queue_size: int = 12,
        obs_video_mode: str = "media_source_refresh",
    ) -> None:
        self.webcam_service = webcam_service
        self.lipsync_service = lipsync_service
        self.obs_service = obs_service
        self.event_cb = event_cb
        self.output_dir = output_dir
        self.target_fps = max(1, target_fps)
        self.obs_video_mode = obs_video_mode

        self.frame_queue = FrameQueue(frame_queue_size)
        self.audio_queue = AudioQueue(audio_queue_size)
        self.sync = AVSyncEstimator()
        self.workers = WorkerManager()

        self._running = False
        self._latest_frame: bytes | None = None
        self._latest_seq = 0
        self._latest_file = output_dir / "stream_latest.jpg"
        self.metrics = StreamMetrics(target_fps=self.target_fps, lipsync_engine=self.lipsync_service.engine_name)

    @property
    def running(self) -> bool:
        return self._running and self.workers.running

    def latest_frame(self) -> bytes | None:
        return self._latest_frame

    def status(self) -> StreamMetrics:
        self.metrics.capture_queue_size = self.frame_queue.qsize()
        self.metrics.audio_queue_size = self.audio_queue.qsize()
        self.metrics.dropped_frames = self.frame_queue.dropped_frames
        self.metrics.queue_pressure = min(1.0, self.frame_queue.qsize() / max(1, self.frame_queue.maxsize))
        self.metrics.av_drift_ms = self.sync.drift_ms()
        self.metrics.running = self.running
        self.metrics.degraded_mode = self.lipsync_service.degraded_mode
        self.metrics.updated_at = datetime.utcnow()
        return self.metrics

    async def start(self) -> None:
        if self.running:
            return
        self._running = True
        self.metrics.message = "stream_initializing"
        await self.event_cb("stream_started", {"message": "Stream workers starting"})
        await self.event_cb("lipsync_engine_changed", {"engine": self.lipsync_service.engine_name})

        self.workers.start(self._capture_loop(), "capture-loop")
        self.workers.start(self._audio_loop(), "audio-loop")
        self.workers.start(self._inference_loop(), "inference-loop")
        self.workers.start(self._publisher_loop(), "publisher-loop")

    async def stop(self) -> None:
        self._running = False
        await self.workers.stop_all()
        self.frame_queue = FrameQueue(self.frame_queue.maxsize)
        self.audio_queue = AudioQueue(self.audio_queue.maxsize)
        self.metrics.message = "stopped"
        await self.event_cb("stream_stopped", {"message": "Stream workers stopped"})

    async def _capture_loop(self) -> None:
        interval = 1.0 / self.target_fps
        while self._running:
            start = time.perf_counter()
            async with boundary("capture_loop"):
                self._latest_seq += 1
                frame = FramePacket(seq_id=self._latest_seq, ts=datetime.utcnow(), jpeg_bytes=self.webcam_service.capture_frame_bytes())
                await self.frame_queue.put(frame)
                self.sync.on_frame(frame.ts)
                if self.frame_queue.dropped_frames > 0:
                    await self.event_cb("frame_dropped", {"count": self.frame_queue.dropped_frames})
                await self.event_cb("queue_pressure", {"pressure": round(self.status().queue_pressure, 3)})
            await asyncio.sleep(max(0.0, interval - (time.perf_counter() - start)))

    async def _audio_loop(self) -> None:
        seq = 0
        while self._running:
            async with boundary("audio_loop"):
                seq += 1
                packet = AudioPacket(seq_id=seq, ts=datetime.utcnow(), wav_bytes=b"\x00\x00")
                await self.audio_queue.put(packet)
                self.sync.on_audio(packet.ts)
            await asyncio.sleep(0.2)

    async def _inference_loop(self) -> None:
        while self._running:
            frame = await self.frame_queue.get()
            audio_packet = self.audio_queue.latest_or_none()
            audio_bytes = audio_packet.wav_bytes if audio_packet else None

            async def _run():
                return await self.lipsync_service.process_frame(frame, audio_bytes=audio_bytes)

            result = await with_retry(_run, retries=1)
            self._latest_frame = result.jpeg_bytes
            self.metrics.last_frame_ts = result.ts
            if self.lipsync_service.degraded_mode:
                self.metrics.message = "degraded_mode"
            await self.event_cb("av_sync_status", {"drift_ms": round(self.sync.drift_ms(), 2)})

    async def _publisher_loop(self) -> None:
        while self._running:
            if self._latest_frame:
                self._latest_file.write_bytes(self._latest_frame)
                if self.obs_service.is_connected:
                    obs_state = self.obs_service.push_stream_endpoint(
                        video_mode=self.obs_video_mode,
                        stream_url="http://127.0.0.1:8000/api/stream/mjpeg",
                        latest_file=self._latest_file,
                    )
                    self.metrics.obs_live_ready = bool(obs_state.get("ok", False))
                    await self.event_cb("obs_live_status", obs_state)
                await self.event_cb("stream_status", self.status().model_dump(mode="json"))
            await asyncio.sleep(0.15)

    async def mjpeg_generator(self):
        while True:
            frame = self._latest_frame
            if frame is None:
                fallback = shutil.which("true")  # no-op anchor for diagnostics
                _ = fallback
                frame = b""
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            await asyncio.sleep(0.1)
