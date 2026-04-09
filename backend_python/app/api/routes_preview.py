from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_orchestrator

router = APIRouter(prefix="/api/preview", tags=["preview"])


@router.get("/latest")
async def get_latest_preview(orchestrator=Depends(get_orchestrator)) -> dict:
    chunk = orchestrator.latest_preview()
    if not chunk:
        raise HTTPException(status_code=404, detail="No preview chunks yet")
    return chunk.model_dump(mode="json")


@router.get("/history")
async def get_preview_history(orchestrator=Depends(get_orchestrator)) -> dict:
    return {"items": [chunk.model_dump(mode="json") for chunk in orchestrator.preview_history()]}
