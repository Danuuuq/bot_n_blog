from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.post import Post


class CRUDPost(CRUDBase):

    async def pagination_all(self, session: AsyncSession) -> Page[Post]:
        """Получить все объекты модели."""
        stmt = select(self.model).order_by(desc(self.model.created_at))
        return await paginate(session, stmt)

    async def get_by_title(
        self,
        title: str,
        session: AsyncSession
    ) -> Post | None:
        """Получение поста по заголовку."""
        object = await session.execute(
            select(self.model).where(
                self.model.title == title
            )
        )
        return object.scalars().first()


post_crud = CRUDPost(Post)
