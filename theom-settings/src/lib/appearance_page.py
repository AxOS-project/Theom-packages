from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
import subprocess
import os
import tomlkit

class AppearancePage(QWidget):
    def __init__(self):
        super().__init__()

        self.last_saved_theme = None
        self.last_saved_layout = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        label = QLabel("Appearance Settings")
        label.setStyleSheet("font-size: 25px; font-weight: bold;")

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
        config_path = os.path.expanduser('~/.config/.theom/config.toml')
        theme, layout = 'light', 'float'

        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                try:
                    config = tomlkit.parse(file.read())
                    theme = config.get("appearance", {}).get("theme", "light")
                    layout = config.get("bar", {}).get("polybar_layout", "float")
                except Exception as e:
                    print(f"Failed to parse TOML: {e}")

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

        config_path = os.path.expanduser('~/.config/.theom/config.toml')

        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                try:
                    config = tomlkit.parse(file.read())
                except Exception:
                    config = tomlkit.document()
        else:
            config = tomlkit.document()

        if "appearance" not in config:
            config["appearance"] = tomlkit.table()
        if "bar" not in config:
            config["bar"] = tomlkit.table()

        config["appearance"]["theme"] = new_theme
        config["bar"]["polybar_layout"] = new_layout

        with open(config_path, 'w') as file:
            file.write(tomlkit.dumps(config))

        self.last_saved_theme = new_theme
        self.last_saved_layout = new_layout

        self.apply_button.setVisible(False)
        self.noticeLabel.setText("Changes applied. Restart i3 to see effect.")
        self.noticeLabel.setVisible(True)

        # Avoid forcing restart for UX reasons
        # os.system("i3 restart")
