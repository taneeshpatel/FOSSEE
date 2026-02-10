"""
Login window for the desktop app.
"""
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QFrame,
)
from PyQt5.QtCore import pyqtSignal, Qt


class LoginWindow(QMainWindow):
    """Login window with username/password, Login and Register buttons."""
    login_success = pyqtSignal(object)  # Emits APIClient or user info

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.resize(520, 380)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 22, 22, 22)
        card_layout.setSpacing(14)

        title = QLabel("Chemical Equipment Visualizer")
        title.setObjectName("Title")
        subtitle = QLabel("Sign in to access your uploads and history.")
        subtitle.setObjectName("Muted")
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignLeft)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('Username')
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText('Password')
        self.password_edit.setEchoMode(QLineEdit.Password)
        form.addRow('Username:', self.username_edit)
        form.addRow('Password:', self.password_edit)
        card_layout.addLayout(form)

        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton('Login')
        self.login_btn.setProperty("kind", "primary")
        self.login_btn.clicked.connect(self._on_login)
        self.register_btn = QPushButton('Register')
        self.register_btn.setProperty("kind", "secondary")
        self.register_btn.clicked.connect(self._on_register)
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.register_btn)
        card_layout.addLayout(btn_layout)

        layout.addStretch(1)
        layout.addWidget(card)
        layout.addStretch(2)

    def _on_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password.')
            return

        self.login_btn.setEnabled(False)
        self.register_btn.setEnabled(False)
        try:
            self.client.login(username, password)
            self.login_success.emit(self.client)
        except Exception as e:
            error_msg = str(e)
            QMessageBox.critical(
                self,
                'Login Failed',
                error_msg if error_msg else 'Invalid credentials',
            )
        finally:
            self.login_btn.setEnabled(True)
            self.register_btn.setEnabled(True)

    def _on_register(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password.')
            return

        self.login_btn.setEnabled(False)
        self.register_btn.setEnabled(False)
        try:
            self.client.register(username, password)
            # Auto-login after registration
            self.client.login(username, password)
            self.login_success.emit(self.client)
        except Exception as e:
            error_msg = str(e)
            QMessageBox.critical(
                self,
                'Registration Failed',
                error_msg if error_msg else 'Registration failed',
            )
        finally:
            self.login_btn.setEnabled(True)
            self.register_btn.setEnabled(True)
