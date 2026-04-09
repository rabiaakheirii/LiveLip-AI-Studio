from __future__ import annotations

import asyncio
import logging

logger = logging.getLogger(__name__)


class WorkerManager:
    def __init__(self) -> None:
        self._tasks: dict[str, asyncio.Task] = {}

    def start(self, coro, name: str) -> None:
        if name in self._tasks and not self._tasks[name].done():
            return
        task = asyncio.create_task(coro, name=name)
        task.add_done_callback(lambda t, n=name: self._on_task_done(n, t))
        self._tasks[name] = task

    def _on_task_done(self, name: str, task: asyncio.Task) -> None:
        try:
            exc = task.exception()
            if exc:
                logger.error("Worker %s crashed: %s", name, exc)
        except asyncio.CancelledError:
            logger.info("Worker %s cancelled", name)

    async def stop_all(self, timeout: float = 2.0) -> None:
        for task in self._tasks.values():
            task.cancel()
        for task in self._tasks.values():
            try:
                await asyncio.wait_for(task, timeout=timeout)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
        self._tasks.clear()

    @property
    def running(self) -> bool:
        return any(not t.done() for t in self._tasks.values())
