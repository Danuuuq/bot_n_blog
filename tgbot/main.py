import asyncio

from aiohttp import ClientSession

from app.core.bot import bot, dp
from app.core.logger import logger # noqa


async def on_startup():
    bot.backend_session = ClientSession()


async def on_shutdown():
    await bot.session.close()


async def main():
    """Запуск приложения с ботом."""
    await on_startup()
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await on_shutdown()


if __name__ == '__main__':
    asyncio.run(main())
