from config import BOT_TOKEN, PROXY_URL
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession

from handlers import routes, weight, pressure, stats, profile
import db

# Подключаем роутеры
dp = Dispatcher()
dp.include_router(routes.router)
dp.include_router(weight.router)
dp.include_router(pressure.router)
dp.include_router(stats.router)
dp.include_router(profile.router)


async def main():
    # 1. Инициализация БД
    await db.init_db()
    print("🗄️ База данных подключена")

    # 2. Создание HTTP-сессии с прокси
    session = AiohttpSession(proxy=PROXY_URL)

    # 3. Создание бота
    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),  # ✅ Исправлено: было session_default
    )

    print("🤖 Бот запущен! Нажмите Ctrl+C для остановки.")

    try:
        # Запуск polling
        await dp.start_polling(bot)

    except (KeyboardInterrupt, SystemExit, asyncio.CancelledError):
        # ✅ Ловим сигналы завершения БЕЗ создания нового event loop
        print("\n👋 Получен сигнал остановки...")

    finally:
        # ✅ Закрываем ресурсы ВНУТРИ текущего event loop
        await db.close_db()
        await bot.session.close()
        await bot.close()
        print("✅ Бот корректно завершил работу.")


if __name__ == "__main__":
    # ✅ asyncio.run() вызывается ТОЛЬКО ОДИН РАЗ в точке входа
    asyncio.run(main())