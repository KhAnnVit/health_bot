# Health Tracker Bot

Телеграм-бот для отслеживания веса, давления и пульса с визуализацией и PDF-отчётами.

---

## Возможности

*   📊 Графики веса и давления
*   📄 PDF-отчёты для врача
*   💾 Хранение истории в PostgreSQL
*   🔒 Поддержка прокси

---

## Стек

Python • aiogram • pandas • matplotlib • seaborn • reportlab • PostgreSQL • asyncpg

---

## Запуск

```bash
git clone https://github.com/KhAnnVit/health-bot.git
cd health-bot
pip install -r requirements.txt

# Настроить .env
notepad .env

python main.py
```

### 🔧 Настройка .env

```env
BOT_TOKEN=ваш_токен_от_botfather
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/health_bot
PROXY_URL=socks5://user:pass@host:port  # опционально
```

---

## 📸 Скриншоты

![Main Menu](images/main_menu.jpg)
![Chart](images/chart.jpg)
![Report](images/report.jpg)

---
