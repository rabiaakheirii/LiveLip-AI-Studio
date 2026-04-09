from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class StreamMetrics(BaseModel):
    running: bool = False
    degraded_mode: bool = False
    lipsync_engine: str = "mock"
    target_fps: int = 10
    capture_queue_size: int = 0
    audio_queue_size: int = 0
    dropped_frames: int = 0
    queue_pressure: float = 0.0
    av_drift_ms: float = 0.0
    last_frame_ts: datetime | None = None
    obs_live_ready: bool = False
    message: str = "idle"
    updated_at: datetime = Field(default_factory=datetime.utcnow)
