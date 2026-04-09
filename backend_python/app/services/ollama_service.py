from __future__ import annotations

from typing import AsyncIterator

import httpx


class OllamaService:
    def __init__(self, base_url: str, model: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model

    async def stream_response(self, prompt: str) -> AsyncIterator[str]:
        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", f"{self._base_url}/api/generate", json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line.strip():
                        continue
                    # Ollama returns JSON lines.
                    # We keep it robust to malformed lines.
                    try:
                        import json

                        parsed = json.loads(line)
                    except Exception:
                        continue
                    token = parsed.get("response", "")
                    if token:
                        yield token
                    if parsed.get("done"):
                        return
