from mpd import MPDClient, CommandError, ConnectionError
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QProgressBar, QSizePolicy,
    QPushButton, QHBoxLayout, QStyle
)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QPainter
import psutil
import subprocess

class CenteredTextProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTextVisible(False)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(self.palette().color(self.foregroundRole()))
        rect = self.rect()

        text = self.text()
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

        painter.end()




class MusicPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.client = MPDClient()
        self.connected = False
        self.connect_to_mpd()

        button_css = """
            QPushButton {
                background-color: #2a2e32;
                color: #b9c7cb;
                padding: 10px 16px;
                border: 1px solid #2f3336;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3a4045;
            }
            QPushButton:pressed {
                background-color: #1e2225;
            }
            QPushButton:disabled {
                background-color: #2b2d2f;
                color: #777;
                border: 1px solid #333;
            }
        """

        self.track_label = QLabel("No track playing")
        self.track_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.track_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.setCheckable(True)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.play_pause_button.setStyleSheet(button_css)

        self.prev_button = QPushButton("⏮ Prev")
        self.prev_button.clicked.connect(self.prev_track)
        self.prev_button.setStyleSheet(button_css)

        self.next_button = QPushButton("Next ⏭")
        self.next_button.clicked.connect(self.next_track)
        self.next_button.setStyleSheet(button_css)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.play_pause_button)
        controls_layout.addWidget(self.next_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.track_label)
        layout.addLayout(controls_layout)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_track_info)
        self.update_timer.start(1000)

    def connect_to_mpd(self):
        try:
            self.client.connect("localhost", 6600)
            self.connected = True
        except ConnectionError:
            self.track_label.setText("Failed to connect to MPD")
            self.connected = False

    def toggle_play_pause(self, checked):
        if not self.connected:
            self.track_label.setText("Not connected to MPD")
            return

        try:
            status = self.client.status()
            state = status.get('state')

            if state == 'play':
                self.client.pause(1)
                self.play_pause_button.setText("Play")
            else:
                self.client.play()
                self.play_pause_button.setText("Pause")
        except CommandError as e:
            self.track_label.setText(f"MPD error: {str(e)}")

    def prev_track(self):
        if not self.connected:
            return
        try:
            self.client.previous()
            self.update_track_info()
        except CommandError as e:
            self.track_label.setText(f"MPD error: {str(e)}")

    def next_track(self):
        if not self.connected:
            return
        try:
            self.client.next()
            self.update_track_info()
        except CommandError as e:
            self.track_label.setText(f"MPD error: {str(e)}")

    def update_track_info(self):
        if not self.connected:
            return
        try:
            status = self.client.status()
            if status.get('state') == 'play':
                current = self.client.currentsong()
                title = current.get('title', 'Unknown Title')
                self.track_label.setText(f"Playing: {title}")
                self.play_pause_button.setChecked(True)
                self.play_pause_button.setText("Pause")
            else:
                self.track_label.setText("Paused")
                self.play_pause_button.setChecked(False)
                self.play_pause_button.setText("Play")
        except CommandError:
            pass



class SystemWidget(QWidget):
    weather_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        container = QFrame()
        container.setFrameShape(QFrame.Shape.StyledPanel)

        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(10)

        title = QLabel("System Stats & Controls")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        button_container = QFrame()
        button_container.setFrameShape(QFrame.Shape.StyledPanel)
        button_container.setObjectName("wbButtonBox")
        #button_container.setStyleSheet(
        #    "background-color: #333333; border-radius: 8px; padding: 10px;"
        #)
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)

        self.wifi_button = QPushButton("📶 WiFi")
        self.wifi_button.setCheckable(False)
        self.wifi_button.setStyleSheet("""
            QPushButton {
                font-size: 14px; 
                padding: 8px 16px; 
                border-radius: 5px; 
                background-color: #555555; 
                color: white;
            }
            QPushButton:hover {
                background-color: #4caf50;
            }
        """)
        self.wifi_button.clicked.connect(self.open_wifi_manager)
        button_layout.addWidget(self.wifi_button)

        self.bluetooth_button = QPushButton("🟦 Bluetooth")
        self.bluetooth_button.setCheckable(False)
        self.bluetooth_button.setStyleSheet("""
            QPushButton {
                font-size: 14px; 
                padding: 8px 16px; 
                border-radius: 5px; 
                background-color: #555555; 
                color: white;
            }
            QPushButton:hover {
                background-color: #2196f3;
            }
        """)
        self.bluetooth_button.clicked.connect(self.open_bluetooth_manager)
        button_layout.addWidget(self.bluetooth_button)

        main_layout.addWidget(button_container)

        # Music Player inside a QFrame, right below buttons
        self.music_frame = QFrame()
        self.music_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.music_frame.setObjectName("MusicBox")
        #self.music_frame.setStyleSheet(
        #    "background-color: #333333; border-radius: 8px; padding: 10px;"
        #)
        music_layout = QVBoxLayout(self.music_frame)
        self.music_player = MusicPlayerWidget()
        music_layout.addWidget(self.music_player)
        music_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.music_frame)

        # System Stats Section (CPU, RAM, Disk) below music player
        self.stats_container = QFrame()
        self.stats_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.stats_container.setObjectName("SystemStatsBox")
        #self.stats_container.setStyleSheet(
        #    "background-color: #333333; border-radius: 8px; padding: 10px;"
        #)
        stats_layout = QVBoxLayout(self.stats_container)

        self.cpu_label = QLabel("🖥️ CPU Usage:")
        self.cpu_label.setStyleSheet("font-size: 14px; background-color: transparent;")
        stats_layout.addWidget(self.cpu_label)

        self.cpu_progress = CenteredTextProgressBar()
        self.cpu_progress.setRange(0, 100)
        stats_layout.addWidget(self.cpu_progress)

        self.ram_label = QLabel("🧠 RAM Usage:")
        self.ram_label.setStyleSheet("font-size: 14px; margin-top: 10px; background-color: transparent")
        stats_layout.addWidget(self.ram_label)

        self.ram_progress = CenteredTextProgressBar()
        self.ram_progress.setRange(0, 100)
        stats_layout.addWidget(self.ram_progress)

        self.disk_label = QLabel("💾 Disk Usage:")
        self.disk_label.setStyleSheet("font-size: 14px; margin-top: 10px; background-color: transparent")
        stats_layout.addWidget(self.disk_label)

        self.disk_progress = CenteredTextProgressBar()
        self.disk_progress.setRange(0, 100)
        stats_layout.addWidget(self.disk_progress)

        main_layout.addWidget(self.stats_container)

        # Setup timers
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_system_stats)
        self.stats_timer.start(1000)

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(container)

    def open_wifi_manager(self):
        try:
            subprocess.Popen(["nm-connection-editor"])
        except Exception as e:
            print(f"Failed to launch nm-connection-editor: {e}")

    def open_bluetooth_manager(self):
        try:
            subprocess.Popen(["blueman-manager"])
        except Exception as e:
            print(f"Failed to launch blueman-manager: {e}")

    def update_system_stats(self):
        cpu_percent = psutil.cpu_percent(interval=None)
        ram_percent = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        self.cpu_progress.setValue(int(cpu_percent))
        self.cpu_progress.setFormat(f"{cpu_percent:.1f}%")

        self.ram_progress.setValue(int(ram_percent))
        self.ram_progress.setFormat(f"{ram_percent:.1f}%")

        self.disk_progress.setValue(int(disk_usage))
        self.disk_progress.setFormat(f"{disk_usage:.1f}%")
