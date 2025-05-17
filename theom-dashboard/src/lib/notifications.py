# NOTE: Be careful when interacting with this code. Idk how it works, its like barely stuck together with duct tape.

# Check out this blog to learn more about notifications: https://www.johnshaughnessy.com/blog/posts/how_do_notifications_work

import threading
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame,
    QScrollArea, QSizePolicy, QHBoxLayout
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import pyqtSignal, QObject, Qt, QTimer


def convert_hex_to_bytes(byte_lines):
    byte_values = []
    for line in byte_lines:
        parts = line.strip().split()
        for part in parts:
            if not part:
                continue
            try:
                val = int(part, 16)
                byte_values.append(val)
            except ValueError:
                pass
    return bytes(byte_values)


class NotificationListener(QObject):
    new_notification = pyqtSignal(str)
    new_image = pyqtSignal(bytes, dict)

    def __init__(self):
        super().__init__()
        self._running = True

    def start(self):
        proc = subprocess.Popen(
            ['dbus-monitor', "interface='org.freedesktop.Notifications'"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        collecting = False
        collected_strings = []

        collecting_array = False
        collecting_dict = False
        current_dict = {}
        current_key = None

        parsing_image_data = False
        collecting_image_bytes = False
        collected_image_bytes = []
        collected_image_metadata = {}

        metadata_keys = ['width', 'height', 'rowstride', 'has_alpha', 'bits_per_sample', 'channels']
        metadata_index = 0

        for line in proc.stdout:
            if not self._running:
                proc.terminate()
                break

            line = line.strip()

            # --- IMAGE DATA PARSING --- DO NOT TOUCH THIS, IT COULD BREAK!!
            if parsing_image_data:
                if collecting_image_bytes:
                    if line == ']':
                        # finished collecting bytes
                        collecting_image_bytes = False
                        parsing_image_data = False

                        # Convert hex lines to bytes
                        image_bytes = convert_hex_to_bytes(collected_image_bytes)

                        # Emit with metadata
                        self.new_image.emit(image_bytes, collected_image_metadata)

                        # reset for next image
                        collected_image_bytes = []
                        collected_image_metadata = {}
                        metadata_index = 0
                    else:
                        collected_image_bytes.append(line)
                    continue  # continue reading lines

                # parse image metadata fields
                if line.startswith('int32 ') or line.startswith('boolean '):
                    key = metadata_keys[metadata_index]

                    if line.startswith('int32 '):
                        val = int(line.split()[1])
                    elif line.startswith('boolean '):
                        val = line.split()[1].lower() == 'true'

                    collected_image_metadata[key] = val
                    metadata_index += 1
                elif line.startswith('array of bytes ['):
                    collecting_image_bytes = True
                continue  # continue reading lines

            # --- NORMAL PARSING ---

            if line.startswith('array ['):
                collecting_array = True
                continue

            if collecting_array:
                if line.startswith('dict entry('):
                    collecting_dict = True
                    current_dict = {}
                    continue

            if collecting_dict:
                if line.startswith('string "image-data"'):
                    current_key = 'image-data'
                    continue
                elif line.startswith('string "'):
                    current_key = line.split('"')[1]
                    continue

            if line.startswith('variant'):
                if current_key == 'image-data' and line.endswith('struct {'):
                    # start parsing image data struct
                    parsing_image_data = True
                    collected_image_bytes = []
                    collected_image_metadata = {}
                    metadata_index = 0
                    continue
                else:
                    parts = line.split(None, 2)
                    value = parts[2] if len(parts) > 2 else None
                    current_dict[current_key] = value
                    continue

            # Detect notification start
            if line.startswith('method call') and 'member=Notify' in line:
                collecting = True
                notification_emitted = False
                collected_strings = []
                continue

            if collecting:
                if line.startswith('string "'):
                    value = line.split('"')[1]
                    collected_strings.append(value)
                else: print(f"Skipped line: {line}")

                # After collecting 4 strings (app_name, icon, summary, body)
                if len(collected_strings) >= 4:
                    notification_emitted = True
                    app_icon = collected_strings[1]
                    title = collected_strings[2]
                    body = collected_strings[3]

                    if body:
                        text = f"{title}: {body}"
                    else:
                        text = title

                    if app_icon:
                        text += f" (Icon: {app_icon})"

                    self.new_notification.emit(text)
                    # FULL RESET HERE
                    collecting = False
                    collecting_array = False
                    collecting_dict = False
                    parsing_image_data = False
                    collecting_image_bytes = False
                    current_dict = {}
                    current_key = None
                    collected_strings = []
                    collected_image_bytes = []
                    collected_image_metadata = {}
                    metadata_index = 0

    def stop(self):
        self._running = False

class NotificationItem(QWidget):
    def __init__(self, text, pixmap=None, parent=None):
        super().__init__(parent)
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


        self.text_label = QLabel(text)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.image_label)
        layout.addWidget(self.text_label)


class NotificationsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.listener = NotificationListener()

        self.debug_window = ImageDebugWindow()
        self.debug_window.show()

        self.listener.new_image.connect(self.debug_window.display_image)
        self.listener.new_notification.connect(self.delayed_add_notification)
        self.listener.new_image.connect(self.store_image)

        self.thread = threading.Thread(target=self.listener.start, daemon=True)
        self.thread.start()


        self.pending_image = None  # buffer for last image

        container = QFrame()
        container.setFrameShape(QFrame.Shape.StyledPanel)

        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(10)

        title = QLabel("🔔 Notifications")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Scroll Area + container for notification items
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
        

    def store_image(self, image_bytes, metadata):
        width = metadata.get('width', 128)
        height = metadata.get('height', 128)
        rowstride = metadata.get('rowstride', width * 4)
        bits = metadata.get('bits_per_sample', 8)
        chans = metadata.get('channels', 4)
        has_alpha = metadata.get('has_alpha', True)

        # Calculate expected rowstride
        calculated_rs = int(width * chans * (bits / 8))

        fmt = QImage.Format.Format_RGBA8888 if has_alpha else QImage.Format.Format_RGB888

        # Try creating QImage using metadata values first
        image = QImage(image_bytes, width, height, rowstride, fmt)
        if image.isNull():
            print("QImage creation failed with original metadata, trying with swapped width/height and calculated rowstride...")

            # Try swapping width and height
            # Also override rowstride with calculated value
            image = QImage(image_bytes, height, width, calculated_rs, fmt)
            if image.isNull():
                print("QImage creation failed again after swapping dimensions and overriding rowstride.")
                self.pending_image = None
                return
            else:
                print(f"Success with swapped dimensions: width={height}, height={width}, rowstride={calculated_rs}")
        else:
            # Check if metadata rowstride is incorrect and override if needed
            if rowstride != calculated_rs:
                print(f"Metadata rowstride ({rowstride}) differs from calculated ({calculated_rs}), recreating QImage with calculated rowstride.")
                image = QImage(image_bytes, width, height, calculated_rs, fmt)
                if image.isNull():
                    print("QImage creation failed after correcting rowstride.")
                    self.pending_image = None
                    return

        pixmap = QPixmap.fromImage(image)
        self.pending_image = pixmap

    def delayed_add_notification(self, notification_text: str, timeout=5000):
        print("Notification moved to delay")
        """
        Wait until self.pending_image is available or timeout expires,
        then call add_notification.
        """
        start_time = 0

        def check_image_and_add():
            nonlocal start_time
            if self.pending_image:
                self.add_notification(notification_text)
            else:
                start_time += 100
                if start_time < timeout:
                    QTimer.singleShot(100, check_image_and_add)
                else:
                    print(f"Timeout waiting for image, adding notification without image: {notification_text}")
                    self.add_notification(notification_text)

        check_image_and_add()

    def add_notification(self, notification_text: str):
        if self.pending_image:
            pixmap = self.pending_image
        else:
            print(f"Adding notification WITHOUT image: {notification_text}")
            # Create a simple fallback pixmap (e.g., gray square) so you can see an image placeholder
            fallback_pixmap = QPixmap(48, 48)
            fallback_pixmap.fill(Qt.GlobalColor.lightGray)
            pixmap = fallback_pixmap

        item = NotificationItem(notification_text, pixmap=pixmap)
        self.pending_image = None  # reset after use

        self.notifications_layout.addWidget(item)


    def clear_notifications(self):
        while self.notifications_layout.count():
            item = self.notifications_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def closeEvent(self, event):
        self.listener.stop()
        super().closeEvent(event)


class ImageDebugWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notification Image Debugger")
        self.label = QLabel("Waiting for image...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.resize(200, 200)

    def display_image(self, image_bytes, metadata):
        width = metadata.get('width', 128)
        height = metadata.get('height', 128)
        rowstride = metadata.get('rowstride', width * 4)
        has_alpha = metadata.get('has_alpha', True)

        fmt = QImage.Format.Format_RGBA8888 if has_alpha else QImage.Format.Format_RGB888
        image = QImage(image_bytes, width, height, rowstride, fmt)
        if image.isNull():
            print("QImage creation failed!")
            self.label.setText("Failed to create image.")
            return

        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio))
