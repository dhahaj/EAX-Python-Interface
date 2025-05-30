from qtpy.QtCore import QEvent, QByteArray, QSize
from qtpy.QtGui import QMovie
from qtpy.QtWidgets import QDialog, QLabel
from ui.ui_HelpDialog import Ui_HelpDialog
import settings
from imports import get_stylesheet


class HelpDialog(QDialog, Ui_HelpDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.settings = settings.get_instance()

        self.restoreGeometry(self.settings.app_settings.value("helpwindow/geometry", QByteArray()))
        # self.toolBox.currentChanged.connect(self.on_tab_clicked)
        self.label.installEventFilter(self)
        self.label_2.installEventFilter(self)
        self.label_3.installEventFilter(self)
        self.setStyleSheet(get_stylesheet(self.settings))

    def eventFilter(self, obj: QLabel, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            if obj == self.label:
                obj.setMovie(QMovie(":/images/firmware_update.gif"))
            elif obj == self.label_2:
                obj.setMovie(QMovie(":/images/testing.gif"))
            elif obj == self.label_3:
                obj.setMovie(QMovie(":/images/setting.gif"))
            obj.movie().setScaledSize(QSize(750, 750))
            obj.movie().setSpeed(180)
            obj.movie().start()
            event.accept()
        return super().eventFilter(obj, event)

    def closeEvent(self, event: QEvent) -> None:
        self.settings.app_settings.setValue("helpwindow/geometry", self.saveGeometry())
        self.deleteLater()
        event.accept()
