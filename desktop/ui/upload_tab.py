"""
Upload tab: file selection, upload, summary display, PDF download.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QGroupBox, QGridLayout, QFrame,
)
from PyQt5.QtCore import pyqtSignal


class UploadTab(QWidget):
    """Upload CSV, show summary, download PDF."""

    def __init__(self, client, on_success_callback):
        super().__init__()
        self.client = client
        self.on_success = on_success_callback
        self.current_dataset_id = None
        self.current_summary = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(12)

        # File selection
        file_layout = QHBoxLayout()
        self.select_btn = QPushButton('Select CSV File')
        self.select_btn.setProperty("kind", "secondary")
        self.select_btn.clicked.connect(self._select_file)
        self.upload_btn = QPushButton('Upload')
        self.upload_btn.setProperty("kind", "primary")
        self.upload_btn.clicked.connect(self._upload)
        self.upload_btn.setEnabled(False)
        self.file_label = QLabel('No file selected')
        self.file_label.setObjectName("Muted")
        file_layout.addWidget(self.select_btn)
        file_layout.addWidget(self.upload_btn)
        file_layout.addWidget(self.file_label)
        card_layout.addLayout(file_layout)

        self.filepath = None

        # Summary group
        summary_group = QGroupBox('Summary')
        summary_layout = QGridLayout()
        self.total_label = QLabel('Total Count: -')
        self.flowrate_label = QLabel('Avg Flowrate: -')
        self.pressure_label = QLabel('Avg Pressure: -')
        self.temp_label = QLabel('Avg Temperature: -')
        summary_layout.addWidget(self.total_label, 0, 0)
        summary_layout.addWidget(self.flowrate_label, 0, 1)
        summary_layout.addWidget(self.pressure_label, 1, 0)
        summary_layout.addWidget(self.temp_label, 1, 1)
        summary_group.setLayout(summary_layout)
        card_layout.addWidget(summary_group)

        # PDF download
        self.pdf_btn = QPushButton('Download PDF Report')
        self.pdf_btn.setProperty("kind", "primary")
        self.pdf_btn.clicked.connect(self._download_pdf)
        self.pdf_btn.setEnabled(False)
        card_layout.addWidget(self.pdf_btn)

        layout.addWidget(card)
        layout.addStretch()

    def _select_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV', '', 'CSV Files (*.csv)'
        )
        if path:
            self.filepath = path
            self.file_label.setText(path.split('/')[-1].split('\\')[-1])
            self.upload_btn.setEnabled(True)

    def _upload(self):
        if not self.filepath:
            return
        self.upload_btn.setEnabled(False)
        try:
            result = self.client.upload(self.filepath)
            dataset_id = result.get('dataset_id')
            summary = result.get('summary', {})

            # Fetch full dataset
            data_res = self.client.get_dataset(dataset_id)
            raw_data = data_res.get('raw_data', [])

            self.current_dataset_id = dataset_id
            self.current_summary = summary
            self._update_summary_labels(summary)
            self.pdf_btn.setEnabled(True)

            self.on_success(dataset_id, summary, raw_data)
        except Exception as e:
            QMessageBox.critical(self, 'Upload Failed', str(e))
        finally:
            self.upload_btn.setEnabled(True)

    def _update_summary_labels(self, summary):
        if not summary:
            return
        self.total_label.setText(f"Total Count: {summary.get('total_count', '-')}")
        self.flowrate_label.setText(f"Avg Flowrate: {summary.get('avg_flowrate', '-')}")
        self.pressure_label.setText(f"Avg Pressure: {summary.get('avg_pressure', '-')}")
        self.temp_label.setText(f"Avg Temperature: {summary.get('avg_temperature', '-')}")

    def set_loaded_data(self, summary, dataset_id):
        """Called when loading from history."""
        self.current_summary = summary
        self.current_dataset_id = dataset_id
        self._update_summary_labels(summary)
        self.pdf_btn.setEnabled(True)

    def _download_pdf(self):
        if not self.current_dataset_id:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, 'Save PDF', 'report.pdf', 'PDF Files (*.pdf)'
        )
        if path:
            try:
                self.client.download_pdf(self.current_dataset_id, path)
                QMessageBox.information(self, 'Success', f'PDF saved to {path}')
            except Exception as e:
                QMessageBox.critical(self, 'Download Failed', str(e))
