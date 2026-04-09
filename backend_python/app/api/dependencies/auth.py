from __future__ import annotations

from fastapi import Header, HTTPException

from app.core.config import get_settings


def require_api_token(x_api_token: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if not settings.api_auth_token:
        return
    if x_api_token != settings.api_auth_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
