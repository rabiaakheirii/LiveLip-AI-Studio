from __future__ import annotations

from pydantic import BaseModel


class StageTiming(BaseModel):
    capture_ms: float = 0.0
    stt_ms: float = 0.0
    ollama_ms: float = 0.0
    tts_ms: float = 0.0
    lipsync_ms: float = 0.0
    encode_ms: float = 0.0
    obs_ms: float = 0.0


class PerformanceMetrics(BaseModel):
    fps_actual: float = 0.0
    frames_processed: int = 0
    frames_dropped: int = 0
    queue_pressure: float = 0.0
    adaptive_degraded: bool = False
    stage_timing: StageTiming = StageTiming()
