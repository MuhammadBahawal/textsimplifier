"""
Enhanced chat widget with modern, beautiful, and responsive design.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
    QLineEdit, QPushButton, QLabel, QFrame, QSizePolicy,
    QGraphicsDropShadowEffect, QSpacerItem
)
from PySide6.QtCore import Qt, Signal, QTimer, QThread, QObject, QSize, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QIcon, QColor, QLinearGradient, QPalette
from typing import Optional

from src.message_bubble import MessageBubble, TypingIndicator
from src.language_detector import detect_language, Language
from src.network_checker import is_online
from src.simplifier_online import get_online_simplifier
from src.simplifier_offline import get_offline_simplifier


class SimplifierWorker(QObject):
    """Worker thread for text simplification."""
    finished = Signal(str, bool)  # result, is_online_mode
    
    def __init__(self, text: str):
        super().__init__()
        self.text = text
    
    def run(self):
        """Run the simplification."""
        result = None
        used_online = False
        
        # Try online first
        if is_online():
            online_simplifier = get_online_simplifier()
            if online_simplifier.is_available():
                result = online_simplifier.simplify(self.text)
                if result:
                    used_online = True
        
        # Fallback to offline
        if not result:
            offline_simplifier = get_offline_simplifier()
            result = offline_simplifier.simplify(self.text)
            used_online = False
        
        self.finished.emit(result or self.text, used_online)


class ChatWidget(QWidget):
    """Main chat widget with beautiful modern design."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark_theme = True
        self.typing_indicator: Optional[TypingIndicator] = None
        self.worker_thread: Optional[QThread] = None
        
        self._setup_ui()
        self._add_welcome_message()
    
    def _setup_ui(self):
        """Set up the chat widget UI with modern styling."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        self.header = self._create_header()
        layout.addWidget(self.header)
        
        # Chat area (scrollable)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.05);
                width: 10px;
                border-radius: 5px;
                margin: 4px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # Messages container with gradient background
        self.messages_container = QWidget()
        self.messages_container.setObjectName("messagesContainer")
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setContentsMargins(20, 20, 20, 20)
        self.messages_layout.setSpacing(12)
        self.messages_layout.addStretch()
        
        self.scroll_area.setWidget(self.messages_container)
        layout.addWidget(self.scroll_area, 1)
        
        # Input area
        self.input_area = self._create_input_area()
        layout.addWidget(self.input_area)
        
        self._apply_container_style()
    
    def _apply_container_style(self):
        """Apply modern container styling."""
        self.messages_container.setStyleSheet("""
            QWidget#messagesContainer {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0F0F1A, stop:0.5 #1A1A2E, stop:1 #16213E);
            }
        """)
    
    def _create_header(self) -> QWidget:
        """Create beautiful header with glass effect."""
        header = QFrame()
        header.setObjectName("chatHeader")
        header.setFixedHeight(80)
        
        # Glass morphism effect
        header.setStyleSheet("""
            QFrame#chatHeader {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(102, 126, 234, 0.2), 
                    stop:0.5 rgba(118, 75, 162, 0.2),
                    stop:1 rgba(102, 126, 234, 0.2));
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)
        
        # Left side - Logo and title
        left_layout = QVBoxLayout()
        left_layout.setSpacing(2)
        
        # Title with gradient text effect (using rich text)
        title = QLabel("✨ Phrase Simplifier")
        title.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 22px;
                font-weight: bold;
                font-family: 'Segoe UI', 'Inter', sans-serif;
            }
        """)
        left_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Simplify Urdu • Punjabi • Roman Urdu")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.6);
                font-size: 12px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        left_layout.addWidget(subtitle)
        
        layout.addLayout(left_layout)
        layout.addStretch()
        
        # Right side - Status indicator with glow
        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(12, 6, 12, 6)
        status_layout.setSpacing(8)
        
        # Status dot with glow
        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: #10B981; font-size: 10px;")
        status_layout.addWidget(self.status_dot)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #10B981;
                font-size: 13px;
                font-weight: 500;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        status_layout.addWidget(self.status_label)
        
        status_container.setStyleSheet("""
            QWidget {
                background: rgba(16, 185, 129, 0.15);
                border-radius: 16px;
                border: 1px solid rgba(16, 185, 129, 0.3);
            }
        """)
        
        layout.addWidget(status_container)
        
        return header
    
    def _create_input_area(self) -> QWidget:
        """Create beautiful input area with glass effect."""
        container = QFrame()
        container.setObjectName("inputArea")
        container.setMinimumHeight(100)
        container.setMaximumHeight(120)
        
        container.setStyleSheet("""
            QFrame#inputArea {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(26, 26, 46, 0.95),
                    stop:1 rgba(15, 15, 26, 0.98));
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        # Text input with modern styling
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("اپنا جملہ لکھیں... Type your sentence here...")
        self.text_input.setMinimumHeight(50)
        self.text_input.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(45, 45, 75, 0.8),
                    stop:1 rgba(35, 35, 60, 0.9));
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 25px;
                padding: 12px 24px;
                color: #FFFFFF;
                font-size: 15px;
                font-family: 'Segoe UI', 'Jameel Noori Nastaleeq', sans-serif;
            }
            QLineEdit:focus {
                border: 2px solid rgba(102, 126, 234, 0.8);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(55, 55, 85, 0.9),
                    stop:1 rgba(45, 45, 70, 0.95));
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.4);
            }
        """)
        self.text_input.returnPressed.connect(self._on_send)
        
        # Set font for multilingual support
        font = QFont("Segoe UI, Jameel Noori Nastaleeq, Noto Sans")
        font.setPointSize(13)
        self.text_input.setFont(font)
        
        layout.addWidget(self.text_input, 1)
        
        # Beautiful send button with gradient
        self.send_button = QPushButton("Send ➤")
        self.send_button.setMinimumSize(100, 50)
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7c8ff5, stop:1 #8b5cb8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5a6fd6, stop:1 #6a3d96);
            }
            QPushButton:disabled {
                background: #4A5568;
                color: #718096;
            }
        """)
        
        # Add shadow to button
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(102, 126, 234, 100))
        self.send_button.setGraphicsEffect(shadow)
        
        self.send_button.clicked.connect(self._on_send)
        layout.addWidget(self.send_button)
        
        return container
    
    def _add_welcome_message(self):
        """Add a beautiful welcome message."""
        welcome_text = """السلام علیکم! 👋

Welcome to Phrase Simplifier!

I can simplify your sentences in:
• اردو (Urdu)
• پنجابی (Punjabi)  
• Roman Urdu

Just type any complex sentence and I'll make it simpler and easier to understand! ✨"""
        
        self._add_message(welcome_text, is_user=False, is_rtl=False)
    
    def _add_message(self, text: str, is_user: bool, is_rtl: bool = False):
        """Add a message bubble to the chat with animation."""
        bubble = MessageBubble(text, is_user=is_user, is_rtl=is_rtl)
        bubble.update_theme(self.is_dark_theme)
        
        # Insert before the stretch
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, bubble)
        
        # Auto-scroll to bottom with smooth animation
        QTimer.singleShot(50, self._scroll_to_bottom)
    
    def _scroll_to_bottom(self):
        """Scroll the chat to the bottom smoothly."""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def _show_typing_indicator(self):
        """Show the typing indicator."""
        if self.typing_indicator is None:
            self.typing_indicator = TypingIndicator()
            self.messages_layout.insertWidget(self.messages_layout.count() - 1, self.typing_indicator)
            QTimer.singleShot(50, self._scroll_to_bottom)
    
    def _hide_typing_indicator(self):
        """Hide and remove the typing indicator."""
        if self.typing_indicator:
            self.messages_layout.removeWidget(self.typing_indicator)
            self.typing_indicator.deleteLater()
            self.typing_indicator = None
    
    def _on_send(self):
        """Handle send button click."""
        text = self.text_input.text().strip()
        if not text:
            return
        
        # Detect language and RTL
        language, _ = detect_language(text)
        is_rtl = language in (Language.URDU, Language.PUNJABI)
        
        # Add user message
        self._add_message(text, is_user=True, is_rtl=is_rtl)
        
        # Clear input
        self.text_input.clear()
        
        # Disable input while processing
        self.text_input.setEnabled(False)
        self.send_button.setEnabled(False)
        
        # Update status
        self.status_label.setText("Processing...")
        self.status_label.setStyleSheet("color: #F59E0B; font-size: 13px; font-weight: 500;")
        self.status_dot.setStyleSheet("color: #F59E0B; font-size: 10px;")
        
        # Show typing indicator
        self._show_typing_indicator()
        
        # Start simplification in background
        self._start_simplification(text)
    
    def _start_simplification(self, text: str):
        """Start the simplification process in a background thread."""
        self.worker_thread = QThread()
        self.worker = SimplifierWorker(text)
        self.worker.moveToThread(self.worker_thread)
        
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_simplification_complete)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        
        self.worker_thread.start()
    
    def _on_simplification_complete(self, result: str, is_online_mode: bool):
        """Handle completion of simplification."""
        # Hide typing indicator
        self._hide_typing_indicator()
        
        # Re-enable input
        self.text_input.setEnabled(True)
        self.send_button.setEnabled(True)
        self.text_input.setFocus()
        
        # Update status with beautiful styling
        if is_online_mode:
            self.status_label.setText("Online")
            self.status_label.setStyleSheet("color: #10B981; font-size: 13px; font-weight: 500;")
            self.status_dot.setStyleSheet("color: #10B981; font-size: 10px;")
        else:
            self.status_label.setText("Offline")
            self.status_label.setStyleSheet("color: #F59E0B; font-size: 13px; font-weight: 500;")
            self.status_dot.setStyleSheet("color: #F59E0B; font-size: 10px;")
        
        # Detect RTL for response
        language, _ = detect_language(result)
        is_rtl = language in (Language.URDU, Language.PUNJABI)
        
        # Add AI response
        self._add_message(result, is_user=False, is_rtl=is_rtl)
    
    def update_theme(self, is_dark: bool):
        """Update the chat theme."""
        self.is_dark_theme = is_dark
        
        if is_dark:
            self.messages_container.setStyleSheet("""
                QWidget#messagesContainer {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #0F0F1A, stop:0.5 #1A1A2E, stop:1 #16213E);
                }
            """)
            self.header.setStyleSheet("""
                QFrame#chatHeader {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(102, 126, 234, 0.2), 
                        stop:0.5 rgba(118, 75, 162, 0.2),
                        stop:1 rgba(102, 126, 234, 0.2));
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                }
            """)
            self.input_area.setStyleSheet("""
                QFrame#inputArea {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(26, 26, 46, 0.95),
                        stop:1 rgba(15, 15, 26, 0.98));
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                }
            """)
            self.text_input.setStyleSheet("""
                QLineEdit {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(45, 45, 75, 0.8),
                        stop:1 rgba(35, 35, 60, 0.9));
                    border: 2px solid rgba(102, 126, 234, 0.3);
                    border-radius: 25px;
                    padding: 12px 24px;
                    color: #FFFFFF;
                    font-size: 15px;
                }
                QLineEdit:focus {
                    border: 2px solid rgba(102, 126, 234, 0.8);
                }
                QLineEdit::placeholder {
                    color: rgba(255, 255, 255, 0.4);
                }
            """)
        else:
            self.messages_container.setStyleSheet("""
                QWidget#messagesContainer {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #F8FAFC, stop:0.5 #F1F5F9, stop:1 #E2E8F0);
                }
            """)
            self.header.setStyleSheet("""
                QFrame#chatHeader {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(102, 126, 234, 0.1), 
                        stop:0.5 rgba(118, 75, 162, 0.1),
                        stop:1 rgba(102, 126, 234, 0.1));
                    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                }
            """)
            self.input_area.setStyleSheet("""
                QFrame#inputArea {
                    background: #FFFFFF;
                    border-top: 1px solid rgba(0, 0, 0, 0.1);
                }
            """)
            self.text_input.setStyleSheet("""
                QLineEdit {
                    background: #F1F5F9;
                    border: 2px solid rgba(102, 126, 234, 0.3);
                    border-radius: 25px;
                    padding: 12px 24px;
                    color: #1A202C;
                    font-size: 15px;
                }
                QLineEdit:focus {
                    border: 2px solid rgba(102, 126, 234, 0.8);
                }
                QLineEdit::placeholder {
                    color: rgba(0, 0, 0, 0.4);
                }
            """)
        
        # Update title colors for light mode
        for child in self.header.findChildren(QLabel):
            if "Phrase Simplifier" in child.text():
                if is_dark:
                    child.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")
                else:
                    child.setStyleSheet("color: #1A202C; font-size: 22px; font-weight: bold;")
            elif "Simplify" in child.text():
                if is_dark:
                    child.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px;")
                else:
                    child.setStyleSheet("color: rgba(0, 0, 0, 0.5); font-size: 12px;")
        
        # Update all message bubbles
        for i in range(self.messages_layout.count()):
            item = self.messages_layout.itemAt(i)
            if item:
                widget = item.widget()
                if isinstance(widget, MessageBubble):
                    widget.update_theme(is_dark)
