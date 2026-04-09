from __future__ import annotations

import base64
import logging
from datetime import datetime
from pathlib import Path
from typing import List

try:
    import cv2
except Exception:  # pragma: no cover - optional runtime dependency
    cv2 = None

from app.models.webcam import CameraDevice

logger = logging.getLogger(__name__)

# 1x1 black jpeg fallback
_MIN_JPEG = base64.b64decode(
    b"/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxAQEBAQEA8QEA8PDw8PDw8QDw8QDw8QFREWFhURFRUYHSggGBolGxUVITEhJSkrLi4uFx8zODMsNygtLisBCgoKDg0OFQ8PGi0dHR0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAAEAAQMBIgACEQEDEQH/xAAXAAEBAQEAAAAAAAAAAAAAAAAAAQID/8QAFhABAQEAAAAAAAAAAAAAAAAAAQAC/9oADAMBAAIQAxAAAAGmA//EABQQAQAAAAAAAAAAAAAAAAAAACD/2gAIAQEAAQUCt//EABQRAQAAAAAAAAAAAAAAAAAAACD/2gAIAQMBAT8BT//EABQRAQAAAAAAAAAAAAAAAAAAACD/2gAIAQIBAT8BT//EABQQAQAAAAAAAAAAAAAAAAAAACD/2gAIAQEABj8Cf//Z"
)


class WebcamService:
    def __init__(self, frames_dir: Path, max_devices: int = 3) -> None:
        self._frames_dir = frames_dir
        self._max_devices = max_devices
        self._selected_index = 0

    def list_cameras(self) -> List[CameraDevice]:
        if cv2 is None:
            return [CameraDevice(id="mock-0", index=0, name="Mock Camera (OpenCV missing)", available=False)]

        devices: list[CameraDevice] = []
        for idx in range(self._max_devices):
            cap = cv2.VideoCapture(idx)
            ok, _ = cap.read()
            cap.release()
            if ok:
                devices.append(CameraDevice(id=f"camera-{idx}", index=idx, name=f"Camera {idx}", available=True))

        if not devices:
            devices.append(CameraDevice(id="mock-0", index=0, name="Mock Camera (No device)", available=False))
        return devices

    def select_camera(self, index: int) -> CameraDevice:
        cameras = self.list_cameras()
        found = next((c for c in cameras if c.index == index), None)
        if found:
            self._selected_index = index
            return found
        logger.warning("Requested camera index %s unavailable; keeping %s", index, self._selected_index)
        return cameras[0]

    @property
    def selected_index(self) -> int:
        return self._selected_index

    def capture_frame_bytes(self) -> bytes:
        if cv2 is None:
            return _MIN_JPEG
        cap = cv2.VideoCapture(self._selected_index)
        ok, frame = cap.read()
        cap.release()
        if not ok:
            logger.warning("Failed to capture from camera %s; using fallback frame", self._selected_index)
            return _MIN_JPEG
        ok_enc, encoded = cv2.imencode(".jpg", frame)
        return encoded.tobytes() if ok_enc else _MIN_JPEG

    def capture_frame(self) -> Path:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        out_path = self._frames_dir / f"frame_{ts}.jpg"
        out_path.write_bytes(self.capture_frame_bytes())
        return out_path
