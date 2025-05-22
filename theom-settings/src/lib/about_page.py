from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import subprocess
import importlib.metadata
from shutil import which
import platform
import os

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("About This Device")
        header.setStyleSheet("font-size: 25px; font-weight: bold;")
        header.setFont(QFont("Sans Serif", 18, QFont.Weight.Bold))
        layout.addWidget(header)

        # Device Info Section
        layout.addWidget(self.section_label("Hardware"))

        hardware_layout = QFormLayout()
        hardware_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        hardware_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)

        hardware_layout.addRow("Device Name:", QLabel(platform.node()))
        hardware_layout.addRow("CPU(s):", QLabel("\n".join(self.get_all_cpu_models()) or "Unknown"))
        hardware_layout.addRow("GPU(s):", QLabel("\n".join(self.get_all_gpu_models()) or "Unknown"))
        hardware_layout.addRow("Memory:", QLabel(self.get_memory_info() or "Unknown"))

        layout.addLayout(hardware_layout)

        # Software Info Section
        layout.addWidget(self.section_label("Software"))

        software_layout = QFormLayout()
        software_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        software_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)

        software_layout.addRow("OS:", QLabel(platform.system() + " " + platform.release()))
        software_layout.addRow("Kernel:", QLabel(platform.uname().release))
        software_layout.addRow("Theom Version:", QLabel(self.get_theom_version() or "Not installed"))

        layout.addLayout(software_layout)
        layout.addStretch()

    def section_label(self, text):
        label = QLabel(text)
        label.setFont(QFont("Sans Serif", 12, QFont.Weight.Bold))
        return label

    def get_all_cpu_models(self) -> list[str]:
        models = set()
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                for line in f:
                    if line.lower().startswith("model name"):
                        models.add(line.split(":", 1)[1].strip())
        except FileNotFoundError:
            pass
        return sorted(models)

    def get_all_gpu_models(self) -> list[str]:
        if which("lspci"):
            try:
                out = subprocess.check_output(["lspci"], stderr=subprocess.DEVNULL)
                lines = out.decode().splitlines()
                gpus = [
                    line.split(":", 2)[2].strip()
                    for line in lines
                    if any(k in line for k in ("VGA compatible controller", "3D controller"))
                ]
                if gpus:
                    return gpus
            except subprocess.SubprocessError:
                pass

        if which("lshw"):
            try:
                out = subprocess.check_output(["lshw", "-C", "display"], stderr=subprocess.DEVNULL)
                lines = out.decode().splitlines()
                gpus = [
                    l.split("product:", 1)[1].strip()
                    for l in lines
                    if "product:" in l
                ]
                return gpus
            except subprocess.SubprocessError:
                pass

        return []

    def get_memory_info(self) -> str | None:
        try:
            with open("/proc/meminfo", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        kb = int(line.split()[1])
                        gb = kb / 1024 / 1024
                        return f"{gb:.1f} GB"
        except Exception:
            return None

    def get_theom_version(self) -> str | None:
        try:
            return importlib.metadata.version("theom")
        except importlib.metadata.PackageNotFoundError:
            return None
