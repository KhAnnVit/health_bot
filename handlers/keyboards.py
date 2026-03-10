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
            [KeyboardButton(text="Записать вес"),
             KeyboardButton(text="Записать давление")],
            [KeyboardButton(text="Мой вес"),
            KeyboardButton(text="Моё давление")],
            [KeyboardButton(text="Моя статистика")]
        ],
        resize_keyboard=True
    )

    return keyboard

def get_basic_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Записать вес', callback_data='set_weight')]
        ]
    )
    return keyboard


def get_start_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='На главную', callback_data='basic_page')]
        ]
    )
    return keyboard