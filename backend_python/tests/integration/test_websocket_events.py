from fastapi.testclient import TestClient

from app.main import app


def test_ws_connect_and_receive_camera_list_or_stream_status():
    client = TestClient(app)
    with client.websocket_connect('/ws/events') as ws:
        ws.send_text('ping')
        msg = ws.receive_json()
        assert msg['event_type'] in {'camera_list', 'stream_status'}
