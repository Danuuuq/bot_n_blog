from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.core.variables import SettingFieldDB

if TYPE_CHECKING:
    from app.models.user import User


class Post(Base):
    """Модель для постов."""

    title: Mapped[str] = mapped_column(
        String(SettingFieldDB.MAX_LENGTH_TITLE),
        unique=True,
        nullable=False,
    )
    text: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'),
        nullable=False,
    )
    user: Mapped['User'] = relationship(
        'User',
        back_populates='posts',
        lazy='joined',
    )
