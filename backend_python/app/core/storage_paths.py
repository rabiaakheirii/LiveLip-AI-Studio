from __future__ import annotations

from pathlib import Path


class StoragePaths:
    def __init__(self, base_dir: str) -> None:
        self.base = Path(base_dir)
        self.audio = self.base / "audio"
        self.preview = self.base / "preview"
        self.frames = self.base / "frames"
        self.cache = self.base / "cache"

        for path in [self.base, self.audio, self.preview, self.frames, self.cache]:
            path.mkdir(parents=True, exist_ok=True)
