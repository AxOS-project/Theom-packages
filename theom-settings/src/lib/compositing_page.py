from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
import os
import json

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
        config_path = os.path.expanduser('~/.config/.theom/config.json')
        compositing = 'true'

        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                try:
                    config = json.load(file)
                    compositing = config.get('compositing', 'true')
                except json.JSONDecodeError:
                    pass

        self.last_saved_compositing_value = compositing
        index = self.enableCompositing.findText(str(compositing).lower())
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

        config_path = os.path.expanduser('~/.config/.theom/config.json')
        config_data = {}

        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                try:
                    config_data = json.load(file)
                except json.JSONDecodeError:
                    pass

        config_data['compositing'] = new_compositing_value

        with open(config_path, 'w') as file:
            json.dump(config_data, file, indent=4)

        self.last_saved_compositing_value = new_compositing_value

        self.apply_button.setVisible(False)
        self.noticeLabel.setText("Changes applied. Restart i3 to see effect.")
        self.noticeLabel.setVisible(True)
