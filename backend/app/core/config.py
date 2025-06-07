import os

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс для базовых настроек приложения."""

    APP_TITLE: str = 'Backend для взаимодействия с постами'
    APP_DESCRIPTION: str = (
        'Реализация бизнес-логики для ТГ-бота blog-n-bot')
    BACKEND_HOST: str
    BACKEND_PORT: int
    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SECRET: str = 'default_secret'
    LIFETIME_JWT_TOKEN: int = 3600
    GT_FOR_AMOUNT: int = 0
    GT_FOR_PASSWORD: int = 3

    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        extra='ignore')

    @property
    def get_db_url(self) -> str:
        """Ссылка для подключения к базе данных."""
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:'
                f'{self.POSTGRES_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}')


try:
    settings = Settings()
except ValidationError as error:
    missing_vars = [err["loc"][0] for err in error.errors()]
    raise EnvironmentError(
        f'Отсутствуют переменные окружения: {", ".join(missing_vars)}')
