from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt

class NetworksWidget(QWidget):
    def __init__(self):
        super().__init__()

        container = QFrame()
        container.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(container)
        layout.setSpacing(10)

        title = QLabel("📶 Network & Bluetooth")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        wifi_button = QPushButton("Toggle Wi-Fi")
        bluetooth_button = QPushButton("Toggle Bluetooth")

        layout.addWidget(wifi_button)
        layout.addWidget(bluetooth_button)

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(container)
