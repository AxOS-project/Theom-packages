from PyQt6.QtCore import Qt, QTimer, QObject, QRunnable, pyqtSignal, pyqtSlot, QThreadPool
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea,
    QFrame, QPushButton
)
from clickable_label import ClickableLabel
from wallpaper_loader import WallpaperLoader


class PixmapWorkerSignals(QObject):
    finished = pyqtSignal(int, QPixmap)


class PixmapWorker(QRunnable):
    def __init__(self, index, path, size):
        super().__init__()
        self.index = index
        self.path = path
        self.size = size
        self.signals = PixmapWorkerSignals()

    @pyqtSlot()
    def run(self):
        pixmap = QPixmap(self.path).scaled(
            self.size[0],
            self.size[1],
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.signals.finished.emit(self.index, pixmap)


class WallpapersPage(QWidget):
    def __init__(self, app_ref):
        super().__init__()

        self.app_ref = app_ref
        self.wallpaper_paths = []
        self.lazy_index = 0

        self.wallpaper_grid = QGridLayout()
        self.wallpaper_grid.setSpacing(10)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.title_label = QLabel("Wallpapers")
        self.title_label.setStyleSheet("font-size: 25px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.wallpaper_container = QWidget()
        self.wallpaper_container.setLayout(self.wallpaper_grid)
        self.scroll_area.setWidget(self.wallpaper_container)
        self.layout.addWidget(self.scroll_area)

        self.set_wallpaper_button = QPushButton("Set Wallpaper")
        self.set_wallpaper_button.setEnabled(False)
        self.set_wallpaper_button.setFixedHeight(50)
        self.set_wallpaper_button.clicked.connect(self.app_ref.set_selected_wallpaper)
        self.layout.addWidget(self.set_wallpaper_button)

        self.thread_pool = QThreadPool()

        self.load_wallpapers_async()

    def load_wallpapers_async(self):
        self.title_label.setText("Loading wallpapers...")
        self.loader_thread = WallpaperLoader('/usr/share/backgrounds/')
        self.loader_thread.wallpapers_loaded.connect(self.on_wallpapers_loaded)
        self.loader_thread.start()

    def on_wallpapers_loaded(self, paths):
        self.title_label.setText("Wallpapers")
        self.wallpaper_paths = paths
        self.lazy_index = 0

        # Start lazy loading timer
        self.lazy_timer = QTimer()
        self.lazy_timer.timeout.connect(self.load_next_batch)
        self.lazy_timer.start(30)

    def load_next_batch(self):
        if self.lazy_index >= len(self.wallpaper_paths):
            self.lazy_timer.stop()
            return

        index = self.lazy_index
        path = self.wallpaper_paths[index]

        worker = PixmapWorker(index, path, (150, 150))
        worker.signals.finished.connect(self.on_pixmap_ready)

        self.thread_pool.start(worker)
        self.lazy_index += 1

    def on_pixmap_ready(self, index, pixmap):
        label_frame = QFrame()
        label_frame.setFrameShape(QFrame.Shape.StyledPanel)
        label_frame.setStyleSheet("QFrame { border: 2px solid transparent; border-radius: 4px; }")

        label = ClickableLabel(label_frame, app_ref=self.app_ref)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.path = self.wallpaper_paths[index]

        label_layout = QVBoxLayout(label_frame)
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.addWidget(label)

        r, c = divmod(index, 4)
        self.wallpaper_grid.addWidget(label_frame, r, c)
