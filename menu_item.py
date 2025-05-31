from qtpy.QtWidgets import QAction
from qtpy.QtGui import QIcon
from qtpy.QtCore import QSize
from imports import get_stylesheet
from settings import get_instance


class MenuItem(QAction):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setChecked(False)

        icon = QIcon()
        icon.addFile(f":/icons/{get_stylesheet(get_instance())}/radio-off-button.png", QSize(), QIcon.Mode.Selected, QIcon.State.Off)
        icon.addFile(f":/icons/{get_stylesheet(get_instance())}/radio-on-button.png", QSize(), QIcon.Mode.Selected, QIcon.State.On)
        self.setIcon(icon)

    def setIcon(self, icon):
        if icon:
            super().setIcon(icon)
        else:
            super().setIcon(QIcon())