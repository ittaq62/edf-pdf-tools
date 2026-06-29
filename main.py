import sys
from PyQt6.QtWidgets import QApplication

from app import MainWindow
from compress_page import CompressPage
from merge_page import MergePage


def main():
    application = QApplication(sys.argv)
    application.setStyle("Fusion")

    window = MainWindow()

    window.add_page(CompressPage(), 0)
    window.add_page(MergePage(), 1)

    window.show()
    sys.exit(application.exec())


if __name__ == "__main__":
    main()
