from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import db
import handlers.keyboards as kb
from forms.user import sets
from aiogram.fsm.context import FSMContext

router = Router()



'''


@router.message(F.text=="Записать давление")
async def set_weight(message: Message, state: FSMContext):
    await message.answer(
        "Запиши своё давление и пульс через пробел. Например: 120 60 80",
    parse_mode="Markdown", reply_markup=kb.get_basic_reply_keyboard())
    await state.set_state(sets.set_pressure)

@router.message(sets.set_pressure, F.text)
async def process_name(message: Message, state: FSMContext):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            await message.answer("❌ Используйте: 120 80 [пульс]")
            return

        systolic = int(parts[0])  # Верхнее
        diastolic = int(parts[1])  # Нижнее
        pulse = int(parts[2]) if len(parts) > 2 else None

        # Проверка на адекватность
        if systolic < 50 or systolic > 250:
            await message.answer("❌ Некорректное верхнее давление")
            return
        if diastolic < 30 or diastolic > 150:
            await message.answer("❌ Некорректное нижнее давление")
            return

        await db.add_pressure(message.from_user.id, systolic, diastolic, pulse)

        pulse_text = f", пульс {pulse}" if pulse else ""
        await message.answer(f"✅ Записал давление: {systolic}/{diastolic}{pulse_text}", reply_markup=kb.get_start_inline_keyboard())
        await state.clear()

    except ValueError:
        await message.answer("❌ Давление должно быть числами (например, 120 80)")







@router.message(Command("pressure"))
async def cmd_pressure(message: Message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            await message.answer("❌ Используйте: /pressure 120 80 [пульс]")
            return

        systolic = int(parts[1])  # Верхнее
        diastolic = int(parts[2])  # Нижнее
        pulse = int(parts[3]) if len(parts) > 3 else None

        # Проверка на адекватность
        if systolic < 50 or systolic > 250:
            await message.answer("❌ Некорректное верхнее давление")
            return
        if diastolic < 30 or diastolic > 150:
            await message.answer("❌ Некорректное нижнее давление")
            return

        await db.add_pressure(message.from_user.id, systolic, diastolic, pulse)

        pulse_text = f", пульс {pulse}" if pulse else ""
        await message.answer(f"✅ Записал давление: {systolic}/{diastolic}{pulse_text}")

    except ValueError:
        await message.answer("❌ Давление должно быть числами (например, 120 80)")

@router.message(F.text=="Моё давление")
@router.message(Command("mypressure"))
async def cmd_mypressure(message: types.Message):
    history = await db.get_pressure_history(message.from_user.id, limit=5)

    if not history:
        await message.answer("📭 Нет записей о давлении.\nИспользуйте /pressure 120 80")
        return

    text = "📊 Ваше давление:\n\n"
    for record in reversed(history):
        date = record['recorded_at'].strftime('%d.%m %H:%M')
        systolic = record['systolic']
        diastolic = record['diastolic']
        pulse = f", пульс {record['pulse']}" if record['pulse'] else ""
        note = f" ({record['note']})" if record['note'] else ""
        text += f"• {date}: {systolic}/{diastolic}{pulse}{note}\n"

    await message.answer(text)

'''