from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
import subprocess
import os
import json

class AppearancePage(QWidget):
    def __init__(self):
        super().__init__()

        self.last_saved_theme = None
        self.last_saved_layout = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        label = QLabel("Appearance Settings")

        lxappearanceLabel = QLabel("Customize application looks:")
        lxappearanceLabel.setStyleSheet("font-size: 12px;")

        button = QPushButton("Open LXAppearance")
        button.clicked.connect(self.launch_lxappearance)

        theomThemeLabel = QLabel("Theom theme:")
        theomThemeLabel.setStyleSheet("font-size: 12px;")

        self.theomTheme = QComboBox()
        self.theomTheme.addItems(["light", "dark"])
        self.theomTheme.currentIndexChanged.connect(self.on_selection_changed)

        polybarlayoutLabel = QLabel("Polybar Layout:")
        polybarlayoutLabel.setStyleSheet("font-size: 12px;")

        self.polybarlayout = QComboBox()
        self.polybarlayout.addItems(["float", "stuck"])
        self.polybarlayout.currentIndexChanged.connect(self.on_selection_changed)

        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.setVisible(False)
        self.apply_button.clicked.connect(self.apply_changes)

        self.noticeLabel = QLabel("")
        self.noticeLabel.setStyleSheet("color: red; font-size: 11px;")
        self.noticeLabel.setVisible(False)

        layout.addWidget(label)
        layout.addWidget(lxappearanceLabel)
        layout.addWidget(button)
        layout.addWidget(theomThemeLabel)
        layout.addWidget(self.theomTheme)
        layout.addWidget(polybarlayoutLabel)
        layout.addWidget(self.polybarlayout)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.noticeLabel)
        layout.addStretch()

        self.load_saved_config()

    def launch_lxappearance(self):
        try:
            subprocess.Popen(["lxappearance"])
        except FileNotFoundError:
            print("lxappearance is not installed or not in PATH.")

    def load_saved_config(self):
        config_path = os.path.expanduser('~/.config/.theom/config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                try:
                    config = json.load(file)
                    theme = config.get('theme', 'light')
                    layout = config.get('polybar_layout', 'float')
                except json.JSONDecodeError:
                    theme, layout = 'light', 'float'
        else:
            theme, layout = 'light', 'float'

        self.last_saved_theme = theme
        self.last_saved_layout = layout

        theme_index = self.theomTheme.findText(theme)
        if theme_index >= 0:
            self.theomTheme.setCurrentIndex(theme_index)

        layout_index = self.polybarlayout.findText(layout)
        if layout_index >= 0:
            self.polybarlayout.setCurrentIndex(layout_index)

    def on_selection_changed(self):
        current_theme = self.theomTheme.currentText()
        current_layout = self.polybarlayout.currentText()

        if current_theme != self.last_saved_theme or current_layout != self.last_saved_layout:
            self.apply_button.setVisible(True)
            self.noticeLabel.setVisible(False)
        else:
            self.apply_button.setVisible(False)

    def apply_changes(self):
        new_theme = self.theomTheme.currentText()
        new_layout = self.polybarlayout.currentText()

        config_path = os.path.expanduser('~/.config/.theom/config.json')
        config_data = {}

        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                try:
                    config_data = json.load(file)
                except json.JSONDecodeError:
                    pass

        config_data['theme'] = new_theme
        config_data['polybar_layout'] = new_layout

        with open(config_path, 'w') as file:
            json.dump(config_data, file, indent=4)

        self.last_saved_theme = new_theme
        self.last_saved_layout = new_layout

        self.apply_button.setVisible(False)
        self.noticeLabel.setText("Changes applied. Restart i3 to see effect.")
        self.noticeLabel.setVisible(True)

        # Thsi coe will restart i3 but i running this would be bad of the ux. i think so.
        # os.system("i3 restart")
