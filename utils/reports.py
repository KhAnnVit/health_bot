# utils/report.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  # ← Добавили импорт шрифтов
from io import BytesIO
from datetime import datetime
import db
import os

# ============================================
# 🅰️ РЕГИСТРАЦИЯ ШРИФТА С КИРИЛЛИЦЕЙ
# ============================================
# Путь к папке со шрифтами (относительно проекта)
FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts')

# Регистрируем шрифт DejaVu Sans (поддерживает русский)
pdfmetrics.registerFont(TTFont('DejaVu', os.path.join(FONTS_DIR, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', os.path.join(FONTS_DIR, 'DejaVuSans-Bold.ttf')))


# ============================================
# ⚖️ ОТЧЁТ ПО ВЕСУ
# ============================================
async def generate_weight_report(telegram_id: int):
    weight_history = await db.get_weight_history(telegram_id, limit=1000)

    if not weight_history:
        return None

    weight_history = sorted(weight_history, key=lambda x: x["recorded_at"])

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    # ⭐ Создаём свои стили с кириллическим шрифтом
    from reportlab.lib.styles import ParagraphStyle

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='DejaVu-Bold',  # ← Используем наш шрифт
        fontSize=16,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontName='DejaVu-Bold',  # ← Используем наш шрифт
        fontSize=12,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='DejaVu',  # ← Используем наш шрифт
        fontSize=10
    )

    elements = []

    # Заголовок
    elements.append(Paragraph("Отчёт по весу", title_style))  # ← Убрали эмодзи (могут не работать)
    elements.append(Spacer(1, 0.5 * cm))

    # Дата формирования
    date_info = f"<b>Дата формирования:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    elements.append(Paragraph(date_info, normal_style))
    elements.append(Spacer(1, 1 * cm))

    # Статистика
    weights = [float(r["weight"]) for r in weight_history]

    stats_data = [
        ["Показатель", "Значение"],
        ["Всего записей", str(len(weights))],
        ["Средний вес", f"{sum(weights) / len(weights):.1f} кг"],
        ["Минимальный вес", f"{min(weights):.1f} кг"],
        ["Максимальный вес", f"{max(weights):.1f} кг"],
        ["Первая запись", f"{weights[0]:.1f} кг"],
        ["Последняя запись", f"{weights[-1]:.1f} кг"],
        ["Изменение", f"{weights[-1] - weights[0]:+.1f} кг"],
    ]

    stats_table = Table(stats_data, colWidths=[5 * cm, 3 * cm])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6c5ce7')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVu-Bold'),  # ← Наш шрифт
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVu'),  # ← Наш шрифт для данных
    ]))

    elements.append(stats_table)
    elements.append(Spacer(1, 1 * cm))

    # Детальные записи
    elements.append(Paragraph(f"Полная история ({len(weights)} записей):", subtitle_style))
    elements.append(Spacer(1, 0.3 * cm))

    weight_rows = [["Дата и время", "Вес (кг)"]]
    for record in reversed(weight_history):
        date = record["recorded_at"].strftime("%d.%m.%Y %H:%M")
        weight_rows.append([date, f"{record['weight']}"])

    weight_table = Table(weight_rows, colWidths=[5 * cm, 2 * cm])
    weight_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6c5ce7')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVu-Bold'),  # ← Наш шрифт
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVu'),  # ← Наш шрифт для данных
    ]))

    elements.append(weight_table)
    elements.append(Spacer(1, 1 * cm))

    # Примечание
    notes = """
    <b>Примечание:</b><br/>
    Данный отчёт сформирован автоматически на основе данных, введённых пользователем.<br/>
    Для точной диагностики и рекомендаций проконсультируйтесь с врачом.
    """
    elements.append(Paragraph(notes, normal_style))

    # Генерируем PDF
    doc.build(elements)
    buffer.seek(0)

    return buffer


# ============================================
# 💓 ОТЧЁТ ПО ДАВЛЕНИЮ (с пульсом)
# ============================================
async def generate_pressure_report(telegram_id: int):
    pressure_history = await db.get_pressure_history(telegram_id, limit=1000)

    if not pressure_history:
        return None

    pressure_history = sorted(pressure_history, key=lambda x: x["recorded_at"])

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    from reportlab.lib.styles import ParagraphStyle

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='DejaVu-Bold',
        fontSize=16,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontName='DejaVu-Bold',
        fontSize=12,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='DejaVu',
        fontSize=10
    )

    elements = []

    # Заголовок
    elements.append(Paragraph("Отчёт по давлению и пульсу", title_style))  # ← Убрали эмодзи
    elements.append(Spacer(1, 0.5 * cm))

    # Дата
    date_info = f"<b>Дата формирования:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    elements.append(Paragraph(date_info, normal_style))
    elements.append(Spacer(1, 1 * cm))

    # Данные
    systolic = [r["systolic"] for r in pressure_history]
    diastolic = [r["diastolic"] for r in pressure_history]
    pulse = [r.get("pulse") for r in pressure_history if r.get("pulse")]

    stats_data = [
        ["Показатель", "Верхнее", "Нижнее"],
        ["Всего записей", str(len(systolic)), str(len(diastolic))],
        ["Среднее", f"{sum(systolic) / len(systolic):.0f}", f"{sum(diastolic) / len(diastolic):.0f}"],
        ["Минимальное", f"{min(systolic)}", f"{min(diastolic)}"],
        ["Максимальное", f"{max(systolic)}", f"{max(diastolic)}"],
        ["Первая запись", f"{systolic[0]}", f"{diastolic[0]}"],
        ["Последняя запись", f"{systolic[-1]}", f"{diastolic[-1]}"],
    ]

    if pulse:
        stats_data.append(["Пульс (средний)", f"{sum(pulse) / len(pulse):.0f} уд/мин", "-"])
        stats_data.append(["Пульс (мин)", f"{min(pulse)} уд/мин", "-"])
        stats_data.append(["Пульс (макс)", f"{max(pulse)} уд/мин", "-"])

    stats_table = Table(stats_data, colWidths=[4 * cm, 2.5 * cm, 2.5 * cm])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVu-Bold'),  # ← Наш шрифт
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVu'),  # ← Наш шрифт для данных
    ]))

    elements.append(stats_table)
    elements.append(Spacer(1, 1 * cm))

    # Детальные записи
    elements.append(Paragraph(f"Полная история ({len(pressure_history)} записей):", subtitle_style))
    elements.append(Spacer(1, 0.3 * cm))

    pressure_rows = [["Дата и время", "Верхнее", "Нижнее", "Пульс"]]
    for record in reversed(pressure_history):
        date = record["recorded_at"].strftime("%d.%m.%Y %H:%M")
        pulse_val = str(record.get("pulse", "-")) if record.get("pulse") else "-"
        pressure_rows.append([date, str(record["systolic"]), str(record["diastolic"]), pulse_val])

    pressure_table = Table(pressure_rows, colWidths=[4 * cm, 2 * cm, 2 * cm, 2 * cm])
    pressure_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVu-Bold'),  # ← Наш шрифт
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVu'),  # ← Наш шрифт для данных
    ]))

    elements.append(pressure_table)
    elements.append(Spacer(1, 1 * cm))

    # Примечание
    notes = """
    <b>Примечание:</b><br/>
    Данный отчёт сформирован автоматически на основе данных, введённых пользователем.<br/><br/>
    <b>Нормальные показатели:</b><br/>
    - Давление: 120/80 мм рт.ст.<br/>
    - Повышенное: от 140/90 мм рт.ст.<br/>
    - Пульс в покое: 60-90 уд/мин
    """
    elements.append(Paragraph(notes, normal_style))

    # Генерируем PDF
    doc.build(elements)
    buffer.seek(0)

    return buffer