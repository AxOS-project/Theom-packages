import sys
import subprocess
from PyQt6.QtWidgets import QApplication
from dashboard import Dashboard
from app_styles import stylesheet, stylesheet_light

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        theme_output = subprocess.check_output(["theom-config", "theme"], text=True).strip().lower()
        if theme_output == "light":
            app.setStyleSheet(stylesheet_light())
        else:
            app.setStyleSheet(stylesheet())
    except Exception as e:
        print(f"Error detecting theme: {e}")
        app.setStyleSheet(stylesheet())

    window = Dashboard()
    window.show()
    sys.exit(app.exec())
