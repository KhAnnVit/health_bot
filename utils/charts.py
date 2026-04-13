import matplotlib.pyplot as plt  # Основная библиотека для рисования
from io import BytesIO  # Чтобы хранить картинку в памяти, а не в файле
import pandas as pd  # Для удобной работы с таблицами данных
import db  # Ваш модуль для работы с базой данных


plt.style.use("seaborn-v0_8-whitegrid")  # Светлая сетка, приятные цвета


async def generate_weight_chart_bytes(telegram_id, limit=30):
    """Создаёт аккуратный график веса"""

    # --- 1. Получаем данные из базы ---
    history = await db.get_weight_history(telegram_id, limit=limit)

    if not history:
        return None

    # --- 2. Готовим данные для графика ---
    df = pd.DataFrame([
        {
            "date": record["recorded_at"],
            "weight": float(record["weight"])
        }
        for record in history
    ])
    df = df.sort_values("date")

    # --- 3. Создаём холст с оптимальным размером ---
    fig, ax = plt.subplots(figsize=(10, 5))

    # --- 4. Рисуем основную линию ---
    ax.plot(
        df["date"],
        df["weight"],
        marker="o",
        linewidth=2.5,
        markersize=7,
        color="#6c5ce7",
        markerfacecolor="white",
        markeredgecolor="#6c5ce7",
        markeredgewidth=2,
        label="Вес"
    )

    # --- 5. Добавляем заливку под графиком ---
    ax.fill_between(
        df["date"],
        df["weight"],
        alpha=0.15,
        color="#6c5ce7"
    )

    # --- 6. Настраиваем ось Y (умный диапазон) ---
    min_weight = df["weight"].min()
    max_weight = df["weight"].max()
    range_weight = max_weight - min_weight

    if range_weight > 0:
        padding = range_weight * 0.2
        ax.set_ylim(min_weight - padding, max_weight + padding)
    else:
        ax.set_ylim(min_weight - 2, min_weight + 2)

    # --- 7. Подписываем график ---
    ax.set_title("Ваш вес", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Дата", fontsize=10)
    ax.set_ylabel("кг", fontsize=10)

    # --- 8. Форматируем даты (аккуратно и читаемо) ---
    from matplotlib import dates as mdates
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=9)

    # --- 9. Настраиваем сетку (мягкая, не отвлекает) ---
    ax.grid(True, linestyle="--", alpha=0.4, color="#cccccc")

    # --- 10. Добавляем легенду ---
    ax.legend(frameon=True, fancybox=True, loc="best", fontsize=9)

    # --- 11. Убираем лишние рамки ---
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#e0e0e0")
    ax.spines["bottom"].set_color("#e0e0e0")

    # --- 12. Подгоняем отступы ---
    plt.tight_layout()

    # --- 13. Сохраняем в память ---
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    return buffer




async def generate_pressure_chart_bytes(telegram_id, limit=30):
    """Создаёт график давления с пульсом"""

    # --- 1. Получаем данные из базы ---
    history = await db.get_pressure_history(telegram_id, limit=limit)

    if not history:
        return None

    # --- 2. Готовим данные для графика ---
    df = pd.DataFrame([
        {
            "date": record["recorded_at"],
            "systolic": record["systolic"],
            "diastolic": record["diastolic"],
            "pulse": record.get("pulse")  # Пульс может быть None
        }
        for record in history
    ])
    df = df.sort_values("date")

    # --- 3. Рисуем график ---
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # 🔴 Верхнее давление (красная линия, левая ось)
    ax1.plot(
        df["date"],
        df["systolic"],
        marker="o",
        linewidth=2,
        markersize=5,
        color="#e74c3c",
        label="Верхнее",
        zorder=3
    )

    # 🔵 Нижнее давление (синяя линия, левая ось)
    ax1.plot(
        df["date"],
        df["diastolic"],
        marker="s",
        linewidth=2,
        markersize=5,
        color="#3498db",
        label="Нижнее",
        zorder=3
    )

    # --- 4. Пульс на отдельной оси (если есть данные) ---
    has_pulse = df["pulse"].notna().any()

    if has_pulse:
        ax2 = ax1.twinx()  # Вторая ось Y справа
        ax2.plot(
            df["date"],
            df["pulse"],
            marker="^",
            linewidth=2,
            markersize=5,
            color="#2ecc71",  # Зелёный
            label="Пульс",
            zorder=3
        )
        ax2.set_ylabel("Пульс (уд/мин)", fontsize=10, color="#2ecc71")
        ax2.tick_params(axis="y", labelcolor="#2ecc71")
        ax2.set_ylim(40, 120)  # Фиксированный диапазон для пульса
    else:
        ax2 = None

    # --- 5. Подписываем график ---
    ax1.set_title("Давление и пульс", fontsize=14, fontweight="bold", pad=15)
    ax1.set_xlabel("Дата", fontsize=10)
    ax1.set_ylabel("Давление (мм рт.ст.)", fontsize=10)

    # --- 6. Форматируем даты ---
    from matplotlib import dates as mdates
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=9)

    # --- 7. Сетка и легенда ---
    ax1.grid(True, linestyle="--", alpha=0.4, color="#cccccc")

    # Объединяем легенды с обеих осей
    lines1, labels1 = ax1.get_legend_handles_labels()
    if ax2:
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, frameon=True, fancybox=True, loc="best", fontsize=9)
    else:
        ax1.legend(frameon=True, fancybox=True, loc="best", fontsize=9)

    # --- 8. Убираем лишние рамки ---
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    plt.tight_layout()

    # --- 9. Сохраняем в память ---
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    return buffer