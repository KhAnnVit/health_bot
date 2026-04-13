from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#основная клавиатура
def get_main_reply_keyboard():
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

#клавиатура для возврата к основной клавиатуре
def get_skip_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Вернуться на главную', callback_data='go_to_basic_menu')],
        ]
    )
    return keyboard

#клавиатура для просмотра веса
def get_myweight_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='График веса', callback_data='weight_chart')],
            [InlineKeyboardButton(text='Отчёт для врача', callback_data='weight_report')],
            [InlineKeyboardButton(text='На главную', callback_data='go_to_basic_menu')]
        ]
    )
    return keyboard

#клавиатура для просмотра давления
def get_mypressure_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='График давления', callback_data='pressure_chart')],
            [InlineKeyboardButton(text='Отчёт для врача', callback_data='pressure_report')],
            [InlineKeyboardButton(text='На главную', callback_data='go_to_basic_menu')]
        ]
    )
    return keyboard
