#---------------------------------------------------------------------------------------------
# Libraries - Core Functionality
#---------------------------------------------------------------------------------------------
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QFrame, QSizePolicy


#---------------------------------------------------------------------------------------------
# Class - Wrapper For Widgets
#---------------------------------------------------------------------------------------------

class CustomWindow(QWidget):
    def __init__(self, child_widget, title="Custom Window"):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)         # Remove the OS-provided title bar
        self.setStyleSheet("background-color: black;")      # Set window background color

        # Title bar
        self.title_bar = QFrame()
        self.title_bar.setStyleSheet("background-color: #333333; color: white;")
        self.title_bar_layout = QHBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: white;")
        self.title_bar_layout.addWidget(self.title_label)

        # Add minimize and close buttons
        self.minimize_button = QPushButton("-")
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.setStyleSheet("background-color: #555555; color: white; border: none;")
        self.minimize_button.clicked.connect(self.showMinimized)

        self.close_button = QPushButton("x")
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet("background-color: #555555; color: white; border: none;")
        self.close_button.clicked.connect(self.close)

        self.title_bar_layout.addWidget(self.minimize_button)
        self.title_bar_layout.addWidget(self.close_button)
        self.title_bar.setLayout(self.title_bar_layout)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_bar)
        child_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)        
        self.layout.addWidget(child_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)      # Remove default margins
        self.setLayout(self.layout)
