"""
Beautiful main application window for Phrase Simplifier.
Features: Modern styling, responsive design, theme switching.
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFrame, QDialog, QLineEdit,
    QFormLayout, QDialogButtonBox, QMessageBox,
    QGraphicsDropShadowEffect, QApplication
)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, QFont, QAction, QColor, QScreen

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chat_widget import ChatWidget
from config import get_theme, set_theme, get_api_key, set_api_key


class SettingsDialog(QDialog):
    """Beautiful settings dialog with modern styling."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Settings")
        self.setFixedSize(500, 280)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1A1A2E, stop:1 #16213E);
                border-radius: 16px;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 14px;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit {
                background: rgba(45, 45, 75, 0.8);
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 12px;
                padding: 12px 16px;
                color: #FFFFFF;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: rgba(102, 126, 234, 0.8);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7c8ff5, stop:1 #8b5cb8);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🔑 API Configuration")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(title)
        
        # API Key section
        api_label = QLabel("Google Gemini API Key:")
        layout.addWidget(api_label)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your API key for online mode...")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setText(get_api_key())
        layout.addWidget(self.api_key_input)
        
        # Info label
        info_label = QLabel("💡 Get a FREE API key from ai.google.dev")
        info_label.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 12px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: rgba(75, 75, 95, 0.8);
            }
            QPushButton:hover {
                background: rgba(95, 95, 115, 0.9);
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("✓ Save")
        save_btn.clicked.connect(self._save_settings)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def _save_settings(self):
        """Save settings and close dialog."""
        api_key = self.api_key_input.text().strip()
        set_api_key(api_key)
        self.accept()


class MainWindow(QMainWindow):
    """Beautiful main application window with modern design."""
    
    def __init__(self):
        super().__init__()
        self.is_dark_theme = get_theme() == 'dark'
        
        self._setup_window()
        self._setup_ui()
        self._apply_theme()
    
    def _setup_window(self):
        """Configure the main window with responsive sizing."""
        self.setWindowTitle("✨ Phrase Simplifier - Urdu | Punjabi | Roman Urdu")
        
        # Get screen size for responsive sizing
        screen = QApplication.primaryScreen().availableGeometry()
        
        # Set minimum and responsive sizing
        self.setMinimumSize(600, 500)
        
        # Default size is 60% of screen, capped at max values
        default_width = min(int(screen.width() * 0.5), 900)
        default_height = min(int(screen.height() * 0.75), 800)
        self.resize(default_width, default_height)
        
        # Center on screen
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
        # Window flags for modern appearance
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint)
    
    def _setup_ui(self):
        """Set up the main UI with beautiful styling."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = self._create_toolbar()
        layout.addWidget(toolbar)
        
        # Chat widget
        self.chat_widget = ChatWidget()
        layout.addWidget(self.chat_widget, 1)
    
    def _create_toolbar(self) -> QWidget:
        """Create beautiful toolbar with glass effect."""
        toolbar = QFrame()
        toolbar.setObjectName("toolbar")
        toolbar.setFixedHeight(56)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(12)
        
        layout.addStretch()
        
        # Theme toggle button with beautiful styling
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedSize(44, 44)
        self.theme_btn.setToolTip("Toggle Dark/Light Theme")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.setStyleSheet("""
            QPushButton {
                background: rgba(102, 126, 234, 0.2);
                border: 1px solid rgba(102, 126, 234, 0.3);
                border-radius: 22px;
                font-size: 20px;
            }
            QPushButton:hover {
                background: rgba(102, 126, 234, 0.4);
                border-color: rgba(102, 126, 234, 0.6);
            }
        """)
        self.theme_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(self.theme_btn)
        
        # Settings button
        settings_btn = QPushButton("⚙️")
        settings_btn.setFixedSize(44, 44)
        settings_btn.setToolTip("Settings")
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.setStyleSheet("""
            QPushButton {
                background: rgba(102, 126, 234, 0.2);
                border: 1px solid rgba(102, 126, 234, 0.3);
                border-radius: 22px;
                font-size: 20px;
            }
            QPushButton:hover {
                background: rgba(102, 126, 234, 0.4);
                border-color: rgba(102, 126, 234, 0.6);
            }
        """)
        settings_btn.clicked.connect(self._show_settings)
        layout.addWidget(settings_btn)
        
        return toolbar
    
    def _toggle_theme(self):
        """Toggle between dark and light theme."""
        self.is_dark_theme = not self.is_dark_theme
        set_theme('dark' if self.is_dark_theme else 'light')
        self._apply_theme()
        self.chat_widget.update_theme(self.is_dark_theme)
    
    def _apply_theme(self):
        """Apply beautiful theme styling."""
        if self.is_dark_theme:
            self.theme_btn.setText("🌙")
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #0F0F1A, stop:1 #1A1A2E);
                }
                QFrame#toolbar {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(15, 15, 26, 0.95),
                        stop:0.5 rgba(26, 26, 46, 0.95),
                        stop:1 rgba(15, 15, 26, 0.95));
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                }
            """)
        else:
            self.theme_btn.setText("☀️")
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #F8FAFC, stop:1 #E2E8F0);
                }
                QFrame#toolbar {
                    background: #FFFFFF;
                    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                }
            """)
    
    def _show_settings(self):
        """Show the settings dialog."""
        dialog = SettingsDialog(self)
        dialog.exec()
    
    def resizeEvent(self, event):
        """Handle window resize for responsiveness."""
        super().resizeEvent(event)
        # The UI automatically adapts due to layout stretch factors
