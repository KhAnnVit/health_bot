from config import BOT_TOKEN
import asyncio
from aiogram import Bot, Dispatcher
from handlers import routes, weight, pressure, stats
import db

# Для прокси
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from config import PROXY_URL
from aiogram.client.session.aiohttp import AiohttpSession

#Подключаем модули
dp = Dispatcher()
dp.include_router(routes.router)
dp.include_router(weight.router)
dp.include_router(pressure.router)
dp.include_router(stats.router)

#Функция по запуску бота
async def main():
    await db.init_db()

    # Создаем сессию с параметром proxy
    session = AiohttpSession(proxy=PROXY_URL)

    # Передаем сессию в бота
    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        session_default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    print("🤖 Бот запущен!")
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")
        asyncio.run(db.close_db())