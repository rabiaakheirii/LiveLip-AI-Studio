from __future__ import annotations

from fastapi import APIRouter, Depends

from app.dependencies import get_orchestrator

router = APIRouter(prefix="/api/performance", tags=["performance"])


@router.get("/metrics")
async def get_performance_metrics(orchestrator=Depends(get_orchestrator)) -> dict:
    return orchestrator.performance_metrics().model_dump(mode="json")
