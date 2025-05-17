from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QSpacerItem, QSizePolicy
)

from notifications import NotificationsWidget
from networks import NetworksWidget
from date_weather import DateWeatherWidget

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Theom Dashboard")
        self.resize(1000, 600)

        # Layouts
        main_layout = QHBoxLayout(self)
        self.setLayout(main_layout)

        # Notification column
        self.notifications = NotificationsWidget()
        main_layout.addWidget(self.notifications, 3)

        # Network & Bluetooth column
        self.networks = NetworksWidget()
        main_layout.addWidget(self.networks, 2)

        # Date + Weather column
        self.date_weather = DateWeatherWidget()
        main_layout.addWidget(self.date_weather, 2)
