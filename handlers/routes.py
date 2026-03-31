from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.methods.answer_callback_query import AnswerCallbackQuery
from forms.user import Form
from aiogram.fsm.context import FSMContext
import handlers.keyboards as kb
import db

router = Router()
'''
@router.message(Command("start"))
async def cmd_start(message: Message):
    await db.add_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "👋 Привет! Я бот для отслеживания здоровья.\n\n"
        "📝 Команды:\n"
        "/weight 65.5 — записать вес\n"
        "/pressure 120 80 70— записать давление и пульс\n"
        "/myweight — история веса\n"
        "/mypressure — история давления\n"
        "/stats — статистика",
        reply_markup=kb.get_basic_reply_keyboard()
    )
@router.callback_query(F.data == 'basic_page')
@router.message(F.text=="На главную")
async def basic(message: Message, state: FSMContext, callback_query: CallbackQuery):
    await message.answer(
        "Выбери, что хочешь сделать",
    parse_mode="Markdown",
    reply_markup=kb.get_basic_reply_keyboard())
    await callback_query.AnswerCallbackQuery("Выбери, что хочешь сделать", reply_markup=kb.get_basic_reply_keyboard())
    await state.clear()




@router.message(Command("weight"))
async def cmd_weight(message: Message):
    try:
        # Парсим вес из сообщения: /weight 65.5
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer("❌ Используйте: /weight 65.5")
            return

        weight = float(parts[1])

        # Проверка на адекватность
        if weight < 20 or weight > 300:
            await message.answer("❌ Пожалуйста, введите реалистичный вес (20-300 кг)")
            return

        # Записываем в базу
        await db.add_weight(message.from_user.id, weight)

        await message.answer(f"✅ Записал вес: {weight} кг")

    except ValueError:
        await message.answer("❌ Вес должен быть числом (например, 65.5)")


@router.message(Command("myweight"))
async def cmd_myweight(message: Message):
    history = await db.get_weight_history(message.from_user.id, limit=5)

    if not history:
        await message.answer("📭 Нет записей о весе.\nИспользуйте /weight 65.5")
        return

    text = "📊 Ваш вес:\n\n"
    for record in reversed(history):
        date = record['recorded_at'].strftime('%d.%m %H:%M')
        weight = record['weight']
        note = f" ({record['note']})" if record['note'] else ""
        text += f"• {date}: {weight} кг{note}\n"

    await message.answer(text)


@router.message(Command("deleteweight"))
async def cmd_deleteweight(message: types.Message):
    # Пока просто заглушка - можно добавить позже
    await message.answer("🗑 Функция удаления в разработке")



'''



'''@router.message(Command("start"))
async def hello(message: Message, state: FSMContext):
    await message.answer(
        "hello",
    parse_mode="Markdown",
    reply_markup=kb.get_main_reply_keyboard())
    await state.clear()

@router.message(F.text=="На главную")
async def basic(message: Message):
    await message.answer(
        "Выбери, что хочешь сделать",
    parse_mode="Markdown",
    reply_markup=kb.get_basic_reply_keyboard())

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
    await message.answer("Отлично! Введите ваш пол", reply_markup=kb.get_gender_inline_keyboard())
    await state.set_state(Form.gender)

@router.callback_query(F.data == 'man')
@router.callback_query(F.data== 'woman')
async def process_gender(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    data = await state.get_data()
    name = data["name"]
    age = data["age"]
    gender = data["gender"]
    await state.clear()
    await callback.message.answer(f"Отлично! Ваше имя : {name}, ваш возраст: {age}, ваш пол: {gender}")'''

