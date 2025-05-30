from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
import os
import tomlkit

class CompositingPage(QWidget):
    def __init__(self):
        super().__init__()

        self.last_saved_compositing_value = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        label = QLabel("Compositing Settings")
        label.setStyleSheet("font-size: 25px; font-weight: bold;")

        compositingLabel = QLabel("Enable Compositing:")
        compositingLabel.setStyleSheet("font-size: 12px;")

        self.enableCompositing = QComboBox()
        self.enableCompositing.addItems(["true", "false"])
        self.enableCompositing.currentIndexChanged.connect(self.on_selection_changed)

        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.setVisible(False)
        self.apply_button.clicked.connect(self.apply_changes)

        self.noticeLabel = QLabel("")
        self.noticeLabel.setStyleSheet("color: red; font-size: 11px;")
        self.noticeLabel.setVisible(False)

        layout.addWidget(label)
        layout.addWidget(compositingLabel)
        layout.addWidget(self.enableCompositing)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.noticeLabel)
        layout.addStretch()

        self.load_saved_config()

    def load_saved_config(self):
        config_path = os.path.expanduser('~/.config/.theom/config.toml')
        compositing = 'true' 

        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                try:
                    config = tomlkit.parse(file.read())
                    compositing = str(config.get("features", {}).get("compositing", "true")).lower()
                except Exception as e:
                    print(f"Failed to load TOML config: {e}")

        self.last_saved_compositing_value = compositing
        index = self.enableCompositing.findText(compositing)
        if index >= 0:
            self.enableCompositing.setCurrentIndex(index)

    def on_selection_changed(self):
        enable_compositing = self.enableCompositing.currentText()

        if enable_compositing != self.last_saved_compositing_value:
            self.apply_button.setVisible(True)
            self.noticeLabel.setVisible(False)
        else:
            self.apply_button.setVisible(False)

    def apply_changes(self):
        new_compositing_value = self.enableCompositing.currentText()

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

        config["features"]["compositing"] = new_compositing_value == "true"

        with open(config_path, 'w') as file:
            file.write(tomlkit.dumps(config))

        self.last_saved_compositing_value = new_compositing_value
        self.apply_button.setVisible(False)
        self.noticeLabel.setText("Changes applied. Restart i3 to see effect.")
        self.noticeLabel.setVisible(True)
