from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FramePacket:
    seq_id: int
    ts: datetime
    jpeg_bytes: bytes


class FrameQueue:
    def __init__(self, maxsize: int) -> None:
        self._queue: asyncio.Queue[FramePacket] = asyncio.Queue(maxsize=maxsize)
        self.maxsize = maxsize
        self.dropped_frames = 0

    async def put(self, packet: FramePacket) -> None:
        if self._queue.full():
            try:
                self._queue.get_nowait()
                self._queue.task_done()
                self.dropped_frames += 1
            except asyncio.QueueEmpty:
                pass
        await self._queue.put(packet)

    async def get(self) -> FramePacket:
        packet = await self._queue.get()
        self._queue.task_done()
        return packet

    def qsize(self) -> int:
        return self._queue.qsize()
