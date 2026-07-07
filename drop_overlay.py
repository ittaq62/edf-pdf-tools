from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve


class DropOverlay(QLabel):
    """Voile affiché au-dessus de la liste pendant le survol d'un
    glisser-déposer de fichiers, avec un fondu à l'apparition."""

    def __init__(self, parent, text="Déposez vos fichiers PDF ici"):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setStyleSheet("""
            background-color: rgba(255, 247, 242, 0.93);
            color: #FF6600;
            border: 2px dashed #FF6600;
            border-radius: 6px;
            font-size: 15px;
            font-weight: bold;
        """)

        self._effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._effect)
        self._animation = QPropertyAnimation(self._effect, b"opacity", self)
        self._animation.setDuration(180)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.hide()

    def show_over(self, target):
        """Apparaît en fondu, exactement au-dessus du widget cible."""
        self.setGeometry(target.geometry())
        self.raise_()
        self._animation.stop()
        self._effect.setOpacity(0.0)
        self.show()
        self._animation.setStartValue(0.0)
        self._animation.setEndValue(1.0)
        self._animation.start()

    def hide_now(self):
        self._animation.stop()
        self.hide()
