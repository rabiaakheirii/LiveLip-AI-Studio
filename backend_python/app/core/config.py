from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="flutter_live_lipsync_assistant")
    environment: str = Field(default="dev")
    log_level: str = Field(default="INFO")

    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)

    ollama_base_url: str = Field(default="http://127.0.0.1:11434")
    ollama_model: str = Field(default="llama3.2:3b")

    tts_voice: str = Field(default="piper-en_US-amy-medium")
    output_dir: str = Field(default="./runtime")

    obs_host: str = Field(default="127.0.0.1")
    obs_port: int = Field(default=4455)
    obs_password: str = Field(default="")
    obs_scene: str = Field(default="Scene")
    obs_audio_source: str = Field(default="LiveLipSyncAudio")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
