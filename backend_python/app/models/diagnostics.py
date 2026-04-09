from __future__ import annotations

from pydantic import BaseModel


class CapabilityStatus(BaseModel):
    webcam_available: bool
    ffmpeg_available: bool
    ollama_reachable: bool
    obs_reachable: bool
    selected_lipsync_engine: str
    degraded_mode: bool
    engine_capabilities: dict[str, bool]
    remote_worker_available: bool


class DiagnosticsSummary(BaseModel):
    app_name: str
    environment: str
    log_level: str
    stream_running: bool
    worker_mode: str
    capability: CapabilityStatus
    stream_message: str
