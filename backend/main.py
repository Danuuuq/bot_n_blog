import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi_pagination import add_pagination
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp

from alembic import command
from alembic.config import Config
from app.api.routers import main_router
from app.core.config import settings
from app.core.log_config import app_logger


app = FastAPI(title=settings.APP_TITLE,
              description=settings.APP_DESCRIPTION,
              )
app.include_router(main_router)
add_pagination(app)

@app.middleware('http')
async def add_logging_context(
        request: Request, call_next: ASGIApp) -> JSONResponse:
    """Добавляет контекст логирования для всех HTTP-запросов."""
    with app_logger.contextualize(
        endpoint=request.url.path,
        method=request.method,
    ):
        return await call_next(request)




def run_migrations() -> None:
    """Применение миграций Alembic перед запуском приложения."""
    alembic_cfg = Config(os.path.join(
                         os.path.dirname(__file__), 'alembic.ini'))
    command.upgrade(alembic_cfg, 'head')


def main() -> None:
    """Функция запуска приложения."""
    run_migrations()
    uvicorn.run('main:app',
                host=settings.BACKEND_HOST,
                port=settings.BACKEND_PORT,
                reload=True)


if __name__ == '__main__':
    main()
