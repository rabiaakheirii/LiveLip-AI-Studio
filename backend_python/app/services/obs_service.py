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
    def __init__(self, host: str, port: int, password: str, default_scene: str, audio_source: str) -> None:
        self._host = host
        self._port = port
        self._password = password
        self._default_scene = default_scene
        self._audio_source = audio_source
        self._client: ReqClient | None = None

    def connect(self) -> OBSStatus:
        try:
            self._client = ReqClient(host=self._host, port=self._port, password=self._password, timeout=3)
            scenes_resp = self._client.get_scene_list()
            scenes = [scene["sceneName"] for scene in scenes_resp.scenes]
            return OBSStatus(connected=True, host=self._host, port=self._port, scenes=scenes)
        except Exception:
            self._client = None
            return OBSStatus(connected=False, host=self._host, port=self._port, scenes=[])

    def list_scenes(self) -> List[str]:
        if not self._client:
            return []
        scenes_resp = self._client.get_scene_list()
        return [scene["sceneName"] for scene in scenes_resp.scenes]

    def set_current_scene(self, scene_name: str) -> None:
        if not self._client:
            raise RuntimeError("OBS is not connected")
        self._client.set_current_program_scene(scene_name)

    def push_audio_file(self, wav_path: Path) -> dict:
        """MVP action: update a media source file path in OBS.

        Requires `self._audio_source` to point to a Media Source input.
        """
        if not self._client:
            raise RuntimeError("OBS is not connected")
        self._client.set_input_settings(
            self._audio_source,
            {
                "local_file": str(wav_path),
                "is_local_file": True,
                "looping": False,
            },
            overlay=True,
        )
        return {"audio_source": self._audio_source, "file": str(wav_path)}
