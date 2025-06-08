from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault

from app.core.config import settings
from app.handlers.handler import router

bot = Bot(token=settings.TOKEN_TG, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))


dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


async def set_commands():
    """Добавление команд для взаимодействия с ботом"""
    commands = [BotCommand(command='start', description='Перезапустить бота'),
                BotCommand(command='posts ', description='Все посты')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
