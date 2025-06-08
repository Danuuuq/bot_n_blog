from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс для базовых настроек приложения."""

    TOKEN_TG: str
    BACKEND_HOST: str
    BACKEND_PORT: int
    POST_PATH: str = '/posts'
    SIZE_PAGINATION: int = 5

    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        extra='ignore')

    @property
    def get_backend_url(self) -> str:
        """Ссылка для обращений к backend."""
        return f'http://{self.BACKEND_HOST}:{self.BACKEND_PORT}'


try:
    settings = Settings()
except ValidationError as error:
    missing_vars = [err['loc'][0] for err in error.errors()]
    raise EnvironmentError(
        f'Отсутствуют переменные окружения: {', '.join(missing_vars)}')
