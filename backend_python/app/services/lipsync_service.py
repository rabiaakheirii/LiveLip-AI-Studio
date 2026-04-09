from __future__ import annotations

import subprocess
import uuid
from datetime import datetime
from pathlib import Path

from app.models.webcam import PreviewChunk


class LipSyncService:
    """Chunk-based preview renderer.

    MVP: Uses FFmpeg to combine captured frame + TTS audio into an MP4 chunk.
    TODO: Replace with Wav2Lip / MuseTalk / LivePortrait pipeline.
    """

    def __init__(self, preview_dir: Path):
        self._preview_dir = preview_dir

    async def render_chunk(self, audio_path: Path, frame_path: Path, source: str = "webcam") -> PreviewChunk:
        chunk_id = uuid.uuid4().hex[:10]
        file_name = f"preview_{chunk_id}.mp4"
        output_path = self._preview_dir / file_name

        cmd = [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(frame_path),
            "-i",
            str(audio_path),
            "-shortest",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            str(output_path),
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
