from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.log_config import log_action_status
from app.core.user import current_user
from app.core.pagination import CustomPage
from app.crud.post import post_crud
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostDB
from app.validators.post import check_duplicate_title, get_or_404

router = APIRouter()


@router.get(
    '/',
    response_model=CustomPage[PostDB],
    response_model_exclude_none=True
)
async def get_all_posts(
    session: AsyncSession = Depends(get_async_session),
) -> Page[PostDB]:
    """Возвращает список всех постов."""
    return await post_crud.pagination_all(session)


@router.get(
    '/{post_id}',
    response_model=PostDB,
)
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> PostDB:
    """Возвращает пост по id."""
    return await get_or_404(post_id, session)


@router.post(
    '/',
    dependencies=[Depends(current_user)],
    response_model=PostDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post: PostCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> PostDB:
    """Создание нового поста."""
    await check_duplicate_title(post.title, session)
    log_action_status(
        message=f'Пользователь {user.email} создает пост {post.title}')
    return await post_crud.create(post, session, user)


@router.delete(
    '/{post_id}',
    dependencies=[Depends(current_user)],
    response_model=PostDB,
)
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> PostDB:
    """Удаление поста."""
    post = await get_or_404(post_id, session)
    log_action_status(
        message=f'Пользователь {user.email} удаляет пост {post.title}')
    return await post_crud.delete(post, session)


@router.patch(
    '/{post_id}',
    dependencies=[Depends(current_user)],
    response_model=PostDB,
)
async def update_post(
    post_id: int,
    obj_in: PostUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> PostDB:
    """Редактирование поста."""
    post = await get_or_404(post_id, session)
    if obj_in.title:
        await check_duplicate_title(obj_in.title, session)
    log_action_status(
        message=f'Пользователь {user.email} обновляет пост {post.title}')
    return await post_crud.update(post, obj_in, session)
