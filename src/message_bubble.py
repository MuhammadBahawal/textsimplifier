"""
Enhanced message bubble widget with modern, beautiful styling.
"""
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont, QColor

class MessageBubble(QWidget):
    """A beautifully styled chat message bubble with animations."""
    
    def __init__(self, message: str, is_user: bool = True, is_rtl: bool = False, parent=None):
        super().__init__(parent)
        self.message = message
        self.is_user = is_user
        self.is_rtl = is_rtl
        self._opacity = 1.0
        
        self._setup_ui()
        self._add_shadow()
    
    def _setup_ui(self):
        """Set up the message bubble UI with modern styling."""
        # Main horizontal layout for alignment
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 6, 16, 6)
        main_layout.setSpacing(0)
        
        # Create the bubble container
        self.bubble = QWidget()
        self.bubble.setObjectName("messageBubble")
        bubble_layout = QVBoxLayout(self.bubble)
        bubble_layout.setContentsMargins(16, 12, 16, 12)
        bubble_layout.setSpacing(4)
        
        # Message label
        self.message_label = QLabel(self.message)
        self.message_label.setWordWrap(True)
        self.message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.message_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        
        # Set text direction for RTL languages
        if self.is_rtl:
            self.message_label.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            self.message_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Set beautiful font
        font = QFont()
        font.setPointSize(12)
        font.setWeight(QFont.Weight.Normal)
        if self.is_rtl:
            font.setFamily("Jameel Noori Nastaleeq, Noto Nastaliq Urdu, Segoe UI, Arial")
        else:
            font.setFamily("Segoe UI, Inter, -apple-system, sans-serif")
        self.message_label.setFont(font)
        
        bubble_layout.addWidget(self.message_label)
        
        # Apply beautiful gradient styling
        if self.is_user:
            self.bubble.setStyleSheet("""
                QWidget#messageBubble {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #667eea, stop:1 #764ba2);
                    border-radius: 20px;
                    border-bottom-right-radius: 6px;
                }
                QLabel {
                    color: #FFFFFF;
                    background: transparent;
                    line-height: 1.5;
                }
            """)
            main_layout.addStretch()
            main_layout.addWidget(self.bubble)
        else:
            self.bubble.setStyleSheet("""
                QWidget#messageBubble {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #2D3748, stop:1 #1A202C);
                    border-radius: 20px;
                    border-bottom-left-radius: 6px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
                QLabel {
                    color: #E2E8F0;
                    background: transparent;
                    line-height: 1.5;
                }
            """)
            main_layout.addWidget(self.bubble)
            main_layout.addStretch()
        
        # Set maximum width for bubbles (responsive)
        self.bubble.setMaximumWidth(500)
        self.bubble.setMinimumWidth(100)
    
    def _add_shadow(self):
        """Add subtle shadow effect for depth."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        if self.is_user:
            shadow.setColor(QColor(102, 126, 234, 80))
        else:
            shadow.setColor(QColor(0, 0, 0, 60))
        self.bubble.setGraphicsEffect(shadow)
    
    def update_theme(self, is_dark: bool):
        """Update bubble colors based on theme."""
        if self.is_user:
            if is_dark:
                self.bubble.setStyleSheet("""
                    QWidget#messageBubble {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #667eea, stop:1 #764ba2);
                        border-radius: 20px;
                        border-bottom-right-radius: 6px;
                    }
                    QLabel {
                        color: #FFFFFF;
                        background: transparent;
                    }
                """)
            else:
                self.bubble.setStyleSheet("""
                    QWidget#messageBubble {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #4F46E5, stop:1 #7C3AED);
                        border-radius: 20px;
                        border-bottom-right-radius: 6px;
                    }
                    QLabel {
                        color: #FFFFFF;
                        background: transparent;
                    }
                """)
        else:
            if is_dark:
                self.bubble.setStyleSheet("""
                    QWidget#messageBubble {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #2D3748, stop:1 #1A202C);
                        border-radius: 20px;
                        border-bottom-left-radius: 6px;
                        border: 1px solid rgba(255, 255, 255, 0.1);
                    }
                    QLabel {
                        color: #E2E8F0;
                        background: transparent;
                    }
                """)
            else:
                self.bubble.setStyleSheet("""
                    QWidget#messageBubble {
                        background: #FFFFFF;
                        border-radius: 20px;
                        border-bottom-left-radius: 6px;
                        border: 1px solid #E2E8F0;
                    }
                    QLabel {
                        color: #1A202C;
                        background: transparent;
                    }
                """)


class TypingIndicator(QWidget):
    """Animated typing indicator with beautiful styling."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the typing indicator UI."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 6, 16, 6)
        main_layout.setSpacing(0)
        
        # Create the bubble container
        bubble = QWidget()
        bubble.setObjectName("typingBubble")
        bubble_layout = QHBoxLayout(bubble)
        bubble_layout.setContentsMargins(20, 14, 20, 14)
        bubble_layout.setSpacing(8)
        
        # Three animated dots
        for i in range(3):
            dot = QLabel("●")
            dot.setStyleSheet(f"""
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                font-size: 12px;
            """)
            dot.setObjectName(f"dot{i}")
            bubble_layout.addWidget(dot)
        
        bubble.setStyleSheet("""
            QWidget#typingBubble {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2D3748, stop:1 #1A202C);
                border-radius: 20px;
                border-bottom-left-radius: 6px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QLabel {
                color: #A0AEC0;
            }
        """)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 50))
        bubble.setGraphicsEffect(shadow)
        
        main_layout.addWidget(bubble)
        main_layout.addStretch()
