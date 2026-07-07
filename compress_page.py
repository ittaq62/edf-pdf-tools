import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QComboBox, QProgressBar,
    QFileDialog, QMessageBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from pdf_tools import compress_pdf, estimate_compression, QUALITY_PRESETS
from drop_overlay import DropOverlay


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


class EstimateWorker(QThread):
    done = pyqtSignal(int, str, int, int)
    failed = pyqtSignal(int, str, str)

    def __init__(self, generation, input_path, quality):
        super().__init__()
        self.generation = generation
        self.input_path = input_path
        self.quality = quality

    def run(self):
        try:
            original, estimated = estimate_compression(self.input_path, self.quality)
            self.done.emit(self.generation, self.input_path, original, estimated)
        except Exception as e:
            self.failed.emit(self.generation, self.input_path, str(e))


class CompressPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.workers = []
        self._estimate_generation = 0
        self._estimate_queue = []
        self._estimate_worker = None
        self._setup_ui()
        self._drop_overlay = DropOverlay(self)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(".pdf"):
                    event.acceptProposedAction()
                    self._drop_overlay.show_over(self.file_list)
                    return

    def dragLeaveEvent(self, event):
        self._drop_overlay.hide_now()

    def dropEvent(self, event):
        self._drop_overlay.hide_now()
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".pdf"):
                self._append_file(path)

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
        self.quality_combo.currentTextChanged.connect(self._on_quality_changed)
        settings_row.addWidget(self.quality_combo)

        settings_row.addStretch()
        layout.addLayout(settings_row)

        list_label = QLabel("Fichiers à compresser :")
        list_label.setObjectName("section_title")
        layout.addWidget(list_label)

        self.file_list = QListWidget()
        self.file_list.setObjectName("compress_list")
        self.file_list.setMinimumHeight(150)
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

    # ----- Gestion de la liste -----

    def _add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionner des fichiers PDF", "",
            "Fichiers PDF (*.pdf)",
        )
        for f in files:
            self._append_file(f)

    def _append_file(self, path):
        if self._file_already_listed(path):
            return

        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, path)

        label = QLabel()
        label.setTextFormat(Qt.TextFormat.RichText)
        label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        label.setStyleSheet("background: transparent; padding: 7px 10px;")

        self.file_list.addItem(item)
        self.file_list.setItemWidget(item, label)
        self._set_item_text(path, self._waiting_text(path))

        self._queue_estimate(path)

    def _file_already_listed(self, path):
        for i in range(self.file_list.count()):
            if self.file_list.item(i).data(Qt.ItemDataRole.UserRole) == path:
                return True
        return False

    def _item_label(self, path):
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == path:
                return item, self.file_list.itemWidget(item)
        return None, None

    def _set_item_text(self, path, html):
        item, label = self._item_label(path)
        if label is not None:
            label.setText(html)
            item.setSizeHint(label.sizeHint())

    def _remove_selected(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def _clear_files(self):
        self._estimate_generation += 1
        self._estimate_queue.clear()
        self.file_list.clear()

    # ----- Estimation du gain en direct -----

    def _on_quality_changed(self, _quality):
        self._estimate_generation += 1
        self._estimate_queue.clear()
        for i in range(self.file_list.count()):
            path = self.file_list.item(i).data(Qt.ItemDataRole.UserRole)
            self._set_item_text(path, self._waiting_text(path))
            self._estimate_queue.append(path)
        self._start_next_estimate()

    def _queue_estimate(self, path):
        self._estimate_queue.append(path)
        self._start_next_estimate()

    def _start_next_estimate(self):
        if self._estimate_worker is not None and self._estimate_worker.isRunning():
            return
        if not self._estimate_queue:
            return

        path = self._estimate_queue.pop(0)
        worker = EstimateWorker(
            self._estimate_generation, path, self.quality_combo.currentText(),
        )
        worker.done.connect(self._on_estimate_done)
        worker.failed.connect(self._on_estimate_failed)
        worker.finished.connect(self._start_next_estimate)
        self._estimate_worker = worker
        worker.start()

    def _on_estimate_done(self, generation, path, original, estimated):
        if generation != self._estimate_generation:
            return
        saved = original - estimated
        ratio = (saved / original * 100) if original > 0 else 0

        base = self._base_text(path)
        if ratio < 0.5:
            gain = '<span style="color:#999999;">déjà optimisé, aucun gain attendu</span>'
        else:
            gain = (
                f'<span style="color:#666666;">→ {self._format_size(estimated)}</span>'
                f'&nbsp;&nbsp;<b><span style="color:#CC0000;">'
                f'-{ratio:.0f} % (-{self._format_size(saved)})</span></b>'
            )
        self._set_item_text(path, f"{base}&nbsp;&nbsp;{gain}")

    def _on_estimate_failed(self, generation, path, message):
        if generation != self._estimate_generation:
            return
        base = self._base_text(path)
        self._set_item_text(
            path,
            f'{base}&nbsp;&nbsp;<span style="color:#CC0000;">'
            f'ne pourra pas être compressé : {message}</span>',
        )

    def _base_text(self, path):
        try:
            size = self._format_size(os.path.getsize(path))
        except OSError:
            size = "?"
        return (
            f'<span style="color:#222222;">{Path(path).name}</span>'
            f'&nbsp;&nbsp;<span style="color:#888888;">({size})</span>'
        )

    def _waiting_text(self, path):
        return (
            f"{self._base_text(path)}&nbsp;&nbsp;"
            f'<i><span style="color:#999999;">calcul du gain...</span></i>'
        )

    # ----- Compression -----

    def _start_compression(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "Aucun fichier", "Veuillez ajouter au moins un fichier PDF.")
            return

        output_dir = QFileDialog.getExistingDirectory(
            self, "Dossier de destination",
        )
        if not output_dir:
            return

        self._estimate_generation += 1
        self._estimate_queue.clear()

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
            if ratio < 0.5:
                lines.append(f"  {name} : {self._format_size(orig)} (déjà optimisé)")
            else:
                lines.append(
                    f"  {name} : {self._format_size(orig)} → {self._format_size(comp)} "
                    f"(-{ratio:.0f}%)"
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
