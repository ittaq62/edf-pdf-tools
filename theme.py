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
