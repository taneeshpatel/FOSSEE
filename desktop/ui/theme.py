"""
Shared desktop theme to match the web UI.

Applies a modern dark theme with cyan accents, rounded cards, and clean widgets.
"""

from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtWidgets import QApplication


APP_QSS = """
/* App background */
QMainWindow, QWidget {
  font-family: "Segoe UI";
  color: #e8e8e8;
}

QMainWindow {
  background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
}

/* Card containers */
QFrame#Card {
  background-color: rgba(255, 255, 255, 13);
  border: 1px solid rgba(255, 255, 255, 26);
  border-radius: 12px;
}

QLabel#Title {
  color: #00d9ff;
  font-size: 18px;
  font-weight: 600;
}

QLabel#Muted {
  color: #b8b8b8;
}

/* Inputs */
QLineEdit {
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 51);
  background-color: rgba(0, 0, 0, 77);
  selection-background-color: rgba(0, 217, 255, 77);
}

QLineEdit:focus {
  border: 1px solid #00d9ff;
}

/* Buttons */
QPushButton {
  padding: 8px 14px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
}

QPushButton[kind="primary"] {
  background-color: #00d9ff;
  color: #1a1a2e;
}
QPushButton[kind="primary"]:hover {
  background-color: #00b8d9;
}
QPushButton[kind="primary"]:disabled {
  background-color: rgba(0, 217, 255, 77);
  color: rgba(26, 26, 46, 160);
}

QPushButton[kind="secondary"] {
  background-color: rgba(255, 255, 255, 38);
  color: #e8e8e8;
  border: 1px solid rgba(255, 255, 255, 51);
}
QPushButton[kind="secondary"]:hover {
  background-color: rgba(255, 255, 255, 51);
}

QPushButton[kind="danger"] {
  background-color: #e94560;
  color: #ffffff;
}
QPushButton[kind="danger"]:hover {
  background-color: #ff6b6b;
}

/* Tabs */
QTabWidget::pane {
  border: 1px solid rgba(255, 255, 255, 26);
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 8);
  top: -1px;
}

QTabBar::tab {
  background-color: rgba(255, 255, 255, 13);
  border: 1px solid rgba(255, 255, 255, 26);
  border-bottom: none;
  padding: 10px 14px;
  margin-right: 4px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  color: #b8b8b8;
}

QTabBar::tab:selected {
  color: #00d9ff;
  background-color: rgba(0, 217, 255, 18);
  border-color: rgba(0, 217, 255, 77);
}

/* Group boxes */
QGroupBox {
  border: 1px solid rgba(255, 255, 255, 26);
  border-radius: 10px;
  margin-top: 10px;
  padding: 12px;
  background-color: rgba(255, 255, 255, 8);
}

QGroupBox::title {
  subcontrol-origin: margin;
  subcontrol-position: top left;
  padding: 0 6px;
  color: #00d9ff;
  font-weight: 600;
}

/* Tables */
QTableWidget {
  background-color: rgba(0, 0, 0, 77);
  border: 1px solid rgba(255, 255, 255, 26);
  border-radius: 10px;
  gridline-color: rgba(255, 255, 255, 26);
  selection-background-color: rgba(0, 217, 255, 51);
}

QHeaderView::section {
  background-color: rgba(0, 217, 255, 38);
  color: #00d9ff;
  padding: 8px;
  border: none;
  font-weight: 600;
}
"""


def apply_theme(app: QApplication) -> None:
    """Apply the dark Fusion theme + QSS to the QApplication."""
    app.setStyle("Fusion")

    # Slightly larger, easy-to-read default font
    base_font = QFont("Segoe UI", 11)
    app.setFont(base_font)

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#1a1a2e"))
    palette.setColor(QPalette.WindowText, QColor("#e8e8e8"))
    palette.setColor(QPalette.Base, QColor("#0b1020"))
    palette.setColor(QPalette.AlternateBase, QColor("#111a33"))
    palette.setColor(QPalette.Text, QColor("#e8e8e8"))
    palette.setColor(QPalette.Button, QColor("#16213e"))
    palette.setColor(QPalette.ButtonText, QColor("#e8e8e8"))
    palette.setColor(QPalette.Highlight, QColor("#00d9ff"))
    palette.setColor(QPalette.HighlightedText, QColor("#1a1a2e"))
    app.setPalette(palette)

    app.setStyleSheet(APP_QSS)

