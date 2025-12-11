from pathlib import Path
from typing import ClassVar, Final

from pydantic import SecretStr, BaseModel, field_validator, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


_ROOT_DIR: Final[Path] = Path(__file__).parent.parent.parent
_DEBUG: Final[bool] = False


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
    DEBUG: bool = _DEBUG
    LOG_DIR: Path = _ROOT_DIR / 'logs'


settings = _Settings()  # type: ignore[call-arg]
