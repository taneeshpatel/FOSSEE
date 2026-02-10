"""
Entry point for the Chemical Equipment Visualizer desktop app.
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from api.client import APIClient
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from ui.theme import apply_theme


def main():
    # Better scaling on high-DPI displays
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    apply_theme(app)
    client = APIClient()

    login_window = LoginWindow(client)
    main_window = None

    def on_login_success(c):
        nonlocal main_window
        main_window = MainWindow(client)
        main_window.logout_requested.connect(on_logout)
        main_window.show()
        login_window.hide()

    def on_logout():
        main_window.close()
        main_window = None
        login_window.show()

    login_window.login_success.connect(on_login_success)
    login_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
