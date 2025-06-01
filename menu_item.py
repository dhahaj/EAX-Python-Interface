from qtpy.QtWidgets import QAction
from qtpy.QtGui import QIcon, QFont
from qtpy.QtCore import QSize
from imports import get_font, get_stylesheet
from settings import get_instance
import device


class MenuItem(QAction):
    def __init__(self, device: device.Device, parent=None):
        super().__init__(device.name, parent)
        self.setCheckable(True)
        self.setChecked(False)
        self.setData(device)
        self.setToolTip(f"{device.name} ({device.firmware})")
        self.setStatusTip(f"{device.name} ({device.firmware})")
        font = QFont()
        font.setPointSize(11)
        self.setFont(font)
        icon = QIcon()
        icon.addFile(f":/icons/{get_stylesheet(get_instance())}/radio-off-button.png", QSize(), QIcon.Mode.Selected, QIcon.State.Off)
        icon.addFile(f":/icons/{get_stylesheet(get_instance())}/radio-on-button.png", QSize(), QIcon.Mode.Selected, QIcon.State.On)
        self.setIcon(icon)

    def setIcon(self, icon):
        if icon:
            super().setIcon(icon)
        else:
            super().setIcon(QIcon())