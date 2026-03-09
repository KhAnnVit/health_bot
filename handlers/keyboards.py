from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_gender_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Мужчина', callback_data='man'), InlineKeyboardButton(text='Женщина', callback_data='woman')],
        ]
    )
    return keyboard



def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Регистрация")],
            [KeyboardButton(text="На главную")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_basic_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Управление весом"),
             KeyboardButton(text="Управление давлением")],
            [KeyboardButton(text="Управление циклом"),
            KeyboardButton(text="Управление питанием")]
        ],
        resize_keyboard=True
    )

    return keyboard