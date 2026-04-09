from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import AsyncIterator, List


@dataclass
class TranscriptResult:
    text: str
    is_final: bool


class STTService:
    """Placeholder local-first STT service.

    TODO: replace with faster-whisper streaming microphone transcription.
    """

    async def stream_transcripts(self) -> AsyncIterator[TranscriptResult]:
        demo_chunks: List[str] = [
            "hello",
            "hello this is",
            "hello this is a local",
            "hello this is a local test",
        ]
        for chunk in demo_chunks[:-1]:
            await asyncio.sleep(0.35)
            yield TranscriptResult(text=chunk, is_final=False)

        await asyncio.sleep(0.4)
        yield TranscriptResult(text=demo_chunks[-1], is_final=True)
