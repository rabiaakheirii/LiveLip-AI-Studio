from __future__ import annotations

import httpx


class RemoteWorkerClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip('/')

    async def health(self) -> dict:
        if not self.base_url:
            return {"available": False, "reason": "base_url_missing"}
        try:
            async with httpx.AsyncClient(timeout=2) as client:
                resp = await client.get(f"{self.base_url}/health")
                return {"available": resp.status_code == 200, "status_code": resp.status_code}
        except Exception as exc:
            return {"available": False, "reason": str(exc)}
