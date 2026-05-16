# handlers/profile.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import db
from forms.user import ProfileStates
import handlers.keyboards as kb

router = Router()


def format_profile(data: dict) -> str:
    """Форматирует профиль для отправки"""
    name = data.get('full_name') or "❓ Не указано"
    gender = {"m": "Мужской", "f": "Женский"}.get(data.get('gender'), "❓ Не указано")
    age = data.get('age') or "❓"
    height = f"{data['height_cm']} см" if data.get('height_cm') else "❓"
    current = f"{data['current_weight']} кг" if data.get('current_weight') else "❓ Нет записей"
    target = f"{data['target_weight_kg']} кг" if data.get('target_weight_kg') else "❓"

    return (
        f"👤 <b>Профиль</b>\n\n"
        f"📝 Имя: <code>{name}</code>\n"
        f"🚻 Пол: <code>{gender}</code>\n"
        f"📅 Возраст: <code>{age}</code>\n"
        f"📏 Рост: <code>{height}</code>\n"
        f"⚖️ Текущий вес: <code>{current}</code>\n"
        f"🎯 Цель: <code>{target}</code>"
    )
@router.message(F.text == "Заполнить профиль")
@router.message(F.text == "Назад в профиль")
@router.message(F.text == "Мой профиль")
@router.callback_query(F.data == "edit_profile")
async def show_profile(event: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    profile = await db.get_profile(event.from_user.id)

    if not profile:
        text = "⚠️ Профиль не найден. Нажми /start"
        markup = None
    else:
        text = format_profile(profile)
        markup = kb.get_profile_keyboard()

    # 🔑 Разделяем обработку CallbackQuery и Message
    if isinstance(event, CallbackQuery):
        await event.message.answer(text, reply_markup=markup)  # Отправка в чат
        await event.answer()                                   # Убирает "часики" загрузки на кнопке
    else:
        await event.answer(text, reply_markup=markup)


# ─── Callbacks на редактирование ───
@router.callback_query(F.data.startswith("edit:"))
async def start_edit(callback: CallbackQuery, state: FSMContext):
    field = callback.data.split(":")[1]
    if field == "gender":
        await state.set_state(ProfileStates.waiting_for_gender)
        # Отправляем клавиатуру вместо просьбы ввести текст
        await callback.message.answer("✏️ Выберите ваш пол:", reply_markup=kb.get_gender_keyboard())
        await callback.answer()
        return
    field_map = {
        "name": ("Имя", ProfileStates.waiting_for_name),
        "age": ("Возраст (лет)", ProfileStates.waiting_for_age),
        "height": ("Рост (см)", ProfileStates.waiting_for_height),
        "target": ("Цель по весу (кг)", ProfileStates.waiting_for_target),
    }
    label, st = field_map[field]
    await state.set_state(st)
    await callback.message.answer(f"✏️ Введите новое значение для поля <b>{label}</b>:")
    await callback.answer()


# ─── Обработчики ввода ───
async def save_and_return(message: Message, state: FSMContext, field: str, value):
    try:
        await db.update_profile_field(message.from_user.id, field, value)
        await state.clear()
        # Перенаправляем обратно на профиль
        await show_profile(message, state)
    except Exception as e:
        await state.clear()
        await message.answer(f"⚠️ Ошибка сохранения: {e}")


@router.message(ProfileStates.waiting_for_name)
async def edit_name(message: Message, state: FSMContext):
    await save_and_return(message, state, "full_name", message.text.strip()[:50])


@router.message(ProfileStates.waiting_for_gender, F.text == "Назад в профиль")
async def gender_back(message: Message, state: FSMContext):
    await state.clear()
    await show_profile(message, state)


@router.message(ProfileStates.waiting_for_gender, F.text.in_(["Мужчина", "Женщина"]))
async def process_gender_selection(message: Message, state: FSMContext):
    gender_code = "m" if message.text == "Мужчина" else "f"
    await save_and_return(message, state, "gender", gender_code)

# ✅ 2. Фолбэк: если пользователь всё же написал текст вручную
@router.message(ProfileStates.waiting_for_gender)
async def gender_wrong_input(message: Message):
    await message.answer(
        "⚠️ Пожалуйста, используйте кнопки ниже:",
        reply_markup=kb.get_gender_keyboard()
    )


@router.message(ProfileStates.waiting_for_age)
async def edit_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if not (10 <= age <= 120): raise ValueError
        await save_and_return(message, state, "age", age)
    except ValueError:
        await message.answer("⚠️ Введите возраст от 10 до 120 лет")


@router.message(ProfileStates.waiting_for_height)
async def edit_height(message: Message, state: FSMContext):
    try:
        h = float(message.text.replace(",", "."))
        if not (100 <= h <= 250): raise ValueError
        await save_and_return(message, state, "height_cm", h)
    except ValueError:
        await message.answer("⚠️ Введите рост от 100 до 250 см")


@router.message(ProfileStates.waiting_for_target)
async def edit_target(message: Message, state: FSMContext):
    try:
        w = float(message.text.replace(",", "."))
        if not (30 <= w <= 300): raise ValueError
        await save_and_return(message, state, "target_weight_kg", w)
    except ValueError:
        await message.answer("⚠️ Введите вес от 30 до 300 кг")