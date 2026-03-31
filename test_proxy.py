import asyncio
from aiohttp_socks import ProxyConnector
from aiohttp import ClientSession
from config import PROXY_URL


async def test_proxy():
    # ВАРИАНТ 1: Без логина (самый частый)
    # Формат: socks5://:PASSWORD@IP:PORT

    print(f"🔍 Тестируем прокси: {PROXY_URL}")

    try:
        connector = ProxyConnector.from_url(PROXY_URL)
        async with ClientSession(connector=connector) as session:
            async with session.get("https://api.telegram.org", timeout=15) as resp:
                print(f"✅ Прокси работает! Статус: {resp.status}")
                return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("💡 Попробуйте Вариант 2 (логин = пароль)")
        return False


asyncio.run(test_proxy())