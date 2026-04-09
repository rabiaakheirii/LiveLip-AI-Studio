import pytest

from app.core.config import Settings


def test_config_invalid_fps_raises():
    with pytest.raises(ValueError):
        Settings(stream_target_fps=0)


def test_config_invalid_engine_raises():
    with pytest.raises(ValueError):
        Settings(lipsync_engine="invalid")
