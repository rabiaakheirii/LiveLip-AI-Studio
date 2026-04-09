from __future__ import annotations

from pathlib import Path


def is_safe_preview_path(base_dir: Path, requested_name: str) -> bool:
    candidate = (base_dir / requested_name).resolve()
    return str(candidate).startswith(str(base_dir.resolve()))
