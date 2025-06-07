from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def main_inline_kb(posts_response) -> InlineKeyboardMarkup:
    """Инлайн клавиатура в главном меню."""
    posts = posts_response.get('items')
    page = posts_response.get('page')
    pages = posts_response.get('pages')
    inline_kb_list = [
        [InlineKeyboardButton(text=post['title'], callback_data=f'post_{post["id"]}')]
        for post in posts
    ]
    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(text="◀️ Назад", callback_data=f"page_{page - 1}")
        )
    if page < pages:
        nav_buttons.append(
            InlineKeyboardButton(text="Вперёд ▶️", callback_data=f"page_{page + 1}")
        )
    if nav_buttons:
        inline_kb_list.append(nav_buttons)
    inline_kb_list.append(
        [InlineKeyboardButton(text='🔁 Обновить список постов',
                              callback_data='back_post')]
        )
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def post_inline_kb() -> InlineKeyboardMarkup:
    """Инлайн клавиатура в описании поста."""
    inline_kb_list = [
        [InlineKeyboardButton(text='🔙 Вернуться к списку блогов',
                              callback_data='back_post')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
