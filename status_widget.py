from qtpy.QtCore import QEvent
from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QStatusBar, QApplication
from qtpy.QtCore import QTimer
from ui.ui_StatusBarWidget import Ui_StatusBarWidget
import settings
import constants
from globals import logger as log


class StatusWidget(QWidget, Ui_StatusBarWidget):
    """
    A custom status bar widget that displays a message and a counter.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class CustomStatusBar(QStatusBar):
    """
    A custom status bar that is able to display a persistant message.
    """

    def __init__(self):
        super().__init__()
        self.widget = StatusWidget()
        self.addPermanentWidget(self.widget, 1)

        self.widget.lcdNumber.setDigitCount(5)
        self.settings = settings.get_instance()
        # if self.settings.get_bool(constants.KEY_COUNTER_ENABLED, False):
        #     self.widget.lcdNumber.display(self.settings.get_int(constants.KEY_TEST_COUNT, 0))
        self.widget.lcdNumber.display(log.get_tests_run())
        self._persistent_message = ""

        app = QApplication.instance()
        if app:
            app.installEventFilter(self)  # catch status‐tips anywhere

    def eventFilter(self, watched, event):
        # catch hover‐tips
        if event.type() == QEvent.StatusTip:
            tip = event.tip()
            if tip:
                # a new hover tip arrived → show it
                self.widget.status.setText(tip)
            else:
                # tip="" means “clear the hover tip” → go back to real text
                self.widget.status.setText(self._persistent_message)
            return True
        return super().eventFilter(watched, event)

    def clearMessage(self):
        self.widget.status.clear()
        super().clearMessage()
        if self._persistent_message:
            self.widget.status.setText(self._persistent_message)

    def showMessage(self, message: str, timeout: int = 0) -> None:
        self._persistent_message = message
        self.widget.status.setText(message)
        if timeout > 0:
            QTimer.singleShot(timeout, lambda: self.clearMessage())

    def update_counter(self) -> None:
        # IF the persistant counter is enabled, increment the counter in the settings
        # so that it can be restored on the next run. Otherwise, just increment the counter in the widget.
        if self.settings.get_bool(constants.KEY_COUNTER_ENABLED, False):
            self.widget.lcdNumber.display(self.settings.get_int(constants.KEY_TEST_COUNT, 0))
        else:
            current_value = self.widget.lcdNumber.value()
            self.widget.lcdNumber.display(current_value + 1)

    def set_value(self, value: int) -> None:
        """Set the value of the counter in the status bar."""
        self.widget.lcdNumber.display(value)
