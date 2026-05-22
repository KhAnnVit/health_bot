from config import BOT_TOKEN, PROXY_URL
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
import logging

from handlers import routes, weight, pressure, stats, profile, errors
from handlers.calculators import bmi, water
import db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# Подключаем роутеры
dp = Dispatcher()
dp.include_router(routes.router)
dp.include_router(weight.router)
dp.include_router(pressure.router)
dp.include_router(stats.router)
dp.include_router(profile.router)
dp.include_router(bmi.router)
dp.include_router(water.router)
dp.include_router(errors.router)


async def main():
    # 1. Инициализация БД
    await db.init_db()
    logger.info("🗄️ База данных подключена")

    # 2. Создание HTTP-сессии с прокси
    session = AiohttpSession(proxy=PROXY_URL)

    # 3. Создание бота
    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    logger.info("🤖 Бот запущен!")

    try:
        # Запуск polling
        await dp.start_polling(bot)

    except (KeyboardInterrupt, SystemExit, asyncio.CancelledError):
        logger.info("👋 Получен сигнал остановки...")

    finally:
        await db.close_db()
        logger.info("🔌 Пул соединений закрыт")
        await bot.session.close()
        await bot.close()
        logger.info("✅ Бот корректно завершил работу.")


if __name__ == "__main__":
    asyncio.run(main())