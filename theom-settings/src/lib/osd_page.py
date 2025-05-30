from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
import os
import tomlkit

class OSDPage(QWidget):
    def __init__(self):
        super().__init__()

        self.last_saved_osd_value = None 

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        label = QLabel("OSD Settings")
        label.setStyleSheet("font-size: 25px; font-weight: bold;")

        osdLabel = QLabel("Enable OSD:")
        osdLabel.setStyleSheet("font-size: 12px;")

        self.enableOSD = QComboBox()
        self.enableOSD.addItems(["true", "false"])
        self.enableOSD.currentIndexChanged.connect(self.on_selection_changed)

        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.setVisible(False)
        self.apply_button.clicked.connect(self.apply_changes)

        self.noticeLabel = QLabel("")
        self.noticeLabel.setStyleSheet("color: red; font-size: 11px;")
        self.noticeLabel.setVisible(False)

        layout.addWidget(label)
        layout.addWidget(osdLabel)
        layout.addWidget(self.enableOSD)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.noticeLabel)
        layout.addStretch()

        self.load_saved_config()

    def load_saved_config(self):
        config_path = os.path.expanduser('~/.config/.theom/config.toml')
        osd_value = 'true'

        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                try:
                    config = tomlkit.parse(file.read())
                    osd_value = str(config.get("features", {}).get("osd", "true")).lower()
                except Exception as e:
                    print(f"Failed to load TOML config: {e}")

        self.last_saved_osd_value = osd_value
        index = self.enableOSD.findText(osd_value)
        if index >= 0:
            self.enableOSD.setCurrentIndex(index)

    def on_selection_changed(self):
        current_value = self.enableOSD.currentText()
        if current_value != self.last_saved_osd_value:
            self.apply_button.setVisible(True)
            self.noticeLabel.setVisible(False)
        else:
            self.apply_button.setVisible(False)

    def apply_changes(self):
        new_osd_value = self.enableOSD.currentText()

        config_path = os.path.expanduser('~/.config/.theom/config.toml')

        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                try:
                    config = tomlkit.parse(file.read())
                except Exception:
                    config = tomlkit.document()
        else:
            config = tomlkit.document()

        if "features" not in config:
            config["features"] = tomlkit.table()

        config["features"]["osd"] = new_osd_value == "true"

        with open(config_path, 'w') as file:
            file.write(tomlkit.dumps(config))

        self.last_saved_osd_value = new_osd_value
        self.apply_button.setVisible(False)
        self.noticeLabel.setText("Changes applied. Restart i3 to see effect.")
        self.noticeLabel.setVisible(True)
