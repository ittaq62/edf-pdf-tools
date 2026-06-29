from PyQt6.QtGui import QPainter, QPixmap, QFont, QColor, QPainterPath, QLinearGradient
from PyQt6.QtCore import Qt, QRectF, QPointF


EDF_BLUE = "#003DA5"
EDF_BLUE_LIGHT = "#0055CC"
EDF_BLUE_DARK = "#002B75"
EDF_ORANGE = "#FF6600"
EDF_ORANGE_HOVER = "#FF8533"
EDF_WHITE = "#FFFFFF"
EDF_GRAY_BG = "#F0F2F5"
EDF_GRAY_BORDER = "#D1D5DB"
EDF_TEXT = "#1F2937"
EDF_TEXT_LIGHT = "#6B7280"


def create_edf_logo(width=200, height=80):
    pixmap = QPixmap(width, height)
    pixmap.fill(QColor(0, 0, 0, 0))

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    flame_x = width * 0.08
    flame_bottom = height * 0.85
    flame_width = width * 0.18
    flame_height = height * 0.7

    path = QPainterPath()
    path.moveTo(flame_x + flame_width * 0.5, flame_bottom - flame_height)
    path.cubicTo(
        flame_x + flame_width * 0.15, flame_bottom - flame_height * 0.5,
        flame_x - flame_width * 0.1, flame_bottom - flame_height * 0.15,
        flame_x + flame_width * 0.3, flame_bottom,
    )
    path.lineTo(flame_x + flame_width * 0.7, flame_bottom)
    path.cubicTo(
        flame_x + flame_width * 1.1, flame_bottom - flame_height * 0.15,
        flame_x + flame_width * 0.85, flame_bottom - flame_height * 0.5,
        flame_x + flame_width * 0.5, flame_bottom - flame_height,
    )

    gradient = QLinearGradient(
        QPointF(flame_x + flame_width * 0.5, flame_bottom - flame_height),
        QPointF(flame_x + flame_width * 0.5, flame_bottom),
    )
    gradient.setColorAt(0.0, QColor(EDF_ORANGE))
    gradient.setColorAt(0.7, QColor("#FF4500"))
    gradient.setColorAt(1.0, QColor("#CC3700"))

    painter.setBrush(gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawPath(path)

    inner = QPainterPath()
    inner_scale = 0.45
    inner_x = flame_x + flame_width * 0.5 - (flame_width * inner_scale * 0.5)
    inner_bottom = flame_bottom - flame_height * 0.08
    inner_h = flame_height * inner_scale

    inner.moveTo(inner_x + flame_width * inner_scale * 0.5, inner_bottom - inner_h)
    inner.cubicTo(
        inner_x + flame_width * inner_scale * 0.2, inner_bottom - inner_h * 0.4,
        inner_x, inner_bottom - inner_h * 0.1,
        inner_x + flame_width * inner_scale * 0.35, inner_bottom,
    )
    inner.lineTo(inner_x + flame_width * inner_scale * 0.65, inner_bottom)
    inner.cubicTo(
        inner_x + flame_width * inner_scale, inner_bottom - inner_h * 0.1,
        inner_x + flame_width * inner_scale * 0.8, inner_bottom - inner_h * 0.4,
        inner_x + flame_width * inner_scale * 0.5, inner_bottom - inner_h,
    )

    inner_gradient = QLinearGradient(
        QPointF(inner_x + flame_width * inner_scale * 0.5, inner_bottom - inner_h),
        QPointF(inner_x + flame_width * inner_scale * 0.5, inner_bottom),
    )
    inner_gradient.setColorAt(0.0, QColor("#FFD700"))
    inner_gradient.setColorAt(1.0, QColor(EDF_ORANGE))
    painter.setBrush(inner_gradient)
    painter.drawPath(inner)

    font = QFont("Arial Black", 28, QFont.Weight.Black)
    painter.setFont(font)
    painter.setPen(QColor(EDF_ORANGE))

    text_x = flame_x + flame_width + width * 0.04
    text_rect = QRectF(text_x, 0, width - text_x, height)
    painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, "EDF")

    painter.end()
    return pixmap


STYLESHEET = f"""
QMainWindow {{
    background-color: {EDF_GRAY_BG};
}}

/* Sidebar */
#sidebar {{
    background-color: {EDF_BLUE};
    border: none;
}}

#sidebar QPushButton {{
    background-color: transparent;
    color: {EDF_WHITE};
    border: none;
    border-radius: 8px;
    padding: 14px 20px;
    text-align: left;
    font-size: 14px;
    font-weight: 500;
    margin: 2px 10px;
}}

#sidebar QPushButton:hover {{
    background-color: {EDF_BLUE_LIGHT};
}}

#sidebar QPushButton[active="true"] {{
    background-color: {EDF_ORANGE};
    font-weight: 700;
}}

/* Content area */
#content {{
    background-color: {EDF_GRAY_BG};
    border: none;
}}

/* Cards */
.card {{
    background-color: {EDF_WHITE};
    border: 1px solid {EDF_GRAY_BORDER};
    border-radius: 12px;
    padding: 24px;
}}

/* File list */
QListWidget {{
    background-color: {EDF_WHITE};
    border: 2px dashed {EDF_GRAY_BORDER};
    border-radius: 10px;
    padding: 8px;
    font-size: 13px;
    color: {EDF_TEXT};
}}

QListWidget::item {{
    padding: 8px 12px;
    border-radius: 6px;
    margin: 2px 0;
}}

QListWidget::item:selected {{
    background-color: #E8F0FE;
    color: {EDF_BLUE};
}}

QListWidget::item:hover {{
    background-color: #F3F4F6;
}}

/* Buttons */
QPushButton#btn_primary {{
    background-color: {EDF_ORANGE};
    color: {EDF_WHITE};
    border: none;
    border-radius: 8px;
    padding: 12px 28px;
    font-size: 14px;
    font-weight: 700;
    min-width: 160px;
}}

QPushButton#btn_primary:hover {{
    background-color: {EDF_ORANGE_HOVER};
}}

QPushButton#btn_primary:disabled {{
    background-color: #CCCCCC;
    color: #888888;
}}

QPushButton#btn_secondary {{
    background-color: {EDF_WHITE};
    color: {EDF_BLUE};
    border: 2px solid {EDF_BLUE};
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: 600;
}}

QPushButton#btn_secondary:hover {{
    background-color: #E8F0FE;
}}

QPushButton#btn_icon {{
    background-color: {EDF_WHITE};
    color: {EDF_TEXT};
    border: 1px solid {EDF_GRAY_BORDER};
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 12px;
}}

QPushButton#btn_icon:hover {{
    background-color: #F3F4F6;
    border-color: {EDF_BLUE};
}}

/* ComboBox */
QComboBox {{
    background-color: {EDF_WHITE};
    border: 2px solid {EDF_GRAY_BORDER};
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 13px;
    color: {EDF_TEXT};
    min-width: 200px;
}}

QComboBox:hover {{
    border-color: {EDF_BLUE};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox QAbstractItemView {{
    background-color: {EDF_WHITE};
    border: 1px solid {EDF_GRAY_BORDER};
    border-radius: 6px;
    selection-background-color: #E8F0FE;
    selection-color: {EDF_BLUE};
}}

/* Progress bar */
QProgressBar {{
    background-color: #E5E7EB;
    border: none;
    border-radius: 6px;
    text-align: center;
    font-size: 12px;
    font-weight: 600;
    color: {EDF_TEXT};
    min-height: 24px;
}}

QProgressBar::chunk {{
    background-color: {EDF_ORANGE};
    border-radius: 6px;
}}

/* Labels */
QLabel#title {{
    color: {EDF_TEXT};
    font-size: 22px;
    font-weight: 700;
}}

QLabel#subtitle {{
    color: {EDF_TEXT_LIGHT};
    font-size: 13px;
}}

QLabel#section_title {{
    color: {EDF_TEXT};
    font-size: 15px;
    font-weight: 600;
}}

QLabel#status {{
    color: {EDF_TEXT_LIGHT};
    font-size: 12px;
    padding: 4px 0;
}}

QLabel#drop_hint {{
    color: {EDF_TEXT_LIGHT};
    font-size: 13px;
    font-style: italic;
}}
"""
