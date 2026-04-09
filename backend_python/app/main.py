from __future__ import annotations

import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from app.api.routes_pipeline import router as pipeline_router
from app.api.routes_preview import router as preview_router
from app.api.routes_settings import router as settings_router
from app.api.routes_webcam import router as webcam_router
from app.core.config import get_settings
from app.core.orchestrator import EventBus, PipelineOrchestrator


def configure_logging(log_level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title=settings.app_name)
    event_bus = EventBus()
    orchestrator = PipelineOrchestrator(settings, event_bus)

    app.state.event_bus = event_bus
    app.state.orchestrator = orchestrator

    app.include_router(pipeline_router)
    app.include_router(settings_router)
    app.include_router(preview_router)
    app.include_router(webcam_router)
    app.mount("/preview", StaticFiles(directory=orchestrator.preview_dir), name="preview")

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok", "service": settings.app_name}

    @app.websocket("/ws/events")
    async def ws_events(websocket: WebSocket):
        await event_bus.connect(websocket)
        await orchestrator.publish_camera_list()
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            event_bus.disconnect(websocket)

    return app


app = create_app()
