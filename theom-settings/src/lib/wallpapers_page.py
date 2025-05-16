import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea,
    QFrame, QVBoxLayout, QPushButton
)
from clickable_label import ClickableLabel

class WallpapersPage(QWidget):
    def __init__(self, app_ref):
        super().__init__()

        self.app_ref = app_ref  # Reference to main app for callbacks

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        label = QLabel("Wallpapers")
        layout.addWidget(label)

        wallpaper_grid = QGridLayout()

        wallpaper_dir = '/usr/share/backgrounds/'
        wallpaper_dir = os.path.expanduser(wallpaper_dir)

        if os.path.exists(wallpaper_dir):
            wallpaper_files = [f for f in os.listdir(wallpaper_dir)
                               if f.lower().endswith(('.jpg', '.png', '.jpeg', '.bmp'))]

            row, col = 0, 0
            for wallpaper in wallpaper_files:
                wallpaper_path = os.path.join(wallpaper_dir, wallpaper)
                pixmap = QPixmap(wallpaper_path).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)

                label_frame = QFrame()
                label_frame.setFrameShape(QFrame.Shape.StyledPanel)
                label_frame.setStyleSheet("QFrame { border: 2px solid transparent; border-radius: 4px; }")

                label = ClickableLabel(label_frame, app_ref=self.app_ref)
                label.setPixmap(pixmap)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.path = wallpaper_path

                label_layout = QVBoxLayout(label_frame)
                label_layout.setContentsMargins(0, 0, 0, 0)
                label_layout.addWidget(label)

                wallpaper_grid.addWidget(label_frame, row, col)
                col += 1
                if col > 3:
                    col = 0
                    row += 1

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        wallpaper_widget = QWidget()
        wallpaper_widget.setLayout(wallpaper_grid)
        scroll_area.setWidget(wallpaper_widget)

        layout.addWidget(scroll_area)

        self.set_wallpaper_button = QPushButton("Set Wallpaper")
        self.set_wallpaper_button.setEnabled(False)
        self.set_wallpaper_button.setFixedHeight(50)
        self.set_wallpaper_button.clicked.connect(self.app_ref.set_selected_wallpaper)
        layout.addWidget(self.set_wallpaper_button)
