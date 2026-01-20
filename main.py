"""
Phrase Simplifier - Windows Desktop Application
A chatbot that simplifies text in Urdu, Punjabi, and Roman Urdu.

Run this file to start the application:
    python main.py
"""
import sys
import os

# Ensure we can import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase, QIcon
from PySide6.QtCore import Qt

from src.app import MainWindow
from config import APP_NAME, APP_VERSION


def setup_fonts():
    """Set up fonts for multilingual support."""
    # Add system fonts that support Urdu/Arabic script
    # These are commonly available on Windows
    preferred_fonts = [
        "Segoe UI",
        "Noto Sans",
        "Noto Nastaliq Urdu", 
        "Jameel Noori Nastaleeq",
        "Arial Unicode MS"
    ]
    
    # Create a font that falls back through the list
    app_font = QFont("Segoe UI")
    app_font.setPointSize(10)
    app_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    
    return app_font


def main():
    """Main entry point for the application."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("PhraseSimplifier")
    
    # Set up fonts
    app_font = setup_fonts()
    app.setFont(app_font)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = MainWindow()
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'icon.png')
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
        window.setWindowIcon(app_icon)
    
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
