import asyncio
from aiohttp_socks import ProxyConnector
from aiohttp import ClientSession
from config import PROXY_URL


async def test_proxy():
    print(f"🔍 Тестируем прокси: {PROXY_URL}\n")

    try:
        # Создаем коннектор
        connector = ProxyConnector.from_url(PROXY_URL)

        # Пробуем подключиться к Telegram
        async with ClientSession(connector=connector) as session:
            print("⏳ Подключение к Telegram...")
            async with session.get("https://api.telegram.org", timeout=15) as resp:
                print(f"✅ Прокси работает!")
                print(f"   Статус ответа: {resp.status}")
                print(f"   Можно использовать в боте!")
                return True

    except asyncio.TimeoutError:
        print("❌ Таймаут подключения")
        print("   Прокси не отвечает или слишком медленный")
    except Exception as e:
        error_msg = str(e)
        if "IncompleteReadError" in error_msg:
            print("❌ Ошибка рукопожатия")
            print("   Неверный логин/пароль или прокси требует другой формат")
        elif "Authentication failed" in error_msg or "auth" in error_msg.lower():
            print("❌ Ошибка авторизации")
            print("   Неверный логин или пароль")
        elif "Connection refused" in error_msg:
            print("❌ Соединение отклонено")
            print("   Прокси не работает или порт закрыт")
        elif "timed out" in error_msg.lower():
            print("❌ Превышено время ожидания")
            print("   Прокси не отвечает")
        else:
            print(f"❌ Ошибка: {type(e).__name__}")
            print(f"   {error_msg[:100]}")

    return False


# Запуск теста
if __name__ == "__main__":
    success = asyncio.run(test_proxy())

    if success:
        print("\n" + "=" * 50)
        print("🎉 ПРОКСИ РАБОЧАЯ!")
        print("=" * 50)
        print(f"📋 Добавьте в .env:")
        print(f"   PROXY_URL={PROXY_URL}")
        print("\nТеперь можно запускать бота!")
    else:
        print("\n" + "=" * 50)
        print("❌ ПРОКСИ НЕ РАБОТАЕТ")
        print("=" * 50)
        print("💡 Что делать:")
        print("   1. Проверьте ссылку на опечатки")
        print("   2. Убедитесь, что добавили свой IP в белый список")
        print("   3. Попробуйте другой прокси")
