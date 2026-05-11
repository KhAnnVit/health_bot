from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import handlers.keyboards as kb
import db

router = Router()


# обработка команды start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await db.upsert_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "👋 Привет! Я бот для отслеживания здоровья.\n\n" "Выбери, что хочешь сделать",
        reply_markup=kb.get_main_reply_keyboard(),
    )


# Возврат к главному меню
@router.callback_query(F.data == "go_to_basic_menu")
async def basic(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(
        "Выбери, что хочешь сделать", reply_markup=kb.get_main_reply_keyboard()
    )
    await state.clear()
