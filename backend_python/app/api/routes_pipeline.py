from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.dependencies import get_orchestrator

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


class PipelineControlResponse(BaseModel):
    status: str
    message: str


@router.post("/start", response_model=PipelineControlResponse)
async def start_pipeline(orchestrator=Depends(get_orchestrator)) -> PipelineControlResponse:
    if orchestrator.is_running:
        raise HTTPException(status_code=409, detail="Pipeline already running")
    await orchestrator.start()
    return PipelineControlResponse(status="ok", message="Pipeline started")


@router.post("/stop", response_model=PipelineControlResponse)
async def stop_pipeline(orchestrator=Depends(get_orchestrator)) -> PipelineControlResponse:
    await orchestrator.stop()
    return PipelineControlResponse(status="ok", message="Pipeline stopped")


@router.get("/state")
async def get_pipeline_state(orchestrator=Depends(get_orchestrator)) -> dict:
    return {
        "state": orchestrator.state.value,
        "running": orchestrator.is_running,
        "timings": orchestrator.timings,
    }
