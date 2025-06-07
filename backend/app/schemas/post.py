from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    """Базовая схема для постов."""

    title: str | None = Field(default=None, description='Название поста')
    text: str | None = Field(default=None, description='Текст поста')


class PostCreate(PostBase):
    """Cхема для создания постов."""

    title: str = Field(description='Название поста')
    text: str = Field(description='Текст поста')


class PostUpdate(PostBase):
    """Cхема для обновления постов."""
    pass


class PostDB(PostBase):
    """Схема выдачи постов."""
    id: int = Field(description='id публикации')
    created_at: datetime = Field(description='Дата публикации')

    model_config = ConfigDict(from_attributes=True)
