from aiogram import Router, types
from aiogram.filters import Command
import db

router = Router()

@router.message(F.text=="Моя статистика")
@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    weight_stats = await db.get_weight_stats(message.from_user.id)
    pressure_stats = await db.get_pressure_stats(message.from_user.id)

    text = "📈 Статистика:\n\n"

    if weight_stats and weight_stats.get('total_records', 0) > 0:
        text += "⚖️ Вес:\n"
        text += f"  • Записей: {weight_stats['total_records']}\n"
        text += f"  • Мин: {weight_stats['min_weight']} кг\n"
        text += f"  • Макс: {weight_stats['max_weight']} кг\n"
        text += f"  • Средний: {weight_stats['avg_weight']:.1f} кг\n\n"
    else:
        text += "⚖️ Вес: нет данных\n\n"

    if pressure_stats and pressure_stats.get('total_records', 0) > 0:
        text += "💓 Давление:\n"
        text += f"  • Записей: {pressure_stats['total_records']}\n"
        text += f"  • Верхнее: {pressure_stats['min_systolic']}-{pressure_stats['max_systolic']}\n"
        text += f"  • Нижнее: {pressure_stats['min_diastolic']} - {pressure_stats['max_diastolic']}\n"
    else:
        text += "💓 Давление: нет данных\n"

    await message.answer(text)