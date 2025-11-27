from pathlib import Path
from typing import ClassVar

from pydantic import SecretStr, BaseModel, field_validator, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


_ROOT_DIR: Path = Path(__file__).parent.parent.parent


class _AudioFiles(BaseModel, frozen=True):
    model_config = ConfigDict(validate_default=True)

    _DIR_NAME: ClassVar[str] = 'audio'

    HAIL: str = 'hail.m4a'

    @field_validator('*')
    @classmethod
    def _expand_path(cls, value: str) -> str:
        return (_ROOT_DIR / cls._DIR_NAME / value).resolve(strict=True).as_posix()


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', frozen=True)

    API_TOKEN: SecretStr
    audio_files: _AudioFiles = _AudioFiles()


settings = _Settings()  # type: ignore[call-arg]
