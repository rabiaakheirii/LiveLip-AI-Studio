from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="flutter_live_lipsync_assistant")
    environment: str = Field(default="dev")
    log_level: str = Field(default="INFO")
    json_logs: bool = Field(default=False)

    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)

    ollama_base_url: str = Field(default="http://127.0.0.1:11434")
    ollama_model: str = Field(default="llama3.2:3b")
    ollama_timeout_seconds: int = Field(default=60)

    tts_voice: str = Field(default="piper-en_US-amy-medium")
    output_dir: str = Field(default="./runtime")

    obs_host: str = Field(default="127.0.0.1")
    obs_port: int = Field(default=4455)
    obs_password: str = Field(default="")
    obs_scene: str = Field(default="Scene")
    obs_audio_source: str = Field(default="LiveLipSyncAudio")
    obs_video_source: str = Field(default="LiveLipSyncVideo")
    obs_video_mode: str = Field(default="media_source_refresh")

    webcam_max_devices: int = Field(default=3)

    lipsync_engine: str = Field(default="ffmpeg")
    enable_experimental_engines: bool = Field(default=False)

    stream_target_fps: int = Field(default=10)
    stream_frame_queue_size: int = Field(default=12)
    stream_audio_queue_size: int = Field(default=12)
    stream_preview_mode: str = Field(default="mjpeg")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("stream_target_fps")
    @classmethod
    def validate_fps(cls, value: int) -> int:
        if value < 1 or value > 60:
            raise ValueError("STREAM_TARGET_FPS must be between 1 and 60")
        return value

    @field_validator("lipsync_engine")
    @classmethod
    def validate_engine(cls, value: str) -> str:
        allowed = {"mock", "ffmpeg", "wav2lip", "musetalk", "liveportrait"}
        if value not in allowed:
            raise ValueError(f"LIPSYNC_ENGINE must be one of {sorted(allowed)}")
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
