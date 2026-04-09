from __future__ import annotations

from fastapi import Request

from app.core.orchestrator import PipelineOrchestrator


def get_orchestrator(request: Request) -> PipelineOrchestrator:
    return request.app.state.orchestrator
