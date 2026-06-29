from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from theme import STYLESHEET, EDF_BLUE, EDF_WHITE
from resources import get_edf_logo_pixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EDF PDF Tools")
        self.setMinimumSize(900, 620)
        self.resize(1000, 680)
        self.setStyleSheet(STYLESHEET)
        self.setWindowIcon(QIcon(get_edf_logo_pixmap(64, 64)))

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
        sidebar.setFixedWidth(240)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(6)

        logo_label = QLabel()
        logo_label.setPixmap(get_edf_logo_pixmap(180, 70))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet(f"background-color: rgba(255,255,255,0.2);")
        layout.addWidget(separator)
        layout.addSpacing(10)

        app_title = QLabel("PDF Tools")
        app_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_title.setStyleSheet(f"color: {EDF_WHITE}; font-size: 12px; font-weight: 500; opacity: 0.8;")
        layout.addWidget(app_title)
        layout.addSpacing(16)

        self.nav_buttons = []

        btn_compress = QPushButton("  Compresser")
        btn_compress.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_compress.clicked.connect(lambda: self._set_active_page(0))
        layout.addWidget(btn_compress)
        self.nav_buttons.append(btn_compress)

        btn_merge = QPushButton("  Fusionner")
        btn_merge.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_merge.clicked.connect(lambda: self._set_active_page(1))
        layout.addWidget(btn_merge)
        self.nav_buttons.append(btn_merge)

        layout.addStretch()

        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet(f"color: rgba(255,255,255,0.4); font-size: 11px;")
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
