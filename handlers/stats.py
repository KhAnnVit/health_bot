from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.methods.answer_callback_query import AnswerCallbackQuery
import db
from utils import charts
from aiogram.types import FSInputFile
import handlers.keyboards as kb



router = Router()

@router.callback_query(F.data == 'weight_chart')
async def cmd_weightchart(callback_query: CallbackQuery):
    await callback_query.answer()
    chart_file = await charts.generate_weight_chart(callback_query.from_user.id)

    if not chart_file:
        await callback_query.message.answer("📭 Нет данных для графика")
        return

    await callback_query.message.answer_photo(
        photo=FSInputFile(chart_file),
        caption="📊 Ваш график веса"
    )

'''
@router.callback_query(F.data == 'basic_page')
@router.message(F.text=="На главную")
async def basic(message: Message, state: FSMContext, callback_query: CallbackQuery):
    await message.answer(
        "Выбери, что хочешь сделать",
    parse_mode="Markdown",
    reply_markup=kb.get_basic_reply_keyboard())
    await callback_query.AnswerCallbackQuery("Выбери, что хочешь сделать", reply_markup=kb.get_basic_reply_keyboard())
    await state.clear()'''
@router.callback_query(F.data == 'pressure_chart')
@router.message(Command("pressurechart"))
async def cmd_pressurechart(callback_query: CallbackQuery):
    await callback_query.answer()
    chart_file = await charts.generate_pressure_chart(callback_query.message.from_user.id)

    if not chart_file:
        await callback_query.message.answer("📭 Нет данных для графика", reply_markup=kb.get_skip_inline_keyboard())
        return

    await callback_query.message.answer_photo(
        photo=FSInputFile(chart_file),
        caption="💓 Ваш график давления")
    await callback_query.message.answer(reply_markup=kb.get_skip_inline_keyboard())








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