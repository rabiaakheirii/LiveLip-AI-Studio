from app.workers.worker_modes import resolve_worker_mode


def test_local_worker_mode_supported():
    status = resolve_worker_mode('local', '')
    assert status.supported is True


def test_remote_worker_requires_url():
    status = resolve_worker_mode('remote', '')
    assert status.supported is False
