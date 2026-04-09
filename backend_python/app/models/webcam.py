from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class CameraDevice(BaseModel):
    id: str
    index: int
    name: str
    available: bool = True


class PreviewChunk(BaseModel):
    chunk_id: str
    file_name: str
    file_path: str
    preview_url: str
    created_at: datetime
    duration_seconds: float | None = None
    source: str = "webcam"
