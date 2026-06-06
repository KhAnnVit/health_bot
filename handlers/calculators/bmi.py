from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import db
from aiogram.fsm.context import FSMContext
import handlers.keyboards as kb
import utils.messages as msg
from forms.user import BMICalcStates

router = Router()

#функция подсчёта ИМТ
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    if height_m <= 0:
        raise ValueError("Рост должен быть > 0")
    return round(weight_kg / (height_m ** 2), 1)

#функция определения категории ИМТ
def get_bmi_category(bmi: float) -> str:
    if bmi < 18.5: return "🔹 Недостаточный вес"
    if bmi < 25.0: return "✅ Норма"
    if bmi < 30.0: return "🔸 Избыточный вес"
    if bmi < 35.0: return "🔴 Ожирение I степени"
    if bmi < 40.0: return "🔴 Ожирение II степени"
    return "🔴 Ожирение III степени"

#высвечиваем информацию и клавиатуру выборас способа ввода
@router.message(F.text == "Калькулятор ИМТ")
async def bmi(message: Message| CallbackQuery):
    text = msg.BMI_INFO_TEXT
    await message.answer(text , reply_markup=kb.get_bmi_inline_keyboard(), parse_mode='HTML')

#считаем в случае данных из профиля
@router.callback_query(F.data == "bmi_from_profile")
async def bmi_from_profile(callback: CallbackQuery, state: FSMContext):
    profile = await db.get_profile(callback.from_user.id)
    #на случай отсутствия подходящих данных
    if not profile or not profile.get('height_cm') or not profile.get('current_weight'):
        await state.clear()
        await callback.message.answer(
            "⚠️ В профиле не указан рост или текущий вес.\nЗаполните профиль или выберите ручной ввод.",
            reply_markup=kb.get_bmi_wrong_profile_keyboard()
        )
        await callback.answer()
        return

    weight = float(profile['current_weight'])
    height_m = float(profile['height_cm']) / 100
    bmi = calculate_bmi(weight, height_m)
    category = get_bmi_category(bmi)

    text = f"📊 <b>Результат (из профиля):</b>\nИМТ: <code>{bmi}</code> — {category}"

    await callback.message.answer(text, reply_markup=kb.get_skip_inline_keyboard())
    await callback.answer()

#ожидаем вес в случае ручного ввода
@router.callback_query(F.data == "bmi_from_input")
async def bmi_from_input(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BMICalcStates.waiting_for_weight)
    await callback.message.answer("⚖Введите ваш текущий вес (кг):")
    await callback.answer()

#обрабатываем вес и ожидаем рост
@router.message(BMICalcStates.waiting_for_weight)
async def input_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text.replace(",", "."))
        if not (20 <= weight <= 300):
            raise ValueError("Вес вне диапазона 20-300 кг")

        await state.update_data(weight=weight)
        await state.set_state(BMICalcStates.waiting_for_height)
        await message.answer("📏 Теперь введите рост (см):")
    except ValueError:
        await message.answer("⚠️ Введите число от 20 до 300 кг.")

#обрабатываем рост и считаем итоговое значение
@router.message(BMICalcStates.waiting_for_height)
async def input_height(message: Message, state: FSMContext):
    try:
        height_cm = float(message.text.replace(",", "."))
        if not (100 <= height_cm <= 250):
            raise ValueError("Рост вне диапазона 100-250 см")

        # Достаём временный вес
        data = await state.get_data()
        weight = data.get("weight")
        height_m = height_cm / 100

        # Считаем
        bmi = calculate_bmi(weight, height_m)
        category = get_bmi_category(bmi)
        text = f"📊 <b>Результат (ручной ввод):</b>\nИМТ: <code>{bmi}</code> — {category}"

        # Очищаем временные данные
        await state.clear()
        await message.answer(text, reply_markup=kb.get_skip_inline_keyboard())
    #На случай неправильного ввода
    except ValueError:
        await message.answer("⚠️ Введите число от 100 до 250 см.")




