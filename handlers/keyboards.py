from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


# основная клавиатура
def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Записать вес"),
                KeyboardButton(text="Записать давление"),
            ],
            [KeyboardButton(text="Мой вес"),
             KeyboardButton(text="Моё давление")],
            [KeyboardButton(text="Моя статистика")],
            [KeyboardButton(text="Мой профиль")],
            [KeyboardButton(text="Калькуляторы и тесты")]
        ],
        resize_keyboard=True,
    )
    return keyboard


# клавиатура для возврата к основной клавиатуре
def get_skip_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Вернуться на главную", callback_data="go_to_basic_menu"
                )
            ],
        ]
    )
    return keyboard


# клавиатура для просмотра веса
def get_myweight_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="График веса",
                                  callback_data="weight_chart")],
            [
                InlineKeyboardButton(
                    text="Отчёт для врача", callback_data="weight_report"
                )
            ],
            [InlineKeyboardButton(text="На главную",
                                  callback_data="go_to_basic_menu")],
        ]
    )
    return keyboard


# клавиатура для просмотра давления
def get_mypressure_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="График давления", callback_data="pressure_chart"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отчёт для врача", callback_data="pressure_report"
                )
            ],
            [InlineKeyboardButton(text="На главную",
                                  callback_data="go_to_basic_menu")],
        ]
    )
    return keyboard


def get_profile_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Имя", callback_data="edit:name"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Пол", callback_data="edit:gender"
                )
            ],
            [
                InlineKeyboardButton(
                text="На главную", callback_data="go_to_basic_menu"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Возраст", callback_data="edit:age"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Рост", callback_data="edit:height"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Цель по весу", callback_data="edit:target"
                )
            ],
            [
                InlineKeyboardButton(
                text="🔙 Назад", callback_data="go_to_basic_menu"
             )
             ]
        ]
    )
    return keyboard

def get_gender_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Женщина"),
                KeyboardButton(text="Мужчина"),
            ],
            [KeyboardButton(text="Назад в профиль")]
        ],
        resize_keyboard=True,
    )
    return keyboard

def get_calculators_list_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Калькулятор ИМТ")],
            [KeyboardButton(text="Калькулятор нормы воды")]
        ],
        resize_keyboard=True,
    )
    return keyboard

def get_bmi_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Использовать данные из профиля", callback_data="bmi_from_profile")
            ],
            [
                InlineKeyboardButton(text="Ввести даные вручную", callback_data="bmi_from_input")
            ],
            [
                InlineKeyboardButton(text="Назад к списку", callback_data="go_to_calculators_list")
            ]
        ]
    )
    return keyboard

def get_bmi_wrong_profile_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Заполнить профиль", callback_data="edit_profile")
            ],
            [
                InlineKeyboardButton(text="Ввести даные вручную", callback_data="bmi_from_input")
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="go_to_calculators_list")
            ]
        ]
    )
    return keyboard


