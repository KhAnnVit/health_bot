from aiogram import Router, F
from aiogram.types import Message
import db
import handlers.keyboards as kb
from forms.user import sets
from aiogram.fsm.context import FSMContext

router = Router()

#Просим записать давление
@router.message(F.text=="Записать давление")
async def set_weight(message: Message, state: FSMContext):
    await message.answer(
        "Запиши своё давление и пульс через пробел. Например: 120 60 80",
    parse_mode="Markdown", reply_markup=kb.get_skip_inline_keyboard())
    await state.set_state(sets.set_pressure)

#Записываем давление
@router.message(sets.set_pressure, F.text)
async def process_name(message: Message, state: FSMContext):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            await message.answer("❌ Используйте: 120 80 [пульс]")
            return

        systolic = int(parts[0])  # Верхнее
        diastolic = int(parts[1])  # Нижнее
        pulse = int(parts[2]) # Пульс

        # Проверка на адекватность
        if systolic < 50 or systolic > 250:
            await message.answer("❌ Некорректное верхнее давление")
            return
        if diastolic < 30 or diastolic > 150:
            await message.answer("❌ Некорректное нижнее давление")
            return

        # добавляем в базу данных
        await db.add_pressure(message.from_user.id, systolic, diastolic, pulse)

        pulse_text = f", пульс {pulse}" if pulse else ""
        await message.answer(f"✅ Записал давление: {systolic}/{diastolic}{pulse_text}", reply_markup=kb.get_skip_inline_keyboard())
        await state.clear()

    except ValueError:
        await message.answer("❌ Давление должно быть числами (например, 120 80)")


# Просмотр давления
@router.message(F.text=="Моё давление")
async def mypressure(message: Message):
    history = await db.get_pressure_history(message.from_user.id, limit=5)

    if not history:
        await message.answer("📭 Нет записей о давлении.", reply_markup=kb.get_skip_inline_keyboard())
        return

    text = "📊 Ваше давление:\n\n"
    for record in reversed(history):
        date = record['recorded_at'].strftime('%d.%m %H:%M')
        systolic = record['systolic']
        diastolic = record['diastolic']
        pulse = f", пульс {record['pulse']}" if record['pulse'] else ""
        note = f" ({record['note']})" if record['note'] else ""
        text += f"• {date}: {systolic}/{diastolic}{pulse}{note}\n"

    await message.answer(text, reply_markup=kb.get_mypressure_inline_keyboard())

