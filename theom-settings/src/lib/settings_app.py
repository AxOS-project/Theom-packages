import os
import json
import sys
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QSpacerItem, QSizePolicy,
    QStackedWidget
)
from clickable_label import ClickableLabel
from appearance_page import AppearancePage
from wallpapers_page import WallpapersPage
from about_page import AboutPage
from compositing_page import CompositingPage
from osd_page import OSDPage

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

        # Sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(10)

        self.sidebar = QListWidget()
        self.sidebar.setSpacing(0)
        self.sidebar.addItems(["Appearance", "Compositing", "OSD", "Wallpapers", "About"])
        self.sidebar.currentItemChanged.connect(self.on_sidebar_item_selected)
        sidebar_layout.addWidget(self.sidebar, stretch=1)

        sidebar_layout.addSpacerItem(QSpacerItem(
            0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setMinimumWidth(160)

        self.content_area = QStackedWidget()
        self.content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.appearance_page = AppearancePage()
        self.compositing_page = CompositingPage()
        self.osd_page = OSDPage()
        self.wallpapers_page = WallpapersPage(app_ref=self)
        self.about_page = AboutPage()

        self.content_area.addWidget(self.appearance_page)
        self.content_area.addWidget(self.compositing_page)
        self.content_area.addWidget(self.osd_page)
        self.content_area.addWidget(self.wallpapers_page)
        self.content_area.addWidget(self.about_page)

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

        self.wallpapers_page.set_wallpaper_button.setEnabled(True)

    def mousePressEvent(self, event):
        if self.selected_wallpaper_label:
            self.selected_wallpaper_label.parent().setStyleSheet(
                "QFrame { border: 2px solid transparent; border-radius: 4px; }")
            self.selected_wallpaper_label = None
            self.selected_wallpaper_path = None
            self.wallpapers_page.set_wallpaper_button.setEnabled(False)

    def on_sidebar_item_selected(self, current, previous):
        if not current:
            return
        if current.text() == "Appearance":
            self.content_area.setCurrentWidget(self.appearance_page)
        elif current.text() == "Compositing":
            self.content_area.setCurrentWidget(self.compositing_page)
        elif current.text() == "OSD":
            self.content_area.setCurrentWidget(self.osd_page)
        elif current.text() == "Wallpapers":
            self.content_area.setCurrentWidget(self.wallpapers_page)
        elif current.text() == "About":
            self.content_area.setCurrentWidget(self.about_page)

    def set_selected_wallpaper(self):
        if self.selected_wallpaper_path:
            self.set_wallpaper(self.selected_wallpaper_path)

            # Clear selection after setting wallpaper
            if self.selected_wallpaper_label:
                self.selected_wallpaper_label.parent().setStyleSheet(
                    "QFrame { border: 2px solid transparent; border-radius: 4px; }")

            self.selected_wallpaper_label = None
            self.selected_wallpaper_path = None
            self.wallpapers_page.set_wallpaper_button.setEnabled(False)

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
