from fastapi import APIRouter

from .post import router as post_router
from .user import router as user_router

main_router = APIRouter()

main_router.include_router(
    post_router, prefix='/posts', tags=['Посты'])

main_router.include_router(user_router)
