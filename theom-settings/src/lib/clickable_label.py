from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QMouseEvent

class ClickableLabel(QLabel):
    def __init__(self, parent=None, app_ref=None):
        super().__init__(parent)
        self.path = None
        self.app_ref = app_ref

    def mousePressEvent(self, event: QMouseEvent):
        if self.app_ref:
            self.app_ref.on_wallpaper_selected(self)
