from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
import subprocess
import os
import json

class AppearancePage(QWidget):
    def __init__(self):
        super().__init__()

        self.last_saved_theme = None  # Track last saved theme

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
        self.theomTheme.addItems(["Light", "Dark"])
        self.theomTheme.currentIndexChanged.connect(self.on_theme_changed)

        # Save button, initially hidden or disabled
        self.save_button = QPushButton("Save Theme")
        self.save_button.setEnabled(False)  # Disabled until change
        self.save_button.clicked.connect(self.save_theme)

        layout.addWidget(label)
        layout.addWidget(lxappearanceLabel)
        layout.addWidget(button)
        layout.addWidget(theomThemeLabel)
        layout.addWidget(self.theomTheme)
        layout.addWidget(self.save_button)  # Add save button to layout
        layout.addStretch()

        self.load_last_saved_theme()

    def launch_lxappearance(self):
        try:
            subprocess.Popen(["lxappearance"])
        except FileNotFoundError:
            print("lxappearance is not installed or not in PATH.")

    def load_last_saved_theme(self):
        config_json_path = os.path.expanduser('~/.config/.theom/config.json')
        if os.path.exists(config_json_path):
            with open(config_json_path, 'r') as file:
                try:
                    config_data = json.load(file)
                    theme = config_data.get('theme', 'Light')
                except json.JSONDecodeError:
                    theme = 'Light'
        else:
            theme = 'Light'
        self.last_saved_theme = theme
        index = self.theomTheme.findText(theme)
        if index >= 0:
            self.theomTheme.setCurrentIndex(index)

    def on_theme_changed(self, index):
        current_theme = self.theomTheme.itemText(index)
        # saves if it is different from last one
        if current_theme != self.last_saved_theme:
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    def save_theme(self):
        selected_theme = self.theomTheme.currentText()
        print(f"Saving theme: {selected_theme}")
        config_json_path = os.path.expanduser('~/.config/.theom/config.json')

        if os.path.exists(config_json_path):
            with open(config_json_path, 'r') as file:
                try:
                    config_data = json.load(file)
                except json.JSONDecodeError:
                    config_data = {}
        else:
            config_data = {}

        config_data['theme'] = selected_theme

        with open(config_json_path, 'w') as file:
            json.dump(config_data, file, indent=4)

        self.last_saved_theme = selected_theme
        self.save_button.setEnabled(False)
        os.system("i3 restart") # restart i3 to apply changes