# wallpaper_loader.py
from PyQt6.QtCore import QThread, pyqtSignal
import os

class WallpaperLoader(QThread):
    wallpapers_loaded = pyqtSignal(list)

    def __init__(self, directory):
        super().__init__()
        self.directory = os.path.expanduser(directory)

    def run(self):
        supported_exts = ('.jpg', '.jpeg', '.png', '.bmp')
        wallpaper_files = []

        if os.path.exists(self.directory):
            for file in os.listdir(self.directory):
                if file.lower().endswith(supported_exts):
                    wallpaper_files.append(os.path.join(self.directory, file))

        self.wallpapers_loaded.emit(wallpaper_files)
