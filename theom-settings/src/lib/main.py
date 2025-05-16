#!/usr/bin/env python3

import sys
import os
import json
import re
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QMouseEvent
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QSpacerItem, QSizePolicy,
    QListWidget, QLineEdit, QLabel, QGridLayout, QFrame, QScrollArea
)

class ClickableLabel(QLabel):
    def __init__(self, parent=None, app_ref=None):
        super().__init__(parent)
        self.path = None
        self.app_ref = app_ref

    def mousePressEvent(self, event: QMouseEvent):
        if self.app_ref:
            self.app_ref.on_wallpaper_selected(self)

class SettingsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Theom Settings")
        self.resize(800, 500)
        self.selected_wallpaper_label = None
        self.selected_wallpaper_path = None

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(10)

        self.sidebar = QListWidget()
        self.sidebar.setSpacing(10)
        self.sidebar.addItems(["Appearance", "Wallpapers"])
        self.sidebar.currentItemChanged.connect(self.on_sidebar_item_selected)
        sidebar_layout.addWidget(self.sidebar, stretch=1)

        sidebar_layout.addSpacerItem(QSpacerItem(
            0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setMinimumWidth(160)

        self.content_area = QStackedWidget()
        self.content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.appearance_page = QWidget()
        appearance_layout = QVBoxLayout(self.appearance_page)
        appearance_layout.setContentsMargins(20, 20, 20, 20)
        appearance_layout.setSpacing(15)
        appearance_label = QLabel("Appearance Settings")
        appearance_button = QPushButton("Open LXAppearance")
        appearance_button.clicked.connect(self.launch_lxappearance)
        appearance_layout.addWidget(appearance_label)
        appearance_layout.addWidget(appearance_button)
        appearance_layout.addStretch()

        self.wallpapers_page = QWidget()
        wallpaper_layout = QVBoxLayout(self.wallpapers_page)
        wallpaper_layout.setContentsMargins(20, 20, 20, 20)
        wallpaper_layout.setSpacing(15)
        wallpaper_label = QLabel("Wallpapers")
        wallpaper_layout.addWidget(wallpaper_label)

        # Create a QGridLayout for the wallpapers
        wallpaper_grid = QGridLayout()
        wallpaper_dir = '/usr/share/backgrounds/theom/'
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

                label = ClickableLabel(label_frame, app_ref=self)

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

        # Create a QScrollArea for the wallpaper grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Ensures the content expands
        wallpaper_widget = QWidget()
        wallpaper_widget.setLayout(wallpaper_grid)
        scroll_area.setWidget(wallpaper_widget)

        # Add the scroll area to the wallpaper layout
        wallpaper_layout.addWidget(scroll_area)

        self.set_wallpaper_button = QPushButton("Set Wallpaper")
        self.set_wallpaper_button.setEnabled(False)
        self.set_wallpaper_button.setFixedHeight(50)
        self.set_wallpaper_button.clicked.connect(self.set_selected_wallpaper)
        wallpaper_layout.addWidget(self.set_wallpaper_button)

        self.content_area.addWidget(self.appearance_page)
        self.content_area.addWidget(self.wallpapers_page)

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.content_area, 1)

        self.setLayout(main_layout)
        self.sidebar.setCurrentRow(0)

    def on_wallpaper_selected(self, clicked_label):
        if self.selected_wallpaper_label:
            self.selected_wallpaper_label.parent().setStyleSheet(
                "QFrame { border: 2px solid transparent; border-radius: 4px; }")

        self.selected_wallpaper_label = clicked_label
        self.selected_wallpaper_path = clicked_label.path
        clicked_label.parent().setStyleSheet(
            "QFrame { border: 2px solid #888; border-radius: 4px; }")

        self.set_wallpaper_button.setEnabled(True)


    def mousePressEvent(self, event):
        if self.selected_wallpaper_label:
            self.selected_wallpaper_label.parent().setStyleSheet(
                "QFrame { border: 2px solid transparent; border-radius: 4px; }")
            self.selected_wallpaper_label = None
            self.selected_wallpaper_path = None
            self.set_wallpaper_button.setEnabled(False)


    def on_sidebar_item_selected(self, current, previous):
        if not current:
            return
        match current.text():
            case "Appearance":
                self.content_area.setCurrentWidget(self.appearance_page)
            case "Wallpapers":
                self.content_area.setCurrentWidget(self.wallpapers_page)

    def launch_lxappearance(self):
        try:
            subprocess.Popen(["lxappearance"])
        except FileNotFoundError:
            print("lxappearance is not installed or not in PATH.")

    def set_selected_wallpaper(self):
        if self.selected_wallpaper_path:
            self.set_wallpaper(self.selected_wallpaper_path)

            # Clear selection after setting wallpaper
            if self.selected_wallpaper_label:
                self.selected_wallpaper_label.parent().setStyleSheet(
                    "QFrame { border: 2px solid transparent; border-radius: 4px; }")

            self.selected_wallpaper_label = None
            self.selected_wallpaper_path = None
            self.set_wallpaper_button.setEnabled(False)


    def set_wallpaper(self, wallpaper):
        print(f"Setting wallpaper: {wallpaper}")
        config_json_path = os.path.expanduser('~/.config/.theom/config.json')

        if os.path.exists(config_json_path):
            with open(config_json_path, 'r') as file:
                try:
                    config_data = json.load(file)
                except json.JSONDecodeError:
                    print("Error: config.json is not valid JSON.")
                    return
        else:
            config_data = {}

        config_data['wallpaper'] = wallpaper

        with open(config_json_path, 'w') as file:
            json.dump(config_data, file, indent=4)

        os.system(f"feh --bg-scale '{wallpaper}'")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QWidget {
            background-color: #2e2e2e;
            color: #ffffff;
        }
        QListWidget {
            background-color: #3b3b3b;
            border: none;
        }
        QListWidget::item {
            padding: 10px;
            margin: 2px 0;
        }
        QListWidget::item:selected {
            background-color: #005c8a;
        }
        QLineEdit {
            background-color: #4c4c4c;
            border: 1px solid #666;
            border-radius: 4px;
            padding: 8px;
        }
        QPushButton {
            background-color: #0078d7;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton:disabled {
            background-color: #555;
            color: #999;
        }
        QPushButton:hover {
            background-color: #0066bb;
        }
        QLabel {
            font-size: 18px;
        }
        QScrollArea {
            border: none;
        }
        QScrollBar:vertical {
            border: none;
            background: #444;
            width: 10px;
            margin: 0px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background: #666;
            min-height: 30px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical:hover {
            background: #888;
        }
    """)

    window = SettingsApp()
    window.show()
    sys.exit(app.exec())
