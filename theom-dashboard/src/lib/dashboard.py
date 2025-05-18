from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QFrame, QSizePolicy,
    QPushButton, QMessageBox, QSpacerItem
)
from PyQt6.QtCore import QTimer, Qt
import psutil
import time
import subprocess
import qtawesome as qta

from notifications import NotificationsWidget
from system import SystemWidget
from date_weather import DateWeatherWidget

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Theom Dashboard")
        self.resize(1200, 700)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.uptime_frame = QFrame()
        self.uptime_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.uptime_frame.setStyleSheet("""
            QFrame {
                background-color: #222222;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton {
                color: white;
                background-color: #444444;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        self.uptime_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        uptime_layout = QHBoxLayout(self.uptime_frame)
        uptime_layout.setContentsMargins(0, 0, 0, 0)

        self.uptime_label = QLabel("Uptime: calculating...")
        self.uptime_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white;")
        self.uptime_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        uptime_layout.addWidget(self.uptime_label)

        uptime_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.reboot_button = QPushButton("Reboot")
        self.reboot_button.clicked.connect(self.confirm_reboot)
        uptime_layout.addWidget(self.reboot_button)

        # Shutdown button
        self.shutdown_button = QPushButton("Shutdown")
        self.shutdown_button.clicked.connect(self.confirm_shutdown)
        uptime_layout.addWidget(self.shutdown_button)

        main_layout.addWidget(self.uptime_frame)

        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(15)
        main_layout.addLayout(columns_layout)

        self.notifications = NotificationsWidget()
        columns_layout.addWidget(self.notifications, 3)

        self.system = SystemWidget()
        columns_layout.addWidget(self.system, 2)

        self.date_weather = DateWeatherWidget()
        columns_layout.addWidget(self.date_weather, 2)

        self.uptime_timer = QTimer(self)
        self.uptime_timer.timeout.connect(self.update_uptime)
        self.uptime_timer.start(1000)

        self.update_uptime()

    def update_uptime(self):
        boot_time = psutil.boot_time()
        current_time = time.time()
        uptime_seconds = current_time - boot_time

        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)

        self.uptime_label.setText(f"Uptime: {hours}h {minutes}m {seconds}s")

    def confirm_reboot(self):
        reply = QMessageBox.question(
            self,
            "Confirm Reboot",
            "Are you sure you want to reboot the system?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.reboot_system()

    def confirm_shutdown(self):
        reply = QMessageBox.question(
            self,
            "Confirm Shutdown",
            "Are you sure you want to shutdown the system?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.shutdown_system()

    def reboot_system(self):
        try:
            subprocess.run(["systemctl", "reboot"], check=True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to reboot:\n{e}")

    def shutdown_system(self):
        try:
            subprocess.run(["systemctl", "poweroff"], check=True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to shutdown:\n{e}")
