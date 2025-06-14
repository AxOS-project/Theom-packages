# INFO: This is a super fragile piece of code... Please be careful if editing it.

import argparse
import os
import sys
import subprocess
import json
from PyQt6.QtCore import QObject, pyqtSignal, QTimer, Qt, QProcess, QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QPushButton, QSizePolicy, QHBoxLayout, QApplication, QSpacerItem
from PyQt6.QtGui import QPixmap, QImage, QIcon, QWindow
from app_styles import stylesheet, stylesheet_light

class NotificationListener(QObject):
    new_notification = pyqtSignal(str, str, QPixmap)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.seen_ids = set()
        self.process = QProcess(self)

        self.timer.timeout.connect(self.fetch_notifications)
        self.process.finished.connect(self.handle_process_finished)

        self._current_action = None  # Track if we are loading notifications or something else

    def start(self):
        self.load_all_notifications()
        self.timer.start(5000)

    def load_all_notifications(self):
        if self.process.state() == QProcess.ProcessState.Running:
            return
        self._current_action = 'load_all'
        self.process.start('theom-notification-history', ['--list'])

    def fetch_notifications(self):
        if self.process.state() == QProcess.ProcessState.Running:
            # Skip if process busy
            return
        self._current_action = 'fetch'
        self.process.start('theom-notification-history', ['--list'])

    def handle_process_finished(self, exit_code, exit_status):
        if exit_code != 0:
            print(f"Process exited with error code {exit_code}")
            self._current_action = None
            return

        data_bytes = self.process.readAllStandardOutput()
        try:
            data_str = bytes(data_bytes).decode('utf-8')
            data = json.loads(data_str)
        except Exception as e:
            print(f"Failed to parse notification history: {e}")
            self._current_action = None
            return

        if self._current_action in ('load_all', 'fetch'):
            for notif_id, notif in data.items():
                if notif_id not in self.seen_ids:
                    self.emit_notification(notif_id, notif)
                    self.seen_ids.add(notif_id)
        else:
            # Unknown or no-op action
            pass

        self._current_action = None

    def emit_notification(self, notif_id, notif):
        heading = notif.get("heading", "")
        subheading = notif.get("subheading", "")
        text = f"{heading}: {subheading}" if subheading else heading

        pixmap = None

        icon_path = notif.get("icon_path", "")
        if icon_path and os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)

        if pixmap is None or pixmap.isNull():
            for arr in notif.get("arrays", []):
                for entry in arr:
                    if isinstance(entry, dict) and "image-data" in entry:
                        pixmap = self.create_pixmap_from_image_data(entry["image-data"])
                        break
                if pixmap:
                    break

        if pixmap is None or pixmap.isNull():
            pixmap = QPixmap(48, 48)
            pixmap.fill(Qt.GlobalColor.transparent)

        self.new_notification.emit(notif_id, text, pixmap)


    def create_pixmap_from_image_data(self, image_info):
        try:
            raw_data = image_info.get("data", [])
            width = image_info.get("width", 0)
            height = image_info.get("height", 0)

            if not raw_data or width == 0 or height == 0:
                return None

            img_bytes = bytes(raw_data)
            image = QImage(img_bytes, width, height, QImage.Format.Format_RGBA8888)
            if image.isNull():
                print("Failed to create image from image-data")
                return None

            return QPixmap.fromImage(image)
        except Exception as e:
            print(f"Error processing image-data: {e}")
            return None

    def delete_notification(self, filename):
        process = QProcess(self)
        process.finished.connect(lambda exit_code, status: self._handle_delete_finished(exit_code, status, filename, process))
        process.start('theom-notification-history', ['--delete', filename])

    def _handle_delete_finished(self, exit_code, exit_status, filename, process):
        if exit_code != 0:
            print(f"Failed to delete notification {filename}, exit code {exit_code}")
        else:
            self.seen_ids.discard(filename)
        process.deleteLater()

    def delete_all_notifications(self):
        process = QProcess(self)
        process.finished.connect(lambda exit_code, status: self._handle_delete_all_list_finished(exit_code, status, process))
        process.start('theom-notification-history', ['--list'])

    def _handle_delete_all_list_finished(self, exit_code, exit_status, process):
        if exit_code != 0:
            print(f"Failed to list notifications for deleting all, exit code {exit_code}")
            process.deleteLater()
            return

        data_bytes = process.readAllStandardOutput()
        try:
            data_str = bytes(data_bytes).decode('utf-8')
            data = json.loads(data_str)
        except Exception as e:
            print(f"Failed to parse notification history for delete all: {e}")
            process.deleteLater()
            return

        for filename in data.keys():
            self.delete_notification(filename)

        process.deleteLater()


class NotificationItem(QWidget):
    delete_requested = pyqtSignal(str)

    def __init__(self, filename, text, pixmap=None):
        super().__init__()
        self.filename = filename

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        self.image_label = QLabel()
        self.image_label.setFixedSize(48, 48)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        if pixmap:
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        else:
            fallback = QPixmap(48, 48)
            fallback.fill(Qt.GlobalColor.lightGray)
            self.image_label.setPixmap(fallback)

        self.text_label = QLabel(text)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon("/usr/lib/tnotifications/icons/red-trash-can-icon.svg"))
        self.delete_button.setFixedSize(32, 32)
        self.delete_button.clicked.connect(self.on_delete_clicked)

        layout.addWidget(self.image_label)
        layout.addWidget(self.text_label)
        layout.addWidget(self.delete_button)

    def on_delete_clicked(self):
        self.delete_requested.emit(self.filename)



class NotificationsWidget(QWidget):
    def __init__(self):
        super().__init__()

        container = QFrame()
        container.setFrameShape(QFrame.Shape.StyledPanel)

        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Notifications")
        #title.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        close_button = QPushButton()
        close_button.setIcon(QIcon("/usr/lib/tnotifications/icons/red-x-icon.svg"))
        close_button.setIconSize(QSize(16, 16))
        close_button.setFixedSize(24, 24)
        close_button.setStyleSheet("border: none; background: transparent;")
        close_button.clicked.connect(QApplication.quit)

        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)


        dummy_space = QWidget()
        dummy_space.setFixedSize(24, 24)
        dummy_space.setStyleSheet("background: transparent; border: none;")
        header_layout.insertWidget(0, dummy_space) 

        left_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        header_layout.addSpacerItem(left_spacer)

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        header_layout.addWidget(title)

        right_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        header_layout.addSpacerItem(right_spacer)

        close_button.setStyleSheet("""
            border: none;
            background: transparent;
            margin-right: 8px;
        """)
        header_layout.addWidget(close_button)

        main_layout.addLayout(header_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.notifications_container = QWidget()
        self.notifications_layout = QVBoxLayout(self.notifications_container)
        self.notifications_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.notifications_container)

        main_layout.addWidget(self.scroll)

        clear_button = QPushButton("Clear All")
        clear_button.clicked.connect(self.clear_notifications)
        main_layout.addWidget(clear_button)

        self.pauseNotifications = QPushButton("Pause Notifications")
        self.pauseNotifications.clicked.connect(self.toggle_notification)
        main_layout.addWidget(self.pauseNotifications)
        self.check_pn_status() # pn == pause notification

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(container)

        self.listener = NotificationListener()
        self.listener.new_notification.connect(self.add_notification)
        self.listener.start()

    def check_pn_status(self):
        process = subprocess.run(['dunstctl', 'is-paused'], stdout=subprocess.PIPE, text=True)
        is_paused = process.stdout.strip() == 'true'
        self.update_pn_button(is_paused)

    def add_notification(self, filename, text, pixmap):
        item = NotificationItem(filename, text, pixmap)
        item.delete_requested.connect(self.handle_delete_notification)
        self.notifications_layout.addWidget(item)

    def handle_delete_notification(self, filename):
        self.listener.delete_notification(filename)

        for i in range(self.notifications_layout.count()):
            item = self.notifications_layout.itemAt(i).widget()
            if isinstance(item, NotificationItem) and item.filename == filename:
                self.notifications_layout.takeAt(i)
                item.deleteLater()
                break

    def clear_notifications(self):
        self.listener.delete_all_notifications()

        while self.notifications_layout.count():
            item = self.notifications_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


    def toggle_notification(self):
        # Check current state
        process = subprocess.run(['dunstctl', 'is-paused'], stdout=subprocess.PIPE, text=True)
        is_paused = process.stdout.strip() == 'true'

        # Toggle state
        new_state = 'false' if is_paused else 'true'
        subprocess.run(['dunstctl', 'set-paused', new_state])

        # Update button appearance
        self.update_pn_button(new_state == 'true')

    def update_pn_button(self, is_paused):
        if is_paused:
            self.pauseNotifications.setStyleSheet("""
                background-color: #444;
                border: 2px solid #888;
                color: white;
                font-weight: bold;
            """)
        else:
            self.pauseNotifications.setStyleSheet("")

def current_theme():
    try:
        theme_output = subprocess.check_output(["theom-config", "appearance.theme"], text=True).strip().lower()
        return (theme_output)
    except Exception as e:
        print(f"Error detecting theme: {e}")
        return ("dark")

def parse_args():
    parser = argparse.ArgumentParser(description="Theom Notifications Viewer")
    parser.add_argument('--position', type=str, choices=["TL", "T", "TR", "L", "C", "R", "BL", "B", "BR"], default="TR",
                        help="Screen position (e.g. TL, T, TR, L, C, R, BL, B, BR)")
    parser.add_argument('--margin-x', type=int, default=10, help="Horizontal margin from screen edge")
    parser.add_argument('--margin-y', type=int, default=10, help="Vertical margin from screen edge")
    return parser.parse_args()

def compute_position(pos_str, window_geom, screen_geom, margin_x, margin_y):
    x = screen_geom.left()
    y = screen_geom.top()

    if "T" in pos_str:
        y = screen_geom.top() + margin_y
    elif "B" in pos_str:
        y = screen_geom.bottom() - window_geom.height() - margin_y
    else:  # vertical center
        y = screen_geom.top() + (screen_geom.height() - window_geom.height()) // 2

    if "L" in pos_str:
        x = screen_geom.left() + margin_x
    elif "R" in pos_str:
        x = screen_geom.right() - window_geom.width() - margin_x
    else:  # horizontal center
        x = screen_geom.left() + (screen_geom.width() - window_geom.width()) // 2

    return x, y


if __name__ == "__main__":
    args = parse_args()

    app = QApplication(sys.argv)
    window = NotificationsWidget()
    window.setWindowTitle("Theom Notifications")
    window.setFixedSize(600, 400)

    theme_output = current_theme()
    if theme_output == "light":
        app.setStyleSheet(stylesheet_light())
    else:
        app.setStyleSheet(stylesheet())

    window.show()

    screen_geometry = app.primaryScreen().availableGeometry()
    window_geometry = window.frameGeometry()

    x, y = compute_position(args.position, window_geometry, screen_geometry, args.margin_x, args.margin_y)
    window.move(x, y)

    sys.exit(app.exec())
