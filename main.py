import sys
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtCore import Qt

from app import MainWindow
from compress_page import CompressPage


def main():
    application = QApplication(sys.argv)
    application.setStyle("Fusion")

    window = MainWindow()

    window.add_page(CompressPage(), 0)

    placeholder_merge = QLabel("Page Fusion")
    placeholder_merge.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.add_page(placeholder_merge, 1)

    window.show()
    sys.exit(application.exec())


if __name__ == "__main__":
    main()
