from __future__ import annotations

import wave
from pathlib import Path


class TTSService:
    """Minimal TTS stub.

    TODO: replace with Piper/Kokoro/XTTS engine implementation.
    """

    def __init__(self, output_dir: str, voice: str) -> None:
        self._output_dir = Path(output_dir)
        self._voice = voice
        self._output_dir.mkdir(parents=True, exist_ok=True)

    async def synthesize_to_wav(self, text: str, filename: str = "response.wav") -> Path:
        # Generates silence WAV as a runnable placeholder.
        wav_path = self._output_dir / filename
        sample_rate = 22050
        duration_seconds = max(1, min(8, len(text) // 20 + 1))
        n_samples = sample_rate * duration_seconds

        with wave.open(str(wav_path), "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            silence = (0).to_bytes(2, byteorder="little", signed=True)
            wav_file.writeframes(silence * n_samples)

        return wav_path
