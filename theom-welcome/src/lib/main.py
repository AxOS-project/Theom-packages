#!/usr/bin/env python3

import sys
import os
import tomlkit
import subprocess
import webbrowser
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QSpacerItem, QSizePolicy,
    QLabel, QCheckBox, QScrollArea
)

CONFIG_PATH = os.path.expanduser("~/.config/.theom/config.toml")
WELCOMER_STATE_PATH = os.path.expanduser("~/.local/state/theom/welcomer.state")

class WelcomeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Theom")
        self.setFixedSize(500, 402)
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
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2b2d42,
                    stop:0.5 #23253a,
                    stop:1 #1e2033
                );

                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 15px;
                background: transparent;
            }
            QCheckBox {
                color: black;
                font-size: 13px;
                background: transparent;
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
    def get_user(self):
        return os.getlogin()

    def init_ui(self):
        welcome_screen = QWidget()
        layout = QVBoxLayout(welcome_screen)
        container = self.create_container()

        layout.addWidget(container)
        self.stacked_widget.addWidget(welcome_screen)

    def create_container(self):
        container = QWidget(self)
        container.setStyleSheet('''
            background-color: rgba(255, 255, 255, 1);
            border-radius: 10px;
        ''')
        layout = QVBoxLayout(container)

        welcome_label = self.create_label(f"Welcome {self.get_user()}!", Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("color: #333333; font-size: 20px; font-weight: bold; background: transparent;")
        layout.addWidget(welcome_label)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        explore_label = self.create_label("Set up your desktop:", Qt.AlignmentFlag.AlignLeft)
        explore_label.setStyleSheet("color: #333333; font-size: 16px; font-weight: bold; background: transparent;")
        layout.addWidget(explore_label)


        #layout.addLayout(self.create_compositing_checkbox())
        layout.addLayout(self.create_osd_checkbox())

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
            "Customize theom appearance",
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

    def load_welcomer_state(self):
        if os.path.exists(WELCOMER_STATE_PATH):
            try:
                with open(WELCOMER_STATE_PATH, "r") as f:
                    return f.read().strip().lower() != "false"
            except Exception:
                return True
        return True 

    def save_welcomer_state(self, show):
        os.makedirs(os.path.dirname(WELCOMER_STATE_PATH), exist_ok=True)
        with open(WELCOMER_STATE_PATH, "w") as f:
            f.write(str(show))

    def on_feature_clicked(self, f):
        try:
            if f == "Customize theom appearance":
                subprocess.Popen(["lxappearance"])
            elif f == "Explore the settings":
                subprocess.Popen(["theom-settings"])
            elif f == "View keybindings":
                webbrowser.open(f"file:///usr/lib/theom-welcome/keybindings.html")
        except FileNotFoundError:
            print(f"Feature '{f}' not available.")

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                return tomlkit.parse(f.read())
        return tomlkit.document()

    def update_config(self, key, value, section=None):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = tomlkit.parse(f.read())
        else:
            config = tomlkit.document()

        if section:
            if section not in config:
                config[section] = tomlkit.table()
            config[section][key] = value
        else:
            config[key] = value

        with open(CONFIG_PATH, 'w') as f:
            f.write(tomlkit.dumps(config))

        print(tomlkit.dumps(config))
        self.config = config



    def on_checkbox_changed(self, state):
        show_again = state != Qt.CheckState.Checked.value
        self.save_welcomer_state(show_again)


    def on_compositing_checkbox_changed(self, state):
        enable_compositing = state == Qt.CheckState.Checked.value
        self.update_config("compositing", enable_compositing, section="features")

    def on_osd_checkbox_changed(self, state):
        enable_osd = state == Qt.CheckState.Checked.value
        self.update_config("osd", enable_osd, section="features")

    def create_checkbox_row(self):
        layout = QHBoxLayout()
        layout.addStretch()
        self.dont_show_checkbox = QCheckBox("Don't show this again")
        self.dont_show_checkbox.setChecked(not self.load_welcomer_state())
        self.dont_show_checkbox.stateChanged.connect(self.on_checkbox_changed)
        self.dont_show_checkbox.setToolTip("Don't show this window again while launching theom.")
        layout.addWidget(self.dont_show_checkbox)
        return layout


    def create_compositing_checkbox(self):
        layout = QHBoxLayout()
        self.compositing_checkbox = QCheckBox("Enable compositing")
        self.compositing_checkbox.setChecked(self.config.get("compositing", True))
        self.compositing_checkbox.stateChanged.connect(self.on_compositing_checkbox_changed)
        self.compositing_checkbox.setStyleSheet("padding-left: 10px;")
        self.compositing_checkbox.setToolTip("Enabling compositing is recommended for better performance and visual effects.")
        layout.addWidget(self.compositing_checkbox)
        return layout

    def create_osd_checkbox(self):
        layout = QHBoxLayout()
        self.osd_checkbox = QCheckBox("Enable on screen display effects")
        self.osd_checkbox.setChecked(self.config.get("features", {}).get("osd", True))
        self.osd_checkbox.stateChanged.connect(self.on_osd_checkbox_changed)
        self.osd_checkbox.setStyleSheet("padding-left: 10px;")
        self.osd_checkbox.setToolTip("If enabled, it will show effects on the screen if certain actions are performed.")
        layout.addWidget(self.osd_checkbox)
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

    if not os.path.exists(WELCOMER_STATE_PATH):
        show = True
    else:
        with open(WELCOMER_STATE_PATH, 'r') as f:
            show = f.read().strip().lower() != "false"
    if not show and not force_launch:
        print("Welcomer is disabled. Exiting.")
        sys.exit(0)


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
