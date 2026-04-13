from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import db
from forms.user import sets
from aiogram.fsm.context import FSMContext
import handlers.keyboards as kb

router = Router()


# обработка запроса на запись веса
@router.message(F.text=="Записать вес")
async def set_weight(message: Message, state: FSMContext):
    await message.answer(
        "Напиши свой вес в кг",
    parse_mode="Markdown", reply_markup=kb.get_skip_inline_keyboard())
    await state.set_state(sets.set_weight)

# Запись веса
@router.message(sets.set_weight, F.text)
async def process_name(message: Message, state: FSMContext):
    try:
        weight = float(message.text)
        if weight < 20 or weight > 300:
            await message.answer("❌ Пожалуйста, введите реалистичный вес (20-300 кг)")
            return
        await db.add_weight(message.from_user.id, weight)
        await message.answer(f"✅ Записал вес: {weight} кг", reply_markup=kb.get_skip_inline_keyboard())
        await state.clear()
    except ValueError:
        await message.answer("❌ Вес должен быть числом (например, 65.5)")


# Просмотр веса
@router.message(F.text=="Мой вес")
async def myweight(message: Message):
    history = await db.get_weight_history(message.from_user.id, limit=5)

    if not history:
        await message.answer("📭 Нет записей о весе.\nИспользуйте /weight 65.5", reply_markup=kb.get_skip_inline_keyboard())
        return

    text = "📊 Ваш вес:\n\n"
    for record in reversed(history):
        date = record['recorded_at'].strftime('%d.%m %H:%M')
        weight = record['weight']
        note = f" ({record['note']})" if record['note'] else ""
        text += f"• {date}: {weight} кг{note}\n"

    await message.answer(text, reply_markup=kb.get_myweight_inline_keyboard())

