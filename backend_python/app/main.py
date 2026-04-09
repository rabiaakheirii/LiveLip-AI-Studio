from __future__ import annotations

import uuid

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from app.api.routes_diagnostics import router as diagnostics_router
from app.api.routes_pipeline import router as pipeline_router
from app.api.routes_preview import router as preview_router
from app.api.routes_settings import router as settings_router
from app.api.routes_stream import router as stream_router
from app.api.routes_webcam import router as webcam_router
from app.core.config import get_settings
from app.core.lifecycle import AppLifecycle
from app.core.logging_config import configure_logging
from app.core.orchestrator import EventBus, PipelineOrchestrator


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level, json_logs=settings.json_logs)

    app = FastAPI(title=settings.app_name)
    event_bus = EventBus()
    orchestrator = PipelineOrchestrator(settings, event_bus)
    lifecycle = AppLifecycle(orchestrator)

    app.state.event_bus = event_bus
    app.state.orchestrator = orchestrator

    app.include_router(pipeline_router)
    app.include_router(settings_router)
    app.include_router(preview_router)
    app.include_router(webcam_router)
    app.include_router(stream_router)
    app.include_router(diagnostics_router)
    app.mount("/preview", StaticFiles(directory=orchestrator.preview_dir), name="preview")

    @app.middleware("http")
    async def correlation_middleware(request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        return response

    @app.on_event("startup")
    async def on_startup() -> None:
        await lifecycle.startup()

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        await lifecycle.shutdown()

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok", "service": settings.app_name}

    @app.websocket("/ws/events")
    async def ws_events(websocket: WebSocket):
        await event_bus.connect(websocket)
        await orchestrator.publish_camera_list()
        await orchestrator._emit_by_name("stream_status", orchestrator.stream_status().model_dump(mode="json"))
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            event_bus.disconnect(websocket)

    return app


app = create_app()
