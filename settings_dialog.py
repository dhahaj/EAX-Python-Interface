from qtpy.QtCore import QEvent, QByteArray, QSize
from qtpy.QtCore import Qt, QDateTime
from qtpy.QtGui import QColor, QFont
from qtpy.QtWidgets import QWidget, QColorDialog, QMainWindow
from ui.ui_Settings import Ui_Settings
from settings import get_instance
import constants
from imports import get_stylesheet, take_screenshot, get_font
from config_loader import get_instance as get_config
from arduino import AIODevice
import re
import asyncio

class SettingsDialog(QWidget, Ui_Settings):
    """
    The SettingsDialog class provides a user interface for configuring various settings related to
    the application. It extends QWidget and Ui_Settings to create a dialog that contains controls
    for managing settings such as COM ports, chip parts, auto-test options, debug mode, and color preferences.
    The dialog also allows users to load, validate, apply, save, and restore default settings.

    The class includes methods to:
        - Load and validate settings.
        - Populate and manage chip parts and USB ports.
        - Enable the selection of colors for different elements.
        - Save and set default configurations.
        - Emit a signal when the dialog is closed, providing the current settings state.

    Various widgets such as comboBox, pushButton, and dial are utilized to allow the user to interact
    with different options and modify the application settings accordingly.

    :param parent: The parent widget.
    """

    def __init__(self, parent: QMainWindow = None):
        super().__init__()
        self.setupUi(self)

        self.settings = get_instance()
        self._parent = parent

        self.background_color: QColor = None
        self.foreground_color: QColor = None
        self.qfont: QFont = None

        self.pushButton_background_color.clicked.connect(self.pick_background_color)
        self.pushButton_foreground_color.clicked.connect(self.pick_text_color)
        self.pushButton_change_font.clicked.connect(self.change_font)

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_default.clicked.connect(self.reset_to_default)
        self.resetCounterButton.clicked.connect(self.reset_counter)
        self.initialize_settings()

        # Set the theme
        self.setStyleSheet(get_stylesheet(self.settings))

        self.checkBoxVirtualCom.toggled.connect(self.on_virtual_com_toggled)
        self.toggle_virtual_com = False

    def on_virtual_com_toggled(self, checked: bool) -> None:
        """Handle the toggling of the virtual COM port checkbox."""
        if checked != self.settings.get_bool(constants.KEY_VIRTUAL_COM_PORT):
            self.toggle_virtual_com = True
        else:
            self.toggle_virtual_com = False

    async def disconnect_device(self) -> None:
        await self._parent.disconnect_device()
        import arduino

        arduino._singleton = None

    def initialize_settings(self) -> None:
        config = get_config()

        self.lineEdit_serial.setText(
            self.settings.app_settings.value(
                constants.KEY_PROGRAMMER_SERIAL_NUMBER, constants.DEFAULT_SETTINGS[constants.KEY_PROGRAMMER_SERIAL_NUMBER]
            )
        )

        self.comboBox_chip.clear()
        for chip_part in constants.CHIP_OPTIONS:
            self.comboBox_chip.addItem(chip_part)

        self.comboBox_chip.setCurrentText(
            self.settings.app_settings.value(constants.KEY_CHIP_PART, constants.DEFAULT_SETTINGS[constants.KEY_CHIP_PART])
        )

        value = self.settings.get_int(constants.KEY_TESTING_SPEED, constants.DEFAULT_SETTINGS[constants.KEY_TESTING_SPEED])
        self.dial.setValue(value)

        self.comboBox_com_port.clear()
        ports = AIODevice.get_usb_ports()
        saved_port = self.settings.app_settings.value(constants.KEY_COM_PORT, constants.DEFAULT_SETTINGS[constants.KEY_COM_PORT])
        if saved_port not in ports:
            ports.append(saved_port)
        self.comboBox_com_port.addItems(ports)

        self.spinBox_autologoff_delay.setValue(
            self.settings.get_int(constants.KEY_INACTIVITY_TIMEOUT, constants.DEFAULT_SETTINGS[constants.KEY_INACTIVITY_TIMEOUT])
        )
        self.spinBox_arduino_id.setValue(
            self.settings.get_int(constants.KEY_ARDUINO_INSTANCE_ID, constants.DEFAULT_SETTINGS[constants.KEY_ARDUINO_INSTANCE_ID])
        )
        self.checkBox_test.setChecked(self.settings.get_bool(constants.KEY_AUTO_TEST, constants.DEFAULT_SETTINGS[constants.KEY_AUTO_TEST]))
        self.checkBox_connect.setChecked(self.settings.get_bool(constants.KEY_AUTO_CONNECT, constants.DEFAULT_SETTINGS[constants.KEY_AUTO_CONNECT]))
        self.checkBox_debug.setChecked(self.settings.get_bool(constants.KEY_DEBUG, constants.DEFAULT_SETTINGS[constants.KEY_DEBUG]))
        self.checkBox_auto_find.setChecked(self.settings.get_bool(constants.KEY_AUTO_FIND, constants.DEFAULT_SETTINGS[constants.KEY_AUTO_FIND]))
        self.checkBox_shutdown_on_exception.setChecked(
            self.settings.get_bool(constants.KEY_SHUTDOWN_ON_EXCEPTION, constants.DEFAULT_SETTINGS[constants.KEY_SHUTDOWN_ON_EXCEPTION])
        )
        self.lineEdit_serial_sleep_tune.setText(
            str(self.settings.app_settings.value(constants.KEY_SLEEP_TUNE, constants.DEFAULT_SETTINGS[constants.KEY_SLEEP_TUNE]))
        )
        self.spinBox_wait_time.setValue(self.settings.get_int(constants.KEY_ARDUINO_WAIT, constants.DEFAULT_SETTINGS[constants.KEY_ARDUINO_WAIT]))
        self.checkBox_fullscreen.setChecked(self.settings.get_bool(constants.KEY_FULLSCREEN, constants.DEFAULT_SETTINGS[constants.KEY_FULLSCREEN]))
        self.checkBoxVirtualCom.setChecked(
            self.settings.get_bool(constants.KEY_VIRTUAL_COM_PORT, constants.DEFAULT_SETTINGS[constants.KEY_VIRTUAL_COM_PORT])
        )
        self.checkBox_frameless.setChecked(self.settings.get_bool(constants.KEY_FRAMELESS, constants.DEFAULT_SETTINGS[constants.KEY_FRAMELESS]))
        self.counterCheckbox.setChecked(
            self.settings.get_bool(constants.KEY_COUNTER_ENABLED, constants.DEFAULT_SETTINGS[constants.KEY_COUNTER_ENABLED])
        )
        self.buttonTimeoutSpinBox.setValue(
            self.settings.get_int(constants.KEY_BUTTON_TIMEOUT, constants.DEFAULT_SETTINGS[constants.KEY_BUTTON_TIMEOUT])
        )

    def reset_to_default(self) -> None:
        self.comboBox_com_port.setCurrentText(constants.DEFAULT_SETTINGS[constants.KEY_COM_PORT])
        self.lineEdit_serial.setText(constants.DEFAULT_SETTINGS[constants.KEY_PROGRAMMER_SERIAL_NUMBER])
        self.comboBox_chip.setCurrentText(constants.DEFAULT_SETTINGS[constants.KEY_CHIP_PART])
        self.dial.setValue(constants.DEFAULT_SETTINGS[constants.KEY_TESTING_SPEED])
        self.checkBox_test.setChecked(constants.DEFAULT_SETTINGS[constants.KEY_AUTO_TEST])
        self.checkBox_connect.setChecked(constants.DEFAULT_SETTINGS[constants.KEY_AUTO_CONNECT])
        self.spinBox_arduino_id.setValue(constants.DEFAULT_SETTINGS[constants.KEY_ARDUINO_INSTANCE_ID])
        self.checkBox_debug.setChecked(constants.DEFAULT_SETTINGS[constants.KEY_DEBUG])
        self.spinBox_autologoff_delay.setValue(constants.DEFAULT_SETTINGS[constants.KEY_INACTIVITY_TIMEOUT])
        self.spinBox_wait_time.setValue(constants.DEFAULT_SETTINGS[constants.KEY_ARDUINO_WAIT])
        self.checkBox_shutdown_on_exception.setChecked(constants.DEFAULT_SETTINGS[constants.KEY_SHUTDOWN_ON_EXCEPTION])
        self.checkBox_auto_find.setChecked(constants.DEFAULT_SETTINGS[constants.KEY_AUTO_FIND])
        self.lineEdit_serial_sleep_tune.setText(str(constants.DEFAULT_SETTINGS[constants.KEY_SLEEP_TUNE]))
        self.checkBox_fullscreen.setChecked(constants.DEFAULT_SETTINGS[constants.KEY_FULLSCREEN])
        self.checkBoxVirtualCom.setChecked(constants.DEFAULT_SETTINGS[constants.KEY_VIRTUAL_COM_PORT])
        self.checkBox_frameless.setChecked(constants.DEFAULT_SETTINGS[constants.KEY_FRAMELESS])
        self.counterCheckbox.setChecked(constants.DEFAULT_SETTINGS[constants.KEY_COUNTER_ENABLED])
        self.buttonTimeoutSpinBox.setValue(constants.DEFAULT_SETTINGS[constants.KEY_BUTTON_TIMEOUT])

    def save_changes(self) -> None:

        self.settings.setValue(constants.KEY_COM_PORT, self.comboBox_com_port.currentText())
        self.settings.setValue(constants.KEY_CHIP_PART, self.comboBox_chip.currentText())
        self.settings.setValue(constants.KEY_PROGRAMMER_SERIAL_NUMBER, self.lineEdit_serial.text())
        self.settings.setValue(constants.KEY_AUTO_TEST, self.checkBox_test.isChecked())
        self.settings.setValue(constants.KEY_AUTO_CONNECT, self.checkBox_connect.isChecked())
        self.settings.setValue(constants.KEY_DEBUG, self.checkBox_debug.isChecked())
        self.settings.setValue(constants.KEY_ARDUINO_INSTANCE_ID, self.spinBox_arduino_id.value())
        self.settings.setValue(constants.KEY_TESTING_SPEED, self.dial.value())
        self.settings.setValue(constants.KEY_INACTIVITY_TIMEOUT, self.spinBox_autologoff_delay.value())
        self.settings.setValue(constants.KEY_AUTO_FIND, self.checkBox_auto_find.isChecked())
        self.settings.setValue(constants.KEY_SHUTDOWN_ON_EXCEPTION, self.checkBox_shutdown_on_exception.isChecked())
        self.settings.setValue(constants.KEY_SLEEP_TUNE, float(self.lineEdit_serial_sleep_tune.text()))
        self.settings.setValue(constants.KEY_ARDUINO_WAIT, self.spinBox_wait_time.value())
        self.settings.setValue(constants.KEY_FULLSCREEN, self.checkBox_fullscreen.isChecked())
        self.settings.setValue(constants.KEY_VIRTUAL_COM_PORT, self.checkBoxVirtualCom.isChecked())
        self.settings.setValue(constants.KEY_FRAMELESS, self.checkBox_frameless.isChecked())
        self.settings.setValue(constants.KEY_COUNTER_ENABLED, self.counterCheckbox.isChecked())
        self.settings.setValue(constants.KEY_BUTTON_TIMEOUT, self.buttonTimeoutSpinBox.value())
        self.settings.setValue(constants.KEY_VIRTUAL_COM_PORT, self.checkBoxVirtualCom.isChecked())

        self.apply_changes()
        if self.toggle_virtual_com:
            asyncio.create_task(self.disconnect_device())

        self.close()

    def apply_changes(self) -> None:
        if self.settings.get(constants.KEY_FULLSCREEN):
            self._parent.actionFullscreen.setChecked(True)
            self._parent.showFullScreen()
        else:
            self._parent.actionFullscreen.setChecked(False)
            self._parent.showNormal()

    def _parse_saved_color(self, s: str) -> QColor:
        """Turn either "rgba(r,g,b,a)" or "#RRGGBB" (or color name) into a QColor."""
        rgba = re.match(r'rgba\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\)', s)
        if rgba:
            r, g, b, a = map(int, rgba.groups())
            return QColor(r, g, b, a)
        return QColor(s)

    def pick_text_color(self):
        old_str = self.settings.get(constants.KEY_FOREGROUND_COLOR, "#ffffff")
        old_col = self._parse_saved_color(old_str)

        new_col = QColorDialog.getColor(old_col, options=QColorDialog.ShowAlphaChannel)
        if not new_col.isValid():
            new_col = old_col

        r, g, b, a = new_col.getRgb()
        new_css = f"rgba({r},{g},{b},{a})"

        sheet = self._parent.text_edit.styleSheet()
        pat = r'(?<!-)\bcolor\s*:\s*[^;]+;'

        if re.search(pat, sheet):
            sheet = re.sub(pat, f"color: {new_css};", sheet)
        else:
            sheet += f"\ncolor: {new_css};"

        self.settings.setValue(constants.KEY_FOREGROUND_COLOR, new_css)
        self._parent.text_edit.setStyleSheet(sheet)

    def pick_background_color(self) -> None:
        old_str = self.settings.get(constants.KEY_BACKGROUND_COLOR, "#000000")
        old_col = self._parse_saved_color(old_str)

        new_col = QColorDialog.getColor(old_col, options=QColorDialog.ShowAlphaChannel)
        if not new_col.isValid():
            new_col = old_col

        r, g, b, a = new_col.getRgb()
        new_css = f"rgba({r},{g},{b},{a})"

        sheet = self._parent.text_edit.styleSheet()
        pat = r'(?<!-)\bbackground-color\s*:\s*[^;]+;'

        if re.search(pat, sheet):
            sheet = re.sub(pat, f"background-color: {new_css};", sheet)
        else:
            sheet += f"\nbackground-color: {new_css};"

        self.settings.setValue(constants.KEY_BACKGROUND_COLOR, new_css)
        self._parent.text_edit.setStyleSheet(sheet)

    def choose_color(self, color_name: QColor) -> QColor:
        print(f"choose_color: old color = {color_name.getRgb()}")
        new_color = QColorDialog.getColor(color_name, options=QColorDialog.ShowAlphaChannel)

        if new_color.isValid():
            return new_color
        else:
            return color_name

    def change_font(self) -> None:
        ok, font = get_font(
            [
                self.settings.get(constants.KEY_FONT_FAMILY, self._parent.font().family()),
                self.settings.get_int(constants.KEY_FONT_SIZE, self._parent.font().pointSize()),
                self.settings.get_int(constants.KEY_FONT_WEIGHT, self._parent.font().weight()),
            ]
        )
        if ok:
            self._parent.text_edit.setFont(font)
            self.qfont = font

    def keyPressEvent(self, event) -> None:
        key = event.key()

        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_F2:
            take_screenshot()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.initialize_settings()
        self.activateWindow()
        self.setFocus()

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.WindowDeactivate:
            # Handle focus out event
            # if event.type() == QEvent.Type.WindowDeactivate:
            # The window lost focus, close the dialog
            self.close()
            event.accept()
            return True
        return super().event(event)

    def reset_counter(self) -> None:
        self.settings.setValue(constants.KEY_TEST_COUNT, 0)
        sb = self._parent.statusBar()
        sb.widget.lcdNumber.display(0)
