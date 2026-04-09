from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AudioPacket:
    seq_id: int
    ts: datetime
    wav_bytes: bytes


class AudioQueue:
    def __init__(self, maxsize: int) -> None:
        self._queue: asyncio.Queue[AudioPacket] = asyncio.Queue(maxsize=maxsize)
        self.maxsize = maxsize

    async def put(self, packet: AudioPacket) -> None:
        if self._queue.full():
            try:
                self._queue.get_nowait()
                self._queue.task_done()
            except asyncio.QueueEmpty:
                pass
        await self._queue.put(packet)

    def latest_or_none(self) -> AudioPacket | None:
        latest = None
        while True:
            try:
                latest = self._queue.get_nowait()
                self._queue.task_done()
            except asyncio.QueueEmpty:
                break
        return latest

    def qsize(self) -> int:
        return self._queue.qsize()
