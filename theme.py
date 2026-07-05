from PyQt6.QtGui import QColor, QPalette

EDF_BLUE = "#003DA5"
EDF_BLUE_LIGHT = "#1a56c4"
EDF_BLUE_DARK = "#002B75"
EDF_ORANGE = "#FF6600"
EDF_ORANGE_HOVER = "#e85d00"
EDF_WHITE = "#FFFFFF"
EDF_GRAY_BG = "#F2F3F5"
EDF_GRAY_BORDER = "#CCCCCC"
EDF_TEXT = "#222222"
EDF_TEXT_LIGHT = "#777777"


def build_light_palette():
    """Palette claire explicite : sans elle, les menus contextuels et
    listes déroulantes héritent du thème sombre de Windows."""
    palette = QPalette()
    roles = {
        QPalette.ColorRole.Window: EDF_GRAY_BG,
        QPalette.ColorRole.WindowText: EDF_TEXT,
        QPalette.ColorRole.Base: EDF_WHITE,
        QPalette.ColorRole.AlternateBase: "#F7F7F7",
        QPalette.ColorRole.Text: EDF_TEXT,
        QPalette.ColorRole.Button: EDF_WHITE,
        QPalette.ColorRole.ButtonText: EDF_TEXT,
        QPalette.ColorRole.ToolTipBase: EDF_WHITE,
        QPalette.ColorRole.ToolTipText: EDF_TEXT,
        QPalette.ColorRole.PlaceholderText: EDF_TEXT_LIGHT,
        QPalette.ColorRole.Highlight: EDF_BLUE,
        QPalette.ColorRole.HighlightedText: EDF_WHITE,
    }
    for role, color in roles.items():
        palette.setColor(role, QColor(color))
    return palette


STYLESHEET = f"""
QMainWindow {{
    background-color: {EDF_GRAY_BG};
}}

#sidebar {{
    background-color: {EDF_BLUE};
}}

#sidebar QPushButton {{
    background-color: transparent;
    color: {EDF_WHITE};
    border: none;
    border-radius: 5px;
    padding: 11px 16px;
    text-align: left;
    font-size: 13px;
    margin: 1px 6px;
}}

#sidebar QPushButton:hover {{
    background-color: {EDF_BLUE_LIGHT};
}}

#sidebar QPushButton[active="true"] {{
    background-color: {EDF_ORANGE};
    font-weight: bold;
}}

#content {{
    background-color: {EDF_GRAY_BG};
}}

QListWidget {{
    background-color: {EDF_WHITE};
    border: 2px dashed {EDF_GRAY_BORDER};
    border-radius: 6px;
    padding: 6px;
    font-size: 13px;
    color: {EDF_TEXT};
}}

QListWidget::item {{
    padding: 6px 10px;
    border-radius: 3px;
}}

QListWidget::item:selected {{
    background-color: #dce6f7;
    color: {EDF_BLUE};
}}

QListWidget::item:hover {{
    background-color: #f0f0f0;
}}

QPushButton#btn_primary {{
    background-color: {EDF_ORANGE};
    color: {EDF_WHITE};
    border: none;
    border-radius: 5px;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: bold;
}}

QPushButton#btn_primary:hover {{
    background-color: {EDF_ORANGE_HOVER};
}}

QPushButton#btn_primary:disabled {{
    background-color: #BBBBBB;
    color: #888888;
}}

QPushButton#btn_secondary {{
    background-color: {EDF_WHITE};
    color: {EDF_BLUE};
    border: 1px solid {EDF_BLUE};
    border-radius: 5px;
    padding: 8px 16px;
    font-size: 13px;
}}

QPushButton#btn_secondary:hover {{
    background-color: #e8eef8;
}}

QPushButton#btn_icon {{
    background-color: {EDF_WHITE};
    color: {EDF_TEXT};
    border: 1px solid {EDF_GRAY_BORDER};
    border-radius: 4px;
    padding: 7px 12px;
    font-size: 12px;
}}

QPushButton#btn_icon:hover {{
    background-color: #f0f0f0;
}}

QComboBox {{
    background-color: {EDF_WHITE};
    border: 1px solid {EDF_GRAY_BORDER};
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 13px;
    color: {EDF_TEXT};
    min-width: 180px;
    combobox-popup: 0;
}}

QComboBox:hover {{
    border-color: {EDF_BLUE};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox QAbstractItemView {{
    background-color: {EDF_WHITE};
    border: 1px solid {EDF_GRAY_BORDER};
    outline: none;
    selection-background-color: #dce6f7;
    selection-color: {EDF_BLUE};
}}

QComboBox QAbstractItemView::item {{
    min-height: 30px;
    padding-left: 8px;
}}

QProgressBar {{
    background-color: #E0E0E0;
    border: none;
    border-radius: 4px;
    text-align: center;
    font-size: 11px;
    color: {EDF_TEXT};
    min-height: 20px;
}}

QProgressBar::chunk {{
    background-color: {EDF_ORANGE};
    border-radius: 4px;
}}

QLabel#title {{
    color: {EDF_TEXT};
    font-size: 18px;
    font-weight: bold;
}}

QLabel#subtitle {{
    color: {EDF_TEXT_LIGHT};
    font-size: 12px;
}}

QLabel#section_title {{
    color: {EDF_TEXT};
    font-size: 13px;
    font-weight: bold;
}}

QLabel#status {{
    color: {EDF_TEXT_LIGHT};
    font-size: 11px;
}}

QLabel#drop_hint {{
    color: {EDF_TEXT_LIGHT};
    font-size: 11px;
    font-style: italic;
}}
"""
