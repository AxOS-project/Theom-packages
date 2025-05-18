# INFO: This is a super fragile piece of code... Please be careful if editing it.

import subprocess
import json
from PyQt6.QtCore import QObject, pyqtSignal, QTimer, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QPushButton, QSizePolicy, QHBoxLayout
from PyQt6.QtGui import QPixmap, QImage

class NotificationListener(QObject):
    new_notification = pyqtSignal(str, str, QPixmap)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.seen_ids = set()
        self.timer.timeout.connect(self.fetch_notifications)
        
    def start(self):
        self.load_all_notifications()
        self.timer.start(5000)


    def load_all_notifications(self):
        try:
            result = subprocess.run(
                ['theom-notification-history', '--list'],
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
        except Exception as e:
            print(f"Failed to load notification history: {e}")
            return

        for notif_id, notif in data.items():
            self.emit_notification(notif_id, notif)
            self.seen_ids.add(notif_id)

    def fetch_notifications(self):
        try:
            result = subprocess.run(
                ['theom-notification-history', '--list'],
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
        except Exception as e:
            print(f"Failed to fetch notification history: {e}")
            return

        for notif_id, notif in data.items():
            if notif_id in self.seen_ids:
                continue
            self.emit_notification(notif_id, notif)
            self.seen_ids.add(notif_id)

    def emit_notification(self, notif_id, notif):
        heading = notif.get("heading", "")
        subheading = notif.get("subheading", "")
        text = f"{heading}: {subheading}" if subheading else heading

        pixmap = None
        for arr in notif.get("arrays", []):
            for entry in arr:
                if isinstance(entry, dict) and "image-data" in entry:
                    pixmap = self.create_pixmap_from_image_data(entry["image-data"])
                    break

        if pixmap is None:
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
        try:
            subprocess.run(
                ['theom-notification-history', '--delete', filename],
                check=True
            )
            self.seen_ids.discard(filename)
        except Exception as e:
            print(f"Failed to delete notification {filename}: {e}")

    def delete_all_notifications(self):
        try:
            result = subprocess.run(
                ['theom-notification-history', '--list'],
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
            for filename in data.keys():
                self.delete_notification(filename)
        except Exception as e:
            print(f"Failed to delete all notifications: {e}")



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

        self.delete_button = QPushButton("🗑️")
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

        title = QLabel("🔔 Notifications")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

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

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(container)

        self.listener = NotificationListener()
        self.listener.new_notification.connect(self.add_notification)
        self.listener.start()

    def add_notification(self, filename, text, pixmap):
        item = NotificationItem(filename, text, pixmap)
        item.delete_requested.connect(self.handle_delete_notification)
        self.notifications_layout.addWidget(item)

    def handle_delete_notification(self, filename):
        self.listener.delete_notification(filename)

        # Remove the widget from layout
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

