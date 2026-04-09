from __future__ import annotations

import subprocess
import uuid
from datetime import datetime
from pathlib import Path

from app.core.frame_queue import FramePacket
from app.models.webcam import PreviewChunk
from app.services.lipsync_engines.base import BaseLipSyncEngine, EngineFrameResult


class FFmpegLipSyncEngine(BaseLipSyncEngine):
    name = "ffmpeg"

    async def process_frame(self, frame: FramePacket, audio_bytes: bytes | None = None) -> EngineFrameResult:  # noqa: ARG002
        # placeholder: pass-through frame (hook for real lip-sync inference)
        return EngineFrameResult(seq_id=frame.seq_id, ts=frame.ts, jpeg_bytes=frame.jpeg_bytes, engine=self.name)

    async def render_chunk(self, audio_path: Path, frame_path: Path, output_dir: Path, source: str = "webcam") -> PreviewChunk:
        chunk_id = uuid.uuid4().hex[:10]
        file_name = f"preview_{chunk_id}.mp4"
        output_path = output_dir / file_name
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", str(frame_path), "-i", str(audio_path), "-shortest",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(output_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return PreviewChunk(
            chunk_id=chunk_id,
            file_name=file_name,
            file_path=str(output_path),
            preview_url=f"/preview/{file_name}",
            created_at=datetime.utcnow(),
            source=source,
        )
