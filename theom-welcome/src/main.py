#!/usr/bin/env python3

import sys
import os
import json
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QSpacerItem, QSizePolicy,
    QLabel, QCheckBox, QScrollArea
)

CONFIG_PATH = os.path.expanduser("~/.config/.theom/config.json")

class WelcomeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Theom")
        self.setFixedSize(500, 400)
        self.setStyleSheet(self.base_stylesheet())

        self.config = self.load_config()

        self.stacked_widget = QStackedWidget(self)
        self.init_ui()
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def base_stylesheet(self):
        return '''
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff99cc, stop:1 #66ccff);
                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 15px;
            }
            QCheckBox {
                color: black;
                font-size: 13px;
            }
            QPushButton {
                background-color: #ff66b2;
                color: white;
                border-radius: 12px;
                font-size: 16px;
                padding: 10px 25px;
                border: none;
            }
            QPushButton:hover {
                background-color: #ff3385;
            }
            QPushButton:pressed {
                background-color: #e60073;
            }
        '''

    def init_ui(self):
        welcome_screen = QWidget()
        layout = QVBoxLayout(welcome_screen)
        container = self.create_container()

        layout.addWidget(container)
        self.stacked_widget.addWidget(welcome_screen)

    def create_container(self):
        container = QWidget(self)
        container.setStyleSheet('''
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
        ''')
        layout = QVBoxLayout(container)

        welcome_label = self.create_label("Welcome to Theom!", Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("color: #333333; font-size: 20px; font-weight: bold;")
        layout.addWidget(welcome_label)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        explore_label = self.create_label("Set up your desktop:", Qt.AlignmentFlag.AlignLeft)
        explore_label.setStyleSheet("color: #333333; font-size: 16px; font-weight: bold;")
        layout.addWidget(explore_label)


        layout.addLayout(self.create_compositioning_checkbox())

        layout.addWidget(self.create_feature_list())
        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        layout.addLayout(self.create_checkbox_row())
        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        layout.addWidget(self.create_exit_button(), alignment=Qt.AlignmentFlag.AlignCenter)

        return container

    def create_label(self, text, align=Qt.AlignmentFlag.AlignLeft):
        label = QLabel(text)
        label.setAlignment(align)
        return label

    def create_feature_list(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent;")
        widget = QWidget()
        vbox = QVBoxLayout(widget)

        features = [
            "Customize your icon/GTK theme",
            "Explore the settings",
            "View keybindings"
        ]
        for feature in features:
            btn = QPushButton(feature)
            btn.setStyleSheet('''
                QPushButton {
                    background-color: #eeeeee;
                    color: #333;
                    font-size: 14px;
                    padding: 8px 20px;
                    border-radius: 8px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #dddddd;
                }
                QPushButton:pressed {
                    background-color: #cccccc;
                }
            ''')
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, f=feature: self.on_feature_clicked(f))
            vbox.addWidget(btn)

        scroll.setWidget(widget)
        return scroll

    def on_feature_clicked(self, f):
        try:
            if f == "Customize your icon/GTK theme":
                subprocess.Popen(["lxappearance"])
            elif f == "Explore the settings":
                subprocess.Popen(["theom-settings"])
            elif f == "View keybindings":
                subprocess.Popen(["xdg-open", os.path.expanduser("~/.config/.theom/keybindings.txt")])
        except FileNotFoundError:
            print(f"Feature '{f}' not available.")

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r') as f:
                    config = json.load(f)
                    
                    if 'welcomer' not in config:
                        config['welcomer'] = True
                    if 'compositioning' not in config:
                        config['compositioning'] = False 

                    return config
            except json.JSONDecodeError:
                print("Failed to parse config.json")
        
        return {"welcomer": True, "compositioning": False}

    def update_config(self, key, value):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        config = self.config
        config[key] = value
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)

    def on_checkbox_changed(self, state):
        show_again = state != Qt.CheckState.Checked.value
        self.update_config("welcomer", show_again)

    def on_compositioning_checkbox_changed(self, state):
        enable_compositing = state == Qt.CheckState.Checked.value
        self.update_config("compositioning", enable_compositing)

    def create_checkbox_row(self):
        layout = QHBoxLayout()
        layout.addStretch()
        self.dont_show_checkbox = QCheckBox("Don't show this again")
        self.dont_show_checkbox.setChecked(not self.config.get("welcomer", True))
        self.dont_show_checkbox.stateChanged.connect(self.on_checkbox_changed)
        self.dont_show_checkbox.setToolTip("Don't show this window again while launching theom.")
        layout.addWidget(self.dont_show_checkbox)
        return layout

    def create_compositioning_checkbox(self):
        layout = QHBoxLayout()
        self.compositioning_checkbox = QCheckBox("Enable compositing")
        self.compositioning_checkbox.setChecked(self.config.get("compositioning", False))
        self.compositioning_checkbox.stateChanged.connect(self.on_compositioning_checkbox_changed)
        self.compositioning_checkbox.setStyleSheet("padding-left: 10px;")
        self.compositioning_checkbox.setToolTip("Enabling compositing is recommended for better performance and visual effects.")
        layout.addWidget(self.compositioning_checkbox)
        return layout

    def create_exit_button(self):
        button = QPushButton("Exit")
        button.setStyleSheet('''
            QPushButton {
                background-color: #444444;
                color: white;
                font-size: 14px;
                padding: 8px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton:pressed {
                background-color: #222222;
            }
        ''')
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.exit_app)
        return button

    def exit_app(self):
        QApplication.quit()


def main():
    force_launch = "--force" in sys.argv

    if not force_launch and os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                cfg = json.load(f)
                if not cfg.get("welcomer", True):
                    print("Welcomer is disabled. Exiting.")
                    sys.exit(0)
        except json.JSONDecodeError:
            print("Invalid JSON config. Proceeding anyway.")

    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QToolTip {
            padding: 6px;
        }
    """)

    app.setFont(QFont("Arial", 11))
    window = WelcomeApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
