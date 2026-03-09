from config import BOT_TOKEN
import asyncio
from aiogram import Bot, Dispatcher
from handlers.routes import router
import db


TOKEN = BOT_TOKEN

dp = Dispatcher()
dp.include_router(router)


async def main():
    bot = Bot(token=TOKEN)
    await db.init_db()  # ← Инициализация БД
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")
        asyncio.run(db.close_db())