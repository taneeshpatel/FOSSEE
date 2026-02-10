"""
Main window with tabs: Upload & Summary, Charts, History.
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QMessageBox, QMenuBar, QAction,
)
from PyQt5.QtCore import pyqtSignal

from .upload_tab import UploadTab
from .chart_tab import ChartTab
from .history_tab import HistoryTab


class MainWindow(QMainWindow):
    """Main window with QTabWidget and shared APIClient."""
    logout_requested = pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.current_dataset_id = None
        self.current_summary = None
        self.current_data = []

        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setMinimumSize(1100, 720)
        self.resize(1280, 800)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBar().setExpanding(False)
        self.upload_tab = UploadTab(client, self._on_data_updated)
        self.chart_tab = ChartTab()
        self.history_tab = HistoryTab(client, self._on_load_from_history)

        self.tabs.addTab(self.upload_tab, 'Upload & Summary')
        self.tabs.addTab(self.chart_tab, 'Charts')
        self.tabs.addTab(self.history_tab, 'History')

        layout.addWidget(self.tabs)

        # Menu bar with Logout
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self._on_logout)
        file_menu.addAction(logout_action)

    def _on_data_updated(self, dataset_id, summary, data):
        """Called when new data is uploaded or loaded."""
        self.current_dataset_id = dataset_id
        self.current_summary = summary
        self.current_data = data or []
        self.chart_tab.update_charts(summary)
        self.history_tab.refresh()

    def _on_load_from_history(self, dataset_id, summary, data):
        """Called when user loads a dataset from history."""
        self._on_data_updated(dataset_id, summary, data)
        self.upload_tab.set_loaded_data(summary, dataset_id)
        self.tabs.setCurrentIndex(0)

    def _on_logout(self):
        try:
            self.client.logout()
        except Exception:
            pass
        self.logout_requested.emit()
