from qtpy.QtWidgets import QWidget
from qtpy import QtCore
from qtpy.QtCore import Qt

from ui.ui_ManualControlDialog import Ui_ManualControlDialog
import qdarkstyle
import asyncio
import settings
from imports import get_theme, warning, take_screenshot
from arduino import AIODevice


class ManualWidget(QWidget, Ui_ManualControlDialog):
    """
    Manual control dialog. This dialog allows the user to manually control the
    pins of the USB device.

    :param usb_handler: The USB connection handler.
    """

    def __init__(self, arduino: AIODevice = None):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.settings = settings.get_instance()
        print('ManualWidget settings =', self.settings)
        if get_theme(self.settings) == "dark":
            self.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette))
        else:
            self.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.LightPalette))

        self._arduino = arduino

        if self._arduino is None or not self._arduino.device_connected:
            warning(self, f"USB device not connected.")
            self.close()
            return

        self.battery_button.clicked.connect(lambda checked: asyncio.create_task(self.toggle_pin("battery", checked)))
        self.low_battery_button.clicked.connect(lambda checked: asyncio.create_task(self.toggle_pin("low battery", checked)))
        self.test_indicator_button.clicked.connect(lambda checked: asyncio.create_task(self.toggle_pin("test indicator", checked)))
        self.indicator_button.clicked.connect(lambda checked: asyncio.create_task(self.toggle_pin("indicator", checked)))

    async def toggle_pin(self, pin: str, checked: bool):
        value = (0, 1)[checked]
        await self._arduino.write_pin_by_func(pin, value)

    async def end(self):
        if self._arduino is not None:
            if self._arduino.device_connected:
                await self._arduino.set_all_pins_to_value(0)

    def closeEvent(self, event):
        # Close the dialog and reset the pins
        asyncio.create_task(self.end())
        event.accept()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_F2:
            take_screenshot()
