from __future__ import annotations

import asyncio


class WorkerManager:
    def __init__(self) -> None:
        self._tasks: list[asyncio.Task] = []

    def start(self, coro, name: str) -> None:
        self._tasks.append(asyncio.create_task(coro, name=name))

    async def stop_all(self) -> None:
        for task in self._tasks:
            task.cancel()
        for task in self._tasks:
            try:
                await task
            except asyncio.CancelledError:
                pass
        self._tasks.clear()

    @property
    def running(self) -> bool:
        return any(not t.done() for t in self._tasks)
