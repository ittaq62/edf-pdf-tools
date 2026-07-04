import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QComboBox, QProgressBar, QFileDialog, QMessageBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl

from pdf_tools import compress_pdf, QUALITY_PRESETS


class CompressWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str, int, int)
    error = pyqtSignal(str, str)

    def __init__(self, input_path, output_path, quality):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.quality = quality

    def run(self):
        try:
            original, compressed = compress_pdf(
                self.input_path, self.output_path, self.quality,
                progress_callback=self.progress.emit,
            )
            self.finished.emit(self.input_path, original, compressed)
        except Exception as e:
            self.error.emit(self.input_path, str(e))


class CompressPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.workers = []
        self._setup_ui()

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
                self.file_list.item(self.file_list.count() - 1).setData(
                    Qt.ItemDataRole.UserRole, path,
                )

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(10)

        title = QLabel("Compresser des PDF")
        title.setObjectName("title")
        layout.addWidget(title)

        subtitle = QLabel("Réduire la taille des fichiers en compressant les images")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        layout.addSpacing(4)

        settings_row = QHBoxLayout()
        quality_label = QLabel("Niveau de compression :")
        quality_label.setObjectName("section_title")
        settings_row.addWidget(quality_label)

        self.quality_combo = QComboBox()
        for name in QUALITY_PRESETS:
            self.quality_combo.addItem(name)
        self.quality_combo.setCurrentText("Moyenne")
        settings_row.addWidget(self.quality_combo)

        settings_row.addStretch()
        layout.addLayout(settings_row)

        list_label = QLabel("Fichiers à compresser :")
        list_label.setObjectName("section_title")
        layout.addWidget(list_label)

        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(150)
        self.file_list.setAcceptDrops(True)
        layout.addWidget(self.file_list, 1)

        drop_hint = QLabel("Glisser-déposer des PDF ici, ou cliquer sur Ajouter")
        drop_hint.setObjectName("drop_hint")
        drop_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(drop_hint)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        btn_add = QPushButton("Ajouter")
        btn_add.setObjectName("btn_secondary")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self._add_files)
        btn_row.addWidget(btn_add)

        btn_remove = QPushButton("Retirer")
        btn_remove.setObjectName("btn_icon")
        btn_remove.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_remove.clicked.connect(self._remove_selected)
        btn_row.addWidget(btn_remove)

        btn_clear = QPushButton("Effacer tout")
        btn_clear.setObjectName("btn_icon")
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.clicked.connect(self._clear_files)
        btn_row.addWidget(btn_clear)

        btn_row.addStretch()

        self.btn_compress = QPushButton("Compresser")
        self.btn_compress.setObjectName("btn_primary")
        self.btn_compress.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_compress.clicked.connect(self._start_compression)
        btn_row.addWidget(self.btn_compress)

        layout.addLayout(btn_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.status_label.setObjectName("status")
        layout.addWidget(self.status_label)

    def _add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionner des fichiers PDF", "",
            "Fichiers PDF (*.pdf)",
        )
        for f in files:
            if not self._file_already_listed(f):
                size = os.path.getsize(f)
                display = f"{Path(f).name}  ({self._format_size(size)})"
                item = self.file_list.addItem(display)
                self.file_list.item(self.file_list.count() - 1).setData(Qt.ItemDataRole.UserRole, f)

    def _file_already_listed(self, path):
        for i in range(self.file_list.count()):
            if self.file_list.item(i).data(Qt.ItemDataRole.UserRole) == path:
                return True
        return False

    def _remove_selected(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def _clear_files(self):
        self.file_list.clear()

    def _start_compression(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "Aucun fichier", "Veuillez ajouter au moins un fichier PDF.")
            return

        output_dir = QFileDialog.getExistingDirectory(
            self, "Dossier de destination",
        )
        if not output_dir:
            return

        self.btn_compress.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self._results = []
        self._errors = []
        self._total_files = self.file_list.count()
        self._files_done = 0

        quality = self.quality_combo.currentText()

        for i in range(self.file_list.count()):
            input_path = self.file_list.item(i).data(Qt.ItemDataRole.UserRole)
            filename = Path(input_path).stem + "_compresse.pdf"
            output_path = str(Path(output_dir) / filename)

            worker = CompressWorker(input_path, output_path, quality)
            worker.progress.connect(self._on_file_progress)
            worker.finished.connect(self._on_file_done)
            worker.error.connect(self._on_file_error)
            self.workers.append(worker)

        self.workers[0].start()

    def _on_file_progress(self, value):
        file_progress = (self._files_done / self._total_files) * 100
        file_contrib = (value / self._total_files)
        self.progress_bar.setValue(int(file_progress + file_contrib))
        self.status_label.setText(
            f"Compression en cours... ({self._files_done + 1}/{self._total_files})"
        )

    def _on_file_done(self, path, original, compressed):
        ratio = (1 - compressed / original) * 100 if original > 0 else 0
        self._results.append((Path(path).name, original, compressed, ratio))
        self._files_done += 1
        self._process_next()

    def _on_file_error(self, path, error_msg):
        self._errors.append((Path(path).name, error_msg))
        self._files_done += 1
        self._process_next()

    def _process_next(self):
        if self._files_done < self._total_files:
            self.workers[self._files_done].start()
        else:
            self._finish()

    def _finish(self):
        self.progress_bar.setValue(100)
        self.btn_compress.setEnabled(True)
        self.workers.clear()

        lines = []
        for name, orig, comp, ratio in self._results:
            lines.append(
                f"  {name} : {self._format_size(orig)} → {self._format_size(comp)} "
                f"(-{ratio:.1f}%)"
            )

        for name, err in self._errors:
            lines.append(f"  {name} : Erreur - {err}")

        summary = "\n".join(lines)
        self.status_label.setText(f"{len(self._results)} fichier(s) compressé(s)")

        QMessageBox.information(
            self, "Compression terminée",
            f"Résultat :\n\n{summary}",
        )
        self.progress_bar.setVisible(False)

    @staticmethod
    def _format_size(size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} o"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} Ko"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} Mo"
