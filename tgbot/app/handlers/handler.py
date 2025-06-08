from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from app.core.config import settings
from app.keyboards.inline import main_inline_kb, post_inline_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    return await cmd_posts(message)


@router.callback_query(F.data == 'back_post')
async def callback_posts(callback: CallbackQuery):
    return await cmd_posts(callback.message)


@router.message(Command('posts'))
async def cmd_posts(message: Message):
    url = f'{settings.get_backend_url}{settings.POST_PATH}'
    async with message.bot.backend_session.get(url) as resp:
        posts = await resp.json()
    await message.delete()
    await message.answer(
        'Выбери пост, который хочешь почитать:',
        reply_markup=main_inline_kb(posts))


@router.callback_query(F.data.startswith('page_'))
async def paginate_posts(callback: CallbackQuery):
    page = int(callback.data.split('_')[1])
    url = (f'{settings.get_backend_url}{settings.POST_PATH}'
           f'?page={page}&size={settings.SIZE_PAGINATION}')
    async with callback.bot.backend_session.get(url) as resp:
        posts = await resp.json()
    await callback.message.delete()
    await callback.message.answer(
        'Выбери пост, который хочешь почитать:',
        reply_markup=main_inline_kb(posts)
    )


@router.callback_query(F.data.startswith('post_'))
async def show_post(callback: CallbackQuery):
    post_id = int(callback.data.split('_')[1])
    url = f'{settings.get_backend_url}{settings.POST_PATH}/{post_id}'
    async with callback.bot.backend_session.get(url) as resp:
        if resp.status == 404:
            await callback.answer('Пост был удален администратором')
            return await cmd_posts(callback.message)
        post = await resp.json()
    parsed_date = datetime.fromisoformat(post['created_at'])
    formatted_date = parsed_date.strftime('%d.%m.%Y %H:%M')
    text = (f'📝 <b>{post['title']}</b>\n\n'
            f'{post['text']}\n\n'
            f'📅 {formatted_date}')
    await callback.message.delete()
    await callback.message.answer(text,
                                  parse_mode='HTML',
                                  reply_markup=post_inline_kb())
