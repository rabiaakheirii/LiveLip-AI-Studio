from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AVSyncEstimator:
    last_frame_ts: datetime | None = None
    last_audio_ts: datetime | None = None

    def on_frame(self, ts: datetime) -> None:
        self.last_frame_ts = ts

    def on_audio(self, ts: datetime) -> None:
        self.last_audio_ts = ts

    def drift_ms(self) -> float:
        if not self.last_audio_ts or not self.last_frame_ts:
            return 0.0
        return (self.last_frame_ts - self.last_audio_ts).total_seconds() * 1000.0
