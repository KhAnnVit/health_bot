from urllib.parse import urlparse, parse_qs, unquote
from config import PROXY_URL

# Ваша ссылка от Telegram
tg_proxy = PROXY_URL

# Парсим URL
parsed = urlparse(tg_proxy)
params = parse_qs(parsed.query)

# Извлекаем данные
server = params["server"][0]
port = params["port"][0]
user = unquote(params.get("user", [None])[0])  # unquote декодирует %20 и т.п.
password = unquote(params.get("pass", [None])[0])

# Формируем строку для aiohttp_socks
if user and password:
    proxy_url = f"socks5://{user}:{password}@{server}:{port}"
else:
    proxy_url = f"socks5://{server}:{port}"

print(f"✅ Готовая ссылка: {proxy_url}")
# Вывод: socks5://myuser:mypass@1.2.3.4:1080
