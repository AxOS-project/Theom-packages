import sys
import subprocess
from PyQt6.QtWidgets import QApplication
from dashboard import Dashboard
from app_styles import stylesheet, stylesheet_light
from detect_theme import current_theme

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")


    theme_output = current_theme()
    if theme_output == "light":
        app.setStyleSheet(stylesheet_light())
    else:
        app.setStyleSheet(stylesheet())

    window = Dashboard()
    window.show()
    sys.exit(app.exec())
