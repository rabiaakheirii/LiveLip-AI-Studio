from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import get_settings

router = APIRouter(prefix="/settings", tags=["settings"])


class SettingsResponse(BaseModel):
    ollama_model: str
    tts_voice: str
    obs_scene: str


class UpdateSettingsRequest(BaseModel):
    ollama_model: str | None = None
    tts_voice: str | None = None
    obs_scene: str | None = None


@router.get("", response_model=SettingsResponse)
async def get_current_settings() -> SettingsResponse:
    settings = get_settings()
    return SettingsResponse(
        ollama_model=settings.ollama_model,
        tts_voice=settings.tts_voice,
        obs_scene=settings.obs_scene,
    )


@router.post("", response_model=SettingsResponse)
async def update_settings(payload: UpdateSettingsRequest) -> SettingsResponse:
    settings = get_settings()
    # In-memory only for MVP; persist later via config store.
    data = {
        "ollama_model": payload.ollama_model or settings.ollama_model,
        "tts_voice": payload.tts_voice or settings.tts_voice,
        "obs_scene": payload.obs_scene or settings.obs_scene,
    }
    return SettingsResponse(**data)
