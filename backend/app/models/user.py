from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.post import Post


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель для пользователей."""

    posts: Mapped[list['Post']] = relationship('Post', back_populates='user')
