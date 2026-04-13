from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.methods.answer_callback_query import AnswerCallbackQuery
import db
from utils import charts
from aiogram.types import FSInputFile, BufferedInputFile
import handlers.keyboards as kb
from utils import reports as report
from datetime import datetime

router = Router()

@router.callback_query(F.data == 'weight_chart')
async def cmd_weightchart(callback_query: CallbackQuery):
    await callback_query.answer()

    chart_buffer = await charts.generate_weight_chart_bytes(
        callback_query.from_user.id
    )

    if not chart_buffer:
        await callback_query.message.answer(
            "📭 Нет данных для графика",
            reply_markup=kb.get_skip_inline_keyboard()
        )
        return

    await callback_query.message.answer_photo(
        photo=BufferedInputFile(
            file=chart_buffer.getvalue(),
            filename="weight.png"
        ),
        caption="📊 Ваш вес (последние записи)",
        reply_markup=kb.get_skip_inline_keyboard()
    )




@router.callback_query(F.data == 'pressure_chart')
async def cmd_pressurechart(callback_query: CallbackQuery):
    await callback_query.answer()

    chart_buffer = await charts.generate_pressure_chart_bytes(
        callback_query.from_user.id
    )

    if not chart_buffer:
        await callback_query.message.answer(
            "📭 Нет данных для графика",
            reply_markup=kb.get_skip_inline_keyboard()
        )
        return

    await callback_query.message.answer_photo(
        photo=BufferedInputFile(
            file=chart_buffer.getvalue(),
            filename="pressure.png"
        ),
        caption="💓 Ваше давление (верхнее / нижнее)",
        reply_markup=kb.get_skip_inline_keyboard()
    )


@router.message(F.text=="Моя статистика")
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


# Отчёт по весу
@router.callback_query(F.data == 'weight_report')
async def cmd_download_weight_report(callback_query: CallbackQuery):
    await callback_query.answer()

    report_buffer = await report.generate_weight_report(
        callback_query.from_user.id
    )

    if not report_buffer:
        await callback_query.message.answer(
            "📭 Нет данных для отчёта по весу.\n\nДобавьте хотя бы одну запись: /weight 70.5",
            reply_markup=kb.get_skip_inline_keyboard()
        )
        return

    await callback_query.message.answer_document(
        document=BufferedInputFile(
            file=report_buffer.getvalue(),
            filename=f"weight_report_{datetime.now().strftime('%Y%m%d')}.pdf"
        ),
        caption="⚖️ Отчёт по весу для врача\n\nВключает:\n• Средний, мин, макс вес\n• Изменение за период\n• Полную историю записей",
        reply_markup=kb.get_skip_inline_keyboard()
    )


# Отчёт по давлению
@router.callback_query(F.data == 'pressure_report')
async def cmd_download_pressure_report(callback_query: CallbackQuery):
    await callback_query.answer()

    report_buffer = await report.generate_pressure_report(
        callback_query.from_user.id
    )

    if not report_buffer:
        await callback_query.message.answer(
            "📭 Нет данных для отчёта по давлению.\n\nДобавьте хотя бы одну запись: /pressure 120 80 75",
            reply_markup=kb.get_skip_inline_keyboard()
        )
        return

    await callback_query.message.answer_document(
        document=BufferedInputFile(
            file=report_buffer.getvalue(),
            filename=f"pressure_report_{datetime.now().strftime('%Y%m%d')}.pdf"
        ),
        caption="💓 Отчёт по давлению и пульсу для врача\n\nВключает:\n• Среднее, мин, макс давление\n• Статистику по пульсу\n• Полную историю записей",
        reply_markup=kb.get_skip_inline_keyboard()
    )