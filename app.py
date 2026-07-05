from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from theme import STYLESHEET, EDF_WHITE, apply_dark_title_bar
from resources import get_edf_logo_pixmap
from version import APP_NAME, APP_VERSION


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(850, 580)
        self.resize(960, 640)
        self.setStyleSheet(STYLESHEET)
        self.setWindowIcon(QIcon(get_edf_logo_pixmap(64, 64)))
        apply_dark_title_bar(self)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = self._build_sidebar()
        main_layout.addWidget(sidebar)

        self.stack = QStackedWidget()
        self.stack.setObjectName("content")
        main_layout.addWidget(self.stack, 1)

        self._set_active_page(0)

    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 16, 10, 16)
        layout.setSpacing(4)

        logo_label = QLabel()
        logo_label.setPixmap(get_edf_logo_pixmap(190, 65, white_text=True))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        layout.addSpacing(20)

        self.nav_buttons = []

        btn_compress = QPushButton("Compresser")
        btn_compress.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_compress.clicked.connect(lambda: self._set_active_page(0))
        layout.addWidget(btn_compress)
        self.nav_buttons.append(btn_compress)

        btn_merge = QPushButton("Fusionner")
        btn_merge.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_merge.clicked.connect(lambda: self._set_active_page(1))
        layout.addWidget(btn_merge)
        self.nav_buttons.append(btn_merge)

        layout.addStretch()

        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet(f"color: rgba(255,255,255,0.35); font-size: 10px;")
        layout.addWidget(version_label)

        return sidebar

    def add_page(self, widget, index):
        self.stack.insertWidget(index, widget)

    def _set_active_page(self, index):
        if index < self.stack.count():
            self.stack.setCurrentIndex(index)

        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", "true" if i == index else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
