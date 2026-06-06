from aiogram import Router, F
from aiogram.types import Message
import db
import handlers.keyboards as kb

router = Router()

#функция для расчёта нормы воды
def calculate_water_norm(weight_kg: float) -> float:
    base = weight_kg * 0.03  # 30 мл/кг
    return round(base, 1)

#расчёт
@router.message(F.text == "Калькулятор нормы воды")
async def calc_water(message: Message):
    profile = await db.get_profile(message.from_user.id)

    #на случай если не получится вытянуть данные из профиля
    if not profile or not profile.get('current_weight'):
        await message.answer(
            "⚠️ В профиле не указан текущий вес.\nВведите его вручную или обновите профиль.",
            reply_markup=kb.get_skip_inline_keyboard()
        )
        return
    else:
        try:
            # asyncpg может вернуть Decimal, float() безопасно конвертирует
            weight = float(profile['current_weight'])
            norm = calculate_water_norm(weight)
            text = (
                f" <b>Ваша норма воды:</b>\n"
                f"• Вес: <code>{weight} кг</code>\n"
                f"• Рекомендация: <code>{norm} л/день</code>\n\n"
                f"<i>Формула: вес × 30 мл (базовая потребность)</i>\n"
                f"При высокой активности или жаре увеличьте объём.\n"
                f"🩺 Пейте равномерно в течение дня. При заболеваниях почек проконсультируйтесь с врачом."
            )
            kb_markup = kb.get_skip_inline_keyboard()
        except (ValueError, TypeError):
            text = "⚠️ Не удалось рассчитать. Проверьте данные в профиле."
            kb_markup = kb.get_skip_inline_keyboard()
    await message.answer(text, reply_markup=kb_markup)