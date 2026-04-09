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
    error = "error"


class EventType(str, Enum):
    pipeline_state = "pipeline_state"
    transcript_partial = "transcript_partial"
    transcript_final = "transcript_final"
    ai_response_partial = "ai_response_partial"
    ai_response_final = "ai_response_final"
    obs_status = "obs_status"
    pipeline_timing = "pipeline_timing"
    log = "log"
    error = "error"


class EventMessage(BaseModel):
    event_type: EventType
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data: Dict[str, Any] = Field(default_factory=dict)
    trace_id: Optional[str] = None
