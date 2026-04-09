from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_orchestrator

router = APIRouter(prefix="/api/webcam", tags=["webcam"])


class SelectCameraRequest(BaseModel):
    index: int


@router.get("/devices")
async def list_devices(orchestrator=Depends(get_orchestrator)) -> dict:
    cams = [cam.model_dump(mode="json") for cam in orchestrator.list_cameras()]
    return {"items": cams, "selected_index": orchestrator.webcam_service.selected_index}


@router.post("/select")
async def select_device(payload: SelectCameraRequest, orchestrator=Depends(get_orchestrator)) -> dict:
    selected = orchestrator.select_camera(payload.index)
    await orchestrator.publish_camera_selected(selected)
    return selected.model_dump(mode="json")
