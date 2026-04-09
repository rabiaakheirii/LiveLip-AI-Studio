from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.dependencies.auth import require_api_token
from app.dependencies import get_orchestrator

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


class PipelineControlResponse(BaseModel):
    status: str
    message: str


@router.post("/start", response_model=PipelineControlResponse)
async def start_pipeline(orchestrator=Depends(get_orchestrator), _auth=Depends(require_api_token)) -> PipelineControlResponse:
    if orchestrator.is_running:
        raise HTTPException(status_code=409, detail="Pipeline already running")
    await orchestrator.start()
    return PipelineControlResponse(status="ok", message="Pipeline started")


@router.post("/stop", response_model=PipelineControlResponse)
async def stop_pipeline(orchestrator=Depends(get_orchestrator), _auth=Depends(require_api_token)) -> PipelineControlResponse:
    await orchestrator.stop()
    return PipelineControlResponse(status="ok", message="Pipeline stopped")


@router.get("/state")
async def get_pipeline_state(orchestrator=Depends(get_orchestrator), _auth=Depends(require_api_token)) -> dict:
    return {
        "state": orchestrator.state.value,
        "running": orchestrator.is_running,
        "timings": orchestrator.timings,
    }
