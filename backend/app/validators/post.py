from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.post import post_crud
from app.models.post import Post


async def get_or_404(
    obj_id: int,
    session: AsyncSession
) -> Post:
    """Проверка на наличие поста в базе данных."""
    db_obj = await post_crud.get_by_id(obj_id, session)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Публикация с id: {obj_id} отсутствует'
        )
    return db_obj


async def check_duplicate_title(
    post_title: str,
    session: AsyncSession
) -> None:
    """Проверка на уникальность имени проекта.

    Если имя не уникальное возвращается ошибка 422"""
    project = await post_crud.get_by_title(
        post_title, session
    )
    if project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Публикация с таким именем уже существует!'
        )
