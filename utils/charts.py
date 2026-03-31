import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import db


async def generate_weight_chart(telegram_id):
    history = await db.get_weight_history(telegram_id, limit=30)

    if not history:
        return None

    # Подготовка данных
    dates = [record['recorded_at'] for record in reversed(history)]
    weights = [float(record['weight']) for record in reversed(history)]

    # Создание графика
    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights, marker='o', linewidth=2, color='#6c5ce7')
    plt.title('📊 Динамика веса', fontsize=14)
    plt.xlabel('Дата')
    plt.ylabel('кг')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Сохранение
    filename = f'weight_{telegram_id}.png'
    plt.savefig(filename)
    plt.close()

    return filename


async def generate_pressure_chart(telegram_id):
    history = await db.get_pressure_history(telegram_id, limit=30)

    if not history:
        return None

    dates = [record['recorded_at'] for record in reversed(history)]
    systolic = [record['systolic'] for record in reversed(history)]
    diastolic = [record['diastolic'] for record in reversed(history)]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, systolic, marker='o', linewidth=2, color='#e74c3c', label='Верхнее')
    plt.plot(dates, diastolic, marker='s', linewidth=2, color='#3498db', label='Нижнее')
    plt.title('💓 Динамика давления', fontsize=14)
    plt.xlabel('Дата')
    plt.ylabel('мм рт.ст.')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    filename = f'pressure_{telegram_id}.png'
    plt.savefig(filename)
    plt.close()

    return filename
