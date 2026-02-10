"""
History tab: list of datasets with Load button.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QFrame,
)
from PyQt5.QtCore import pyqtSlot


class HistoryTab(QWidget):
    """Shows last 5 datasets. Load button fetches and updates other tabs."""

    def __init__(self, client, on_load_callback):
        super().__init__()
        self.client = client
        self.on_load = on_load_callback

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(10)

        self.refresh_btn = QPushButton('Refresh')
        self.refresh_btn.setProperty("kind", "secondary")
        self.refresh_btn.clicked.connect(self.refresh)
        card_layout.addWidget(self.refresh_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'File Name', 'Uploaded At', 'Action'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        card_layout.addWidget(self.table)

        layout.addWidget(card)

    @pyqtSlot()
    def refresh(self):
        """Fetch datasets and populate table."""
        self.refresh_btn.setEnabled(False)
        try:
            datasets = self.client.get_datasets()
            self.table.setRowCount(len(datasets))
            for i, ds in enumerate(datasets):
                self.table.setItem(i, 0, QTableWidgetItem(str(ds.get('id', ''))))
                self.table.setItem(i, 1, QTableWidgetItem(ds.get('file_name', '')))
                self.table.setItem(i, 2, QTableWidgetItem(str(ds.get('uploaded_at', ''))))

                load_btn = QPushButton('Load')
                load_btn.setProperty("kind", "primary")
                load_btn.setProperty('dataset_id', ds.get('id'))
                load_btn.clicked.connect(lambda checked, did=ds.get('id'): self._load(did))
                self.table.setCellWidget(i, 3, load_btn)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
        finally:
            self.refresh_btn.setEnabled(True)

    def _load(self, dataset_id):
        """Load dataset and summary, notify main window."""
        try:
            data_res = self.client.get_dataset(dataset_id)
            summary_res = self.client.get_summary(dataset_id)
            raw_data = data_res.get('raw_data', [])
            summary = summary_res
            self.on_load(dataset_id, summary, raw_data)
        except Exception as e:
            QMessageBox.critical(self, 'Load Failed', str(e))
