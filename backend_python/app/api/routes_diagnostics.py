from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_orchestrator

router = APIRouter(prefix="/api/diagnostics", tags=["diagnostics"])


class LogLevelRequest(BaseModel):
    log_level: str


@router.get("/summary")
async def summary(orchestrator=Depends(get_orchestrator)) -> dict:
    return orchestrator.get_diagnostics_summary().model_dump(mode="json")


@router.post("/log-level")
async def set_log_level(payload: LogLevelRequest) -> dict:
    import logging

    level = payload.log_level.upper()
    logging.getLogger().setLevel(getattr(logging, level, logging.INFO))
    return {"status": "ok", "log_level": level}


@router.get("/metrics")
async def metrics(orchestrator=Depends(get_orchestrator)) -> dict:
    return orchestrator.stream_status().model_dump(mode="json")
