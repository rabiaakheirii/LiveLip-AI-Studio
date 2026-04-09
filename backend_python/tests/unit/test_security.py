from pathlib import Path

from app.core.security import is_safe_preview_path


def test_safe_preview_path_allows_inside_base(tmp_path: Path):
    assert is_safe_preview_path(tmp_path, 'a.jpg') is True


def test_safe_preview_path_blocks_traversal(tmp_path: Path):
    assert is_safe_preview_path(tmp_path, '../etc/passwd') is False
