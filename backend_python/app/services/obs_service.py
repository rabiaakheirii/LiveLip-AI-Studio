from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from obsws_python import ReqClient


@dataclass
class OBSStatus:
    connected: bool
    host: str
    port: int
    scenes: List[str]


class OBSService:
    def __init__(
        self,
        host: str,
        port: int,
        password: str,
        default_scene: str,
        audio_source: str,
        video_source: str,
    ) -> None:
        self._host = host
        self._port = port
        self._password = password
        self._default_scene = default_scene
        self._audio_source = audio_source
        self._video_source = video_source
        self._client: ReqClient | None = None

    @property
    def is_connected(self) -> bool:
        return self._client is not None

    def connect(self) -> OBSStatus:
        try:
            self._client = ReqClient(host=self._host, port=self._port, password=self._password, timeout=3)
            scenes_resp = self._client.get_scene_list()
            scenes = [scene["sceneName"] for scene in scenes_resp.scenes]
            return OBSStatus(connected=True, host=self._host, port=self._port, scenes=scenes)
        except Exception:
            self._client = None
            return OBSStatus(connected=False, host=self._host, port=self._port, scenes=[])

    def push_audio_file(self, wav_path: Path) -> dict:
        if not self._client:
            raise RuntimeError("OBS is not connected")
        self._client.set_input_settings(
            self._audio_source,
            {"local_file": str(wav_path), "is_local_file": True, "looping": False},
            overlay=True,
        )
        return {"audio_source": self._audio_source, "file": str(wav_path)}

    def push_preview_video(self, preview_path: Path) -> dict:
        if not self._client:
            raise RuntimeError("OBS is not connected")
        self._client.set_input_settings(
            self._video_source,
            {"local_file": str(preview_path), "is_local_file": True, "looping": False},
            overlay=True,
        )
        return {"video_source": self._video_source, "file": str(preview_path), "mode": "media_source_refresh"}

    def push_stream_endpoint(self, video_mode: str, stream_url: str, latest_file: Path) -> dict:
        """Phase 3 live-output abstraction.

        video_mode:
        - media_source_refresh (works now)
        - browser_source_url (works if source type supports URL)
        """
        if not self._client:
            return {"ok": False, "connected": False, "mode": video_mode}

        if video_mode == "browser_source_url":
            self._client.set_input_settings(self._video_source, {"url": stream_url}, overlay=True)
            return {"ok": True, "connected": True, "mode": video_mode, "stream_url": stream_url}

        self._client.set_input_settings(
            self._video_source,
            {"local_file": str(latest_file), "is_local_file": True, "looping": False},
            overlay=True,
        )
        return {"ok": True, "connected": True, "mode": "media_source_refresh", "file": str(latest_file)}
