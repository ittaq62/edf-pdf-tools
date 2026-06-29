import sys
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtCore import Qt

from app import MainWindow


def main():
    application = QApplication(sys.argv)
    application.setStyle("Fusion")

    window = MainWindow()

    placeholder_compress = QLabel("Page Compression")
    placeholder_compress.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.add_page(placeholder_compress, 0)

    placeholder_merge = QLabel("Page Fusion")
    placeholder_merge.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.add_page(placeholder_merge, 1)

    window.show()
    sys.exit(application.exec())


if __name__ == "__main__":
    main()
