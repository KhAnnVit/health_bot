from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from forms.user import Form
from aiogram.fsm.context import FSMContext

router = Router()






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



@router.message(Command("start"))
async def hello(message: Message, state: FSMContext):
    await message.answer(
        "hello",
    parse_mode="Markdown",
    reply_markup=get_main_reply_keyboard())

@router.message(F.text=="На главную")
async def basic(message: Message):
    await message.answer(
        "Выбери, что хочешь сделать",
    parse_mode="Markdown",
    reply_markup=get_basic_reply_keyboard())

@router.message(F.text=="Регистрация")
async def basic(message: Message, state: FSMContext):
    await message.answer(
        "Давай сначала заполним анкету. Введите имя:",
    parse_mode="Markdown")
    await state.set_state(Form.name)

@router.message(Form.name, F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отлично! Введите ваш возраст")
    await state.set_state(Form.age)


@router.message(Form.age, F.text)
async def process_name(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Отлично! Введите ваш пол")
    await state.set_state(Form.gender)


@router.message(Form.gender, F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Отлично! Введите ваш пол")
    data = await state.get_data()
    name = data["name"]
    age = data["age"]
    gender = data["gender"]
    await state.clear()