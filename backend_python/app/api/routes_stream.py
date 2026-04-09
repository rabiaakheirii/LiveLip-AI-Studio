from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, StreamingResponse

from app.api.dependencies.auth import require_api_token
from app.dependencies import get_orchestrator

router = APIRouter(prefix="/api/stream", tags=["stream"])


@router.post("/start")
async def start_stream(orchestrator=Depends(get_orchestrator), _auth=Depends(require_api_token)) -> dict:
    await orchestrator.start_stream()
    return {"status": "ok", "message": "stream started"}


@router.post("/stop")
async def stop_stream(orchestrator=Depends(get_orchestrator), _auth=Depends(require_api_token)) -> dict:
    await orchestrator.stop_stream()
    return {"status": "ok", "message": "stream stopped"}


@router.get("/status")
async def stream_status(orchestrator=Depends(get_orchestrator), _auth=Depends(require_api_token)) -> dict:
    return orchestrator.stream_status().model_dump(mode="json")


@router.get("/latest-frame")
async def latest_frame(orchestrator=Depends(get_orchestrator), _auth=Depends(require_api_token)):
    frame = orchestrator.stream_latest_frame()
    if not frame:
        raise HTTPException(status_code=404, detail="No frame available yet")
    return Response(content=frame, media_type="image/jpeg")


@router.get("/mjpeg")
async def stream_mjpeg(orchestrator=Depends(get_orchestrator), _auth=Depends(require_api_token)):
    return StreamingResponse(orchestrator.stream_mjpeg(), media_type="multipart/x-mixed-replace; boundary=frame")
