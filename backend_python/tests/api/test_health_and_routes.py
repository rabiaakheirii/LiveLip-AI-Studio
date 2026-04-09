from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_ok():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


def test_webcam_devices_route():
    r = client.get('/api/webcam/devices')
    assert r.status_code == 200
    assert 'items' in r.json()


def test_preview_history_route():
    r = client.get('/api/preview/history')
    assert r.status_code == 200
    assert 'items' in r.json()


def test_stream_status_route():
    r = client.get('/api/stream/status')
    assert r.status_code == 200
    assert 'running' in r.json()


def test_diagnostics_summary_route():
    r = client.get('/api/diagnostics/summary')
    assert r.status_code == 200
    body = r.json()
    assert 'capability' in body
