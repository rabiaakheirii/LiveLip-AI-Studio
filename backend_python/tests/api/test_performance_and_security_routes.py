from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_performance_metrics_route():
    r = client.get('/api/performance/metrics')
    assert r.status_code == 200
    assert 'fps_actual' in r.json()


def test_protected_pipeline_route_without_token_when_token_empty():
    # default settings token is empty, so request should pass
    r = client.get('/pipeline/state')
    assert r.status_code == 200
