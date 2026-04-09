from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class PipelineState(str, Enum):
    idle = "idle"
    listening = "listening"
    transcribing = "transcribing"
    thinking = "thinking"
    speaking = "speaking"
    lip_syncing = "lip_syncing"
    streaming = "streaming"
    camera_ready = "camera_ready"
    capturing_video = "capturing_video"
    rendering_preview = "rendering_preview"
    preview_ready = "preview_ready"
    error = "error"


class EventType(str, Enum):
    pipeline_state = "pipeline_state"
    transcript_partial = "transcript_partial"
    transcript_final = "transcript_final"
    ai_response_partial = "ai_response_partial"
    ai_response_final = "ai_response_final"
    obs_status = "obs_status"
    pipeline_timing = "pipeline_timing"
    camera_list = "camera_list"
    camera_selected = "camera_selected"
    preview_chunk_ready = "preview_chunk_ready"
    preview_status = "preview_status"
    render_progress = "render_progress"
    render_error = "render_error"
    log = "log"
    error = "error"


class EventMessage(BaseModel):
    event_type: EventType
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data: Dict[str, Any] = Field(default_factory=dict)
    trace_id: Optional[str] = None
