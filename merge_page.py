import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QProgressBar, QFileDialog, QMessageBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from pdf_tools import merge_pdfs


class MergeWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str, int)
    error = pyqtSignal(str)

    def __init__(self, input_paths, output_path):
        super().__init__()
        self.input_paths = input_paths
        self.output_path = output_path

    def run(self):
        try:
            size = merge_pdfs(
                self.input_paths, self.output_path,
                progress_callback=self.progress.emit,
            )
            self.finished.emit(self.output_path, size)
        except Exception as e:
            self.error.emit(str(e))


class MergePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.worker = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        title = QLabel("Fusionner des fichiers PDF")
        title.setObjectName("title")
        layout.addWidget(title)

        subtitle = QLabel("Combinez plusieurs PDF en un seul document, réorganisez l'ordre si besoin")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        layout.addSpacing(8)

        list_label = QLabel("Fichiers à fusionner (dans l'ordre) :")
        list_label.setObjectName("section_title")
        layout.addWidget(list_label)

        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(200)
        self.file_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.file_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        layout.addWidget(self.file_list)

        drop_hint = QLabel("Glissez-déposez vos fichiers PDF ici ou utilisez le bouton ci-dessous")
        drop_hint.setObjectName("drop_hint")
        drop_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(drop_hint)

        btn_row = QHBoxLayout()

        btn_add = QPushButton("Ajouter des fichiers")
        btn_add.setObjectName("btn_secondary")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self._add_files)
        btn_row.addWidget(btn_add)

        btn_up = QPushButton("Monter")
        btn_up.setObjectName("btn_icon")
        btn_up.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_up.clicked.connect(self._move_up)
        btn_row.addWidget(btn_up)

        btn_down = QPushButton("Descendre")
        btn_down.setObjectName("btn_icon")
        btn_down.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_down.clicked.connect(self._move_down)
        btn_row.addWidget(btn_down)

        btn_remove = QPushButton("Retirer")
        btn_remove.setObjectName("btn_icon")
        btn_remove.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_remove.clicked.connect(self._remove_selected)
        btn_row.addWidget(btn_remove)

        btn_clear = QPushButton("Tout effacer")
        btn_clear.setObjectName("btn_icon")
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.clicked.connect(self._clear_files)
        btn_row.addWidget(btn_clear)

        btn_row.addStretch()

        self.btn_merge = QPushButton("Fusionner")
        self.btn_merge.setObjectName("btn_primary")
        self.btn_merge.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_merge.clicked.connect(self._start_merge)
        btn_row.addWidget(self.btn_merge)

        layout.addLayout(btn_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.status_label.setObjectName("status")
        layout.addWidget(self.status_label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(".pdf"):
                    event.acceptProposedAction()
                    return

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".pdf") and not self._file_already_listed(path):
                size = os.path.getsize(path)
                display = f"{Path(path).name}  ({self._format_size(size)})"
                self.file_list.addItem(display)
                item = self.file_list.item(self.file_list.count() - 1)
                item.setData(Qt.ItemDataRole.UserRole, path)

    def _add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionner des fichiers PDF", "",
            "Fichiers PDF (*.pdf)",
        )
        for f in files:
            if not self._file_already_listed(f):
                size = os.path.getsize(f)
                display = f"{Path(f).name}  ({self._format_size(size)})"
                self.file_list.addItem(display)
                item = self.file_list.item(self.file_list.count() - 1)
                item.setData(Qt.ItemDataRole.UserRole, f)

    def _file_already_listed(self, path):
        for i in range(self.file_list.count()):
            if self.file_list.item(i).data(Qt.ItemDataRole.UserRole) == path:
                return True
        return False

    def _move_up(self):
        row = self.file_list.currentRow()
        if row > 0:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row - 1, item)
            self.file_list.setCurrentRow(row - 1)

    def _move_down(self):
        row = self.file_list.currentRow()
        if row < self.file_list.count() - 1:
            item = self.file_list.takeItem(row)
            self.file_list.insertItem(row + 1, item)
            self.file_list.setCurrentRow(row + 1)

    def _remove_selected(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def _clear_files(self):
        self.file_list.clear()

    def _start_merge(self):
        if self.file_list.count() < 2:
            QMessageBox.warning(
                self, "Fichiers insuffisants",
                "Veuillez ajouter au moins 2 fichiers PDF à fusionner.",
            )
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le PDF fusionné", "fusion.pdf",
            "Fichier PDF (*.pdf)",
        )
        if not output_path:
            return

        input_paths = []
        for i in range(self.file_list.count()):
            input_paths.append(self.file_list.item(i).data(Qt.ItemDataRole.UserRole))

        self.btn_merge.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Fusion en cours...")

        self.worker = MergeWorker(input_paths, output_path)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self._on_merge_done)
        self.worker.error.connect(self._on_merge_error)
        self.worker.start()

    def _on_merge_done(self, output_path, size):
        self.progress_bar.setValue(100)
        self.btn_merge.setEnabled(True)
        self.status_label.setText("Fusion terminée")

        QMessageBox.information(
            self, "Fusion terminée",
            f"Le fichier fusionné a été créé :\n\n"
            f"  {Path(output_path).name}\n"
            f"  Taille : {self._format_size(size)}\n"
            f"  Fichiers combinés : {self.file_list.count()}",
        )
        self.progress_bar.setVisible(False)

    def _on_merge_error(self, error_msg):
        self.btn_merge.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("")

        QMessageBox.critical(
            self, "Erreur de fusion",
            f"Une erreur est survenue :\n\n{error_msg}",
        )

    @staticmethod
    def _format_size(size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} o"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} Ko"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} Mo"
