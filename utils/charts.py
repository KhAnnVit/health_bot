
import matplotlib.pyplot as plt  # Основная библиотека для рисования
from io import BytesIO  # Чтобы хранить картинку в памяти, а не в файле
import pandas as pd  # Для удобной работы с таблицами данных
import db  # Ваш модуль для работы с базой данных


plt.style.use("seaborn-v0_8-whitegrid")  # Светлая сетка, приятные цвета


async def generate_weight_chart_bytes(telegram_id, limit=30):
    """
    Создаёт простой график веса.

    Args:
        telegram_id: ID пользователя в Telegram
        limit: Сколько последних записей взять (по умолчанию 30)

    Returns:
        BytesIO: Картинка в памяти (или None, если нет данных)
    """

    # --- Получаем данные из базы ---
    # Запрашиваем историю веса у пользователя
    history = await db.get_weight_history(telegram_id, limit=limit)

    # Если записей нет — нечего рисовать, возвращаем None
    if not history:
        return None

    # --- Готовим данные для графика ---
    # Превращаем список записей из БД в таблицу (DataFrame)
    # Это как Excel в коде — очень удобно для графиков
    df = pd.DataFrame([
        {
            "date": record["recorded_at"],  # Дата записи
            "weight": float(record["weight"])  # Вес (число)
        }
        for record in history  # Для каждой записи в истории
    ])

    # Сортируем по дате: от старых к новым (чтобы линия шла слева направо)
    df = df.sort_values("date")

    # --- Рисуем график ---
    # Создаём «холст» (figure) и «ось» (ax), на которой будем рисовать
    fig, ax = plt.subplots()

    # Рисуем линию графика:
    # - data=df: берём данные из нашей таблицы
    # - x="date": по горизонтали будет дата
    # - y="weight": по вертикали будет вес
    # - marker="o": ставим точки на каждом значении
    # - linewidth=2: толщина линии
    # - color="#6c5ce7": красивый фиолетовый цвет (можно менять)
    ax.plot(
        df["date"],
        df["weight"],
        marker="o",  # Кружочки на точках
        linewidth=2.5,  # Толще линия
        markersize=7,  # Крупнее точки
        color="#6c5ce7",  # Красивый фиолетовый
        markerfacecolor="white",  # Белая серединка у точек
        markeredgecolor="#6c5ce7",  # Цвет обводки точек
        markeredgewidth=2,  # Толщина обводки
        label="Вес"
    )

    ax.fill_between(
        df["date"],
        df["weight"],
        alpha=0.15,  # Прозрачность
        color="#6c5ce7"  # Тот же цвет, что у линии
    )
    # --- Настраиваем ось Y: убираем пустое место снизу ---
    min_weight = df["weight"].min()
    max_weight = df["weight"].max()
    range_weight = max_weight - min_weight

    # Если есть хоть какие-то изменения
    if range_weight > 0:
        # Добавляем 20% «воздуха» сверху и снизу, чтобы линия не касалась краёв
        padding = range_weight * 0.2
        ax.set_ylim(min_weight - padding, max_weight + padding)
    else:
        # Если вес не менялся — показываем диапазон ±2 кг от значения
        ax.set_ylim(min_weight - 2, min_weight + 2)

    # --- Подписываем график ---
    # Заголовок сверху (размер 14, жирный)
    ax.set_title("📊 Ваш вес", fontsize=14, fontweight="bold")

    # Подпись оси X (горизонтальная)
    ax.set_xlabel("Дата")

    # Подпись оси Y (вертикальная)
    ax.set_ylabel("кг")

    # --- Делаем даты читаемыми ---
    # Поворачиваем подписи дат на 45 градусов, чтобы не наезжали друг на друга
    plt.xticks(rotation=45, ha="right")

    # --- Добавляем сетку ---
    # alpha=0.3 — прозрачность, чтобы не отвлекала
    ax.grid(True, alpha=0.3)

    # --- Убираем лишние рамки ---
    # Делает график чище и современнее
    ax.spines["top"].set_visible(False)  # Убираем верхнюю рамку
    ax.spines["right"].set_visible(False)  # Убираем правую рамку

    # --- Автоматически подгоняем отступы ---
    # Чтобы подписи и заголовок не обрезались
    plt.tight_layout()

    # --- Сохраняем график в память (не в файл!) ---
    buffer = BytesIO()  # Создаём «виртуальный файл» в оперативной памяти
    # Сохраняем картинку в этот буфер:
    # - format="png": формат изображения
    # - dpi=100: качество (чем больше, тем чётче, но тяжелее файл)
    # - bbox_inches="tight": обрезать лишние пустые поля
    plt.savefig(buffer, format="png", dpi=100, bbox_inches="tight")

    # «Перематываем» буфер в начало, чтобы его можно было прочитать
    buffer.seek(0)

    # Закрываем график, чтобы освободить память
    plt.close(fig)

    return buffer


async def generate_pressure_chart_bytes(telegram_id, limit=30):

    # --- 1. Получаем данные из базы ---
    history = await db.get_pressure_history(telegram_id, limit=limit)

    if not history:
        return None

    # --- 2. Готовим данные для графика ---
    df = pd.DataFrame([
        {
            "date": record["recorded_at"],
            "systolic": record["systolic"],  # Верхнее (красное)
            "diastolic": record["diastolic"]  # Нижнее (синее)
        }
        for record in history
    ])
    df = df.sort_values("date")

    # --- 3. Рисуем график ---
    fig, ax = plt.subplots()

    # 🔴 Верхнее давление (красная линия)
    ax.plot(
        df["date"],
        df["systolic"],
        marker="o",
        linewidth=2,
        markersize=5,
        color="#e74c3c",  # Красный цвет
        label="Верхнее",
        zorder=3  # Рисуем поверх сетки
    )

    # 🔵 Нижнее давление (синяя линия)
    ax.plot(
        df["date"],
        df["diastolic"],
        marker="s",  # Квадратные маркеры (чтобы отличать)
        linewidth=2,
        markersize=5,
        color="#3498db",  # Синий цвет
        label="Нижнее",
        zorder=3
    )

    # --- 4. Подписываем график ---
    ax.set_title("Давление", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Дата", fontsize=10)
    ax.set_ylabel("мм рт.ст.", fontsize=10)

    # --- 5. Форматируем даты ---
    from matplotlib import dates as mdates
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=9)

    # --- 6. Сетка и легенда ---
    ax.grid(True, linestyle="--", alpha=0.4, color="#cccccc")
    ax.legend(frameon=True, fancybox=True, loc="best", fontsize=9)

    # --- 7. Убираем лишние рамки ---
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    # --- 8. Сохраняем в память ---
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    return buffer
'''
import matplotlib.dates as mdates
from datetime import datetime
import db
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so

# utils/charts.py
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import pandas as pd
import database as db


# 🔧 Настройки стиля (выполнить один раз при старте)
def setup_seaborn_style():
    """Настраивает красивый стиль для всех графиков"""
    sns.set_theme(
        style="whitegrid",  # Сетка на белом фоне
        palette="viridis",  # Цветовая палитра
        context="notebook",  # Размер шрифтов
        rc={
            "figure.figsize": (10, 5),
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
            "grid.linestyle": "--",
            "grid.alpha": 0.3,
            "axes.edgecolor": "#e0e0e0",
            "axes.linewidth": 0.5,
        }
    )


# 📈 График веса с трендом
async def generate_weight_chart_bytes(telegram_id, limit=30):
    """Создаёт красивый график веса с линией тренда"""

    history = await db.get_weight_history(telegram_id, limit=limit)

    if not history:
        return None

    # Подготовка данных для pandas
    df = pd.DataFrame([
        {
            "date": record["recorded_at"],
            "weight": float(record["weight"])
        }
        for record in history
    ])
    df = df.sort_values("date")  # Сортируем по дате

    # Настройка стиля
    setup_seaborn_style()

    # Создание графика
    fig, ax = plt.subplots()

    # Основной график (точки + линия)
    sns.lineplot(
        data=df,
        x="date",
        y="weight",
        marker="o",
        linewidth=2.5,
        markersize=6,
        color="#6c5ce7",
        label="Вес",
        ax=ax
    )

    # Линия тренда (скользящее среднее)
    if len(df) >= 3:
        df["trend"] = df["weight"].rolling(window=3, min_periods=1).mean()
        sns.lineplot(
            data=df,
            x="date",
            y="trend",
            linewidth=2,
            color="#fd79a8",
            linestyle="--",
            label="Тренд (3 дня)",
            ax=ax
        )

    # Оформление
    ax.set_title("📊 Динамика веса", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Дата", fontsize=11)
    ax.set_ylabel("кг", fontsize=11)

    # Форматирование дат на оси X
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Легенда и сетка
    ax.legend(frameon=True, fancybox=True, shadow=False)
    ax.grid(True, alpha=0.3)

    # Убираем лишние рамки
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    # Сохранение в память
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    return buffer


# 💓 График давления (два значения + пульс)
async def generate_pressure_chart_bytes(telegram_id, limit=30):
    """Создаёт красивый график давления с пульсом"""

    history = await db.get_pressure_history(telegram_id, limit=limit)

    if not history:
        return None

    # Подготовка данных
    df = pd.DataFrame([
        {
            "date": record["recorded_at"],
            "systolic": record["systolic"],  # Верхнее
            "diastolic": record["diastolic"],  # Нижнее
            "pulse": record["pulse"]
        }
        for record in history
    ])
    df = df.sort_values("date")

    # Настройка стиля
    setup_seaborn_style()

    # Создаём фигуру с двумя осями Y
    fig, ax1 = plt.subplots()

    # Цвета
    color_systolic = "#e74c3c"  # Красный для верхнего
    color_diastolic = "#3498db"  # Синий для нижнего
    color_pulse = "#2ecc71"  # Зелёный для пульса

    # Верхнее давление (левая ось)
    sns.lineplot(
        data=df,
        x="date",
        y="systolic",
        marker="o",
        linewidth=2.5,
        markersize=5,
        color=color_systolic,
        label="Верхнее",
        ax=ax1
    )

    # Нижнее давление (левая ось)
    sns.lineplot(
        data=df,
        x="date",
        y="diastolic",
        marker="s",
        linewidth=2.5,
        markersize=5,
        color=color_diastolic,
        label="Нижнее",
        ax=ax1
    )

    # Пульс (правая ось, если есть данные)
    if df["pulse"].notna().any():
        ax2 = ax1.twinx()
        sns.lineplot(
            data=df,
            x="date",
            y="pulse",
            marker="^",
            linewidth=2,
            markersize=4,
            color=color_pulse,
            label="Пульс",
            ax=ax2,
            linestyle=":"
        )
        ax2.set_ylabel("Пульс (уд/мин)", fontsize=10, color=color_pulse)
        ax2.tick_params(axis="y", labelcolor=color_pulse)

    # Оформление
    ax1.set_title("💓 Динамика давления", fontsize=16, fontweight="bold", pad=15)
    ax1.set_xlabel("Дата", fontsize=11)
    ax1.set_ylabel("мм рт.ст.", fontsize=11)

    # Форматирование дат
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Легенды для обеих осей
    lines1, labels1 = ax1.get_legend_handles_labels()
    if 'ax2' in locals():
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, frameon=True, fancybox=True)
    else:
        ax1.legend(frameon=True, fancybox=True)

    # Сетка и рамки
    ax1.grid(True, alpha=0.3, linestyle="--")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    plt.tight_layout()

    # Сохранение
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    return buffer


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
'''