from __future__ import annotations

from collections import deque
from typing import Deque, Optional

from app.models.webcam import PreviewChunk


class RenderQueueService:
    def __init__(self, max_history: int = 20) -> None:
        self._history: Deque[PreviewChunk] = deque(maxlen=max_history)

    def push(self, chunk: PreviewChunk) -> None:
        self._history.appendleft(chunk)

    def latest(self) -> Optional[PreviewChunk]:
        return self._history[0] if self._history else None

    def history(self) -> list[PreviewChunk]:
        return list(self._history)
