import sys


def _update_splash(message):
    # L'ecran de demarrage n'existe que dans l'application empaquetee ;
    # en environnement de developpement ces appels sont ignores
    try:
        import pyi_splash
        pyi_splash.update_text(message)
    except Exception:
        pass


def _close_splash():
    try:
        import pyi_splash
        pyi_splash.close()
    except Exception:
        pass


def main():
    _update_splash("Initialisation...")

    from PyQt6.QtWidgets import QApplication

    from app import MainWindow
    from compress_page import CompressPage
    from merge_page import MergePage
    from theme import build_light_palette

    application = QApplication(sys.argv)
    application.setStyle("Fusion")
    application.setPalette(build_light_palette())

    window = MainWindow()

    window.add_page(CompressPage(), 0)
    window.add_page(MergePage(), 1)

    window.show()
    _close_splash()

    sys.exit(application.exec())


if __name__ == "__main__":
    main()
