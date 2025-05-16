import sys
from PyQt6.QtWidgets import QApplication
from settings_app import SettingsApp
from app_styles import stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(stylesheet())

    window = SettingsApp()
    window.show()
    sys.exit(app.exec())
