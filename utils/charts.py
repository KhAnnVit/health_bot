# charts.py
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import db
from matplotlib import dates as mdates

plt.style.use("seaborn-v0_8-whitegrid")


async def generate_weight_chart_bytes(telegram_id, limit=30):
    """Создаёт аккуратный график веса с линией цели (если она задана)"""

    # --- 1. Получаем данные из базы ---
    history = await db.get_weight_history(telegram_id, limit=limit)
    if not history:
        return None

    # --- 2. Готовим данные для графика ---
    df = pd.DataFrame(
        [
            {"date": record["recorded_at"], "weight": float(record["weight"])}
            for record in history
        ]
    )
    df = df.sort_values("date")

    # --- 3. Берём цель из профиля ---
    profile = await db.get_profile(telegram_id)
    target_weight = profile.get("target_weight_kg") if profile else None
    if target_weight is not None:
        target_weight = float(target_weight)

    # --- 4. Создаём холст ---
    fig, ax = plt.subplots(figsize=(10, 5))

    # --- 5. Рисуем основную линию ---
    ax.plot(
        df["date"], df["weight"],
        marker="o", linewidth=2.5, markersize=7,
        color="#6c5ce7", markerfacecolor="white",
        markeredgecolor="#6c5ce7", markeredgewidth=2,
        label="Вес",
    )

    # --- 6. Заливка под графиком ---
    ax.fill_between(df["date"], df["weight"], alpha=0.15, color="#6c5ce7")

    # --- 7. 🎯 Линия цели (если задана) ---
    if target_weight is not None:
        ax.axhline(
            y=target_weight, color="orange", linestyle="--", linewidth=2,
            label=f"Цель: {target_weight} кг"
        )

    # --- 8. Умный диапазон оси Y (с учётом цели) ---
    min_weight = df["weight"].min()
    max_weight = df["weight"].max()
    range_weight = max_weight - min_weight
    padding = range_weight * 0.2 if range_weight > 0 else 2

    y_min = min_weight - padding
    y_max = max_weight + padding

    # Если цель выходит за пределы данных → расширяем границы
    if target_weight is not None:
        y_min = min(y_min, target_weight - padding)
        y_max = max(y_max, target_weight + padding)

    ax.set_ylim(y_min, y_max)

    # --- 9. Подписи и форматирование ---
    ax.set_title("Ваш вес", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Дата", fontsize=10)
    ax.set_ylabel("кг", fontsize=10)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(
        ax.xaxis.get_majorticklabels(),
        rotation=45, ha="right", fontsize=9
    )

    ax.grid(True, linestyle="--", alpha=0.4, color="#cccccc")
    ax.legend(frameon=True, fancybox=True, loc="best", fontsize=9)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#e0e0e0")
    ax.spines["bottom"].set_color("#e0e0e0")

    plt.tight_layout()

    # --- 10. Сохраняем в память ---
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    return buffer