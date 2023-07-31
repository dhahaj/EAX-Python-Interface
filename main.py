from PySide6 import QtCore, QtGui
from PySide6.QtCore import QTimer, QEvent, Slot, Qt, QSize
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QColorDialog,
    QWidget,
    QFontDialog,
    QPushButton,
    QInputDialog,
    QLabel,
    QWizard,
)
from PySide6.QtGui import (
    QFont,
    QFontInfo,
    QColor,
    QPalette,
    QIcon,
    QImage,
    QPixmap,
    QAction,
)

from ui_ManualControlDialog import Ui_ManualControlDialog
from ui_MainWindow import Ui_MainWindow

import os
import sys
import subprocess
from loguru import logger as lgr
from constants import *
from applogger import AppLogger, Log
from usbhandler import USBHandler
from settings import Settings
from userdatabase import UserDatabase
from device import Device
from user import User
from rich import print

app_logger = AppLogger("logger").get_logger()
settings = Settings("settings.json")
usb_device = None
db = UserDatabase("users.db")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app

        icon12 = QIcon()
        icon12.addFile(
            ":/resources/icons/images/icons/usb2.png", QSize(), QIcon.Normal, QIcon.On
        )

        self.connect_menu = ConnectMenu("", None)
        self.connect_menu.setIcon(icon12)
        self.connect_menu.menu_clicked.connect(self.connect)

        self.menuBar().addMenu(self.connect_menu)

        self.inactivityTimer = QTimer()
        self.inactivityTimer.setSingleShot(True)
        self.inactivityTimer.timeout.connect(self.onInactivityTimeout)
        self.installEventFilter(self)
        for widget in QApplication.instance().allWidgets():
            widget.installEventFilter(self)

        # Settings
        global settings
        self.settings = settings
        self.settings_dialog = SettingsDialog()
        self.settings_dialog.closed.connect(self.on_settings_closed)

        # Setup the text area
        self.text_edit.setFont(
            QFont(
                self.settings.get(KEY_FONT_FAMILY),
                self.settings.get(KEY_FONT_SIZE),
            )
        )
        self.text_edit.setStyleSheet(
            f'color:{self.settings.get(KEY_FOREGROUND_COLOR)};background-color:{self.settings.get(KEY_BACKGROUND_COLOR)};'
        )

        # Connect the menu items
        self.actionConnect.triggered.connect(self.connect)
        self.actionAbout.triggered.connect(self.aboutQt)
        self.actionChip_Select.triggered.connect(self.get_chip_part)
        self.actionShow_Logs.triggered.connect(self.show_log)
        self.actionChange_font.triggered.connect(self.choose_font)
        self.actionManual_Control.triggered.connect(self.manual_control)
        self.actionModify_Settings.triggered.connect(self.modify_settings)
        self.actionAdd_User.triggered.connect(self.add_user)
        self.actionRemove_User.triggered.connect(self.remove_user)

        self.actionEAX300.triggered.connect(self.deviceSelect)
        self.actionEAX500.triggered.connect(self.deviceSelect)
        self.actionEAX503.triggered.connect(self.deviceSelect)
        self.actionEAX504.triggered.connect(self.deviceSelect)
        self.actionEAX505.triggered.connect(self.deviceSelect)
        self.actionEAX510.triggered.connect(self.deviceSelect)
        self.actionEAX513.triggered.connect(self.deviceSelect)
        self.actionEAX514.triggered.connect(self.deviceSelect)
        self.actionEAX515.triggered.connect(self.deviceSelect)
        self.actionEAX520.triggered.connect(self.deviceSelect)
        self.actionEAX523.triggered.connect(self.deviceSelect)
        self.actionEAX524.triggered.connect(self.deviceSelect)
        self.actionEAX525.triggered.connect(self.deviceSelect)

        self.actionLogout.triggered.connect(self.do_login)
        self.program_button.clicked.connect(self.program)
        self.test_button.clicked.connect(self.run_test)
        self.button_pressed = False
        self.blinker_running = False
        self.testing = False
        self.waiting = False
        self.blocked = False
        self.connecting = False
        self.firmware = None
        self.device_name = None
        self.log_view = None
        self.load_text_from_file()

        # The device
        self.eax_device = None

        # USB device
        self.device = None

        # Auto Connect
        if settings.get(KEY_AUTO_CONNECT):
            QTimer.singleShot(2000, self.connect)

    def deviceSelect(self):
        # Uncheck all other actions
        for action in self.menuDevice.actions():
            if action.text() != self.sender().text():
                action.setChecked(False)


        # Uncheck the device label if the same action is clicked
        if self.eax_device is not None and not self.sender().isChecked():
            self.device_label.setStyleSheet(DEVICE_LABEL)
            self.device_label.setText("")
            self.eax_device = None
            return
        
        self.eax_device = Device(self.sender().text())
        self.device_label.setText(f"Device: {self.eax_device.name}")

        # Set the color of the device label
        if self.eax_device.get_name() == "EAX300":
            self.device_label.setStyleSheet(YELLOW)
        elif self.eax_device.get_name() == "EAX500":
            self.device_label.setStyleSheet(GREEN)
        else:
            self.device_label.setStyleSheet(ORANGE)

        print(self.eax_device)


    def choose_font(self):
        old_font = self.text_edit.font()

        (ok, font) = QFontDialog.getFont(
            QFont(old_font.family(), old_font.pointSize()), self
        )

        if ok:
            if self.settings.get(KEY_DEBUG):
                print(f"User selected font: {font.toString()}")
                lgr.debug(f"User selected font: {font.toString()}")
            self.text_edit.setFont(font)
            self.settings.set(KEY_FONT_FAMILY, QFontInfo(font).family())
            self.settings.set(KEY_FONT_SIZE, font.pointSize())

    def get_chip_part(self):
        self.settings.load()
        current_chip = self.settings.get(KEY_CHIP_PART)
        current_selection = CHIP_PARTS.index(current_chip)
        item, okPressed = QInputDialog.getItem(
            self, "Get item", "Chip Select:", CHIP_PARTS, current_selection, False
        )
        if okPressed and item:
            self.settings_dialog.comboBox_chip.setCurrentText(
                item
            )  # update the combo box
            self.settings.set(KEY_CHIP_PART, item)
            print('saved "' + item + '" to settings.')

    def eventFilter(self, watched, event):
        if event.type() in (QEvent.MouseMove, QEvent.KeyPress):
            # Reset the inactivity timer if a mouse movement or key press event is detected
            self.inactivityTimer.start(
                self.settings.get(KEY_LOGOFF_DELAY) * 60 * 1000
            )  # 60 seconds of inactivity before timeout
        return super(MainWindow, self).eventFilter(watched, event)

    def onInactivityTimeout(self):
        if self.settings.get(KEY_DEBUG):
            print("Inactivity timeout.")
            app_logger.debug("Inactivity timeout.")
            lgr.debug("Inactivity timeout.")
        if not self.settings.get(KEY_AUTO_LOGIN):
            self.do_login()

    def add_user(self):
        self.add = AddUserDialog()
        self.add.show()

    def remove_user(self):
        self.remove = RemoveUserDialog()
        self.remove.show()

    def add_text(self, text):
        """
        Add text to the text area.

        :param text: The text to add.
        """
        self.text_edit.append("\n" + text)
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.ensureCursorVisible()

    def add_markdown(self, text):
        # t = self.text_edit.toMarkdown()
        # t += "\n### "+text
        self.text_edit.setMarkdown(text)
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.ensureCursorVisible()

    def load_text_from_file(self, filename="instructions.txt"):
        """
        Load text from a file and add it to the text area.

        :param filename: The name of the file to load.
        """

        self.text_edit.setMarkdown(INSTRUCTIONS + "   \r\n")
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.ensureCursorVisible()
        return
        if os.path.exists(filename):
            with open(filename, "r") as file:
                content = file.read()
            self.text_edit.setMarkdown(content)
            self.text_edit.moveCursor(QtGui.QTextCursor.End)
            self.text_edit.ensureCursorVisible()
        else:
            self.add_text(f"{filename} not found!")

    def about(self):
        QMessageBox.information(
            self, "Going pro!", "QMainWindow,Qt Designer and Resources : Going pro!"
        )

    def aboutQt(self):
        QApplication.aboutQt()

    def connect(self):
        if self.connecting:
            return

        if self.device is None:
            self.device = USBHandler(
                _port=self.settings.get(KEY_COM_PORT),
                device_connected_callback=self.device_connected_callback,
                arduino_instance_id=self.settings.get(KEY_ARDUINO_INSTANCE_ID),
                wait=self.settings.get(KEY_ARDUINO_WAIT),
                shutdown_on_exception=self.settings.get(KEY_SHUTDOWN_ON_EXCEPTION),
                sleep_tune=self.settings.get(KEY_SLEEP_TUNE),
                debug=self.settings.get(KEY_DEBUG),
            )

        if not self.device.is_connected():
            self.connecting = True
            self.usb_label.setStyleSheet(YELLOW)
            self.usb_label.setText("USB: Connecting...")
            self.label_usb_icon.setStyleSheet(ICON_USB_BACKGROUND_YLW)
            self.device.connect(self.device_connected_callback)

    def device_connected_callback(self, connected, error=None):
        global usb_device
        if connected:
            self.label_usb_icon.setStyleSheet(ICON_USB_BACKGROUND_GRN)
            self.usb_label.setStyleSheet(GREEN)
            self.usb_label.setText(f"USB: {self.device.serial_port.port}")
            self.actionConnect.setText("Disconnect")
            self.connect_menu.setEnabled(False)
            self.actionConnect.triggered.connect(self.disconnect)
            self.actionConnect.triggered.disconnect(self.connect)
            if self.settings.get(KEY_DEBUG):
                app_logger.debug(f"USB: connected to {self.device.serial_port.port}")
            lgr.success(f"USB: connected to {self.device.serial_port.port}")
        else:
            print(f'Error: {error}')    
            lgr.error(f'Error: {error}')
            if self.settings.get(KEY_DEBUG):
                app_logger.error(f"USB: connection failed. Error: {error}")
                lgr.error(f"USB: connection failed. Error: {error}")
            self.label_usb_icon.setStyleSheet(ICON_USB_BACKGROUND_RED)
            self.connect_menu.setEnabled(True)
            self.actionConnect.setText("Connect")
            self.usb_label.setStyleSheet(RED)
            self.usb_label.setText("USB: connection failed")
            self.device = None

        usb_device = self.device
        self.connecting = False

    def disconnect(self):
        global usb_device
        if self.device is not None:
            self.device.set_all_pins(0)
            self.actionConnect.setText("Connect")
            self.connect_menu.setEnabled(True)
            self.actionConnect.triggered.connect(self.connect)
            self.actionConnect.triggered.disconnect(self.disconnect)
            self.label_usb_icon.setStyleSheet(ICON_USB_BACKGROUND_RED)
            self.usb_label.setStyleSheet(RED)
            self.usb_label.setText("USB: disconnected")
            if self.settings.get(KEY_DEBUG):
                app_logger.debug("USB: disconnected.")
                lgr.debug("USB: disconnected.")
            self.device.cleanup()
            self.device = None
            usb_device = None

    def manual_control(self):
        self.manual = ManualWidget(self.device)
        self.manual.show()

    def run_test(self):
        """ Run the test. """
        if self.testing:
            self.button_pressed = True
        elif not self.blocked:
            if self.device is None:
                QMessageBox.warning(
                    self, "Error", f"USB device not connected.", QMessageBox.Ok
                )
                return
            elif not self.device.is_connected():
                QMessageBox.warning(
                    self, "Error", f"USB device not connected.", QMessageBox.Ok
                )
                return
            self.blinker_running = False
            app_logger.info(f"Testing started for {self.eax_device.name}")
            lgr.info(f"Testing started for {self.eax_device.name}")
            
            self.queue = []

            speed = self.settings.get(KEY_TESTING_SPEED)

            # self.text_edit.setText("")
            self.text_edit.setMarkdown(f"# Starting test for {self.eax_device.name}... ")

            self.queue.append(  # turn on indicator
                (1, self.device.write_pin_by_func, "testing indicator", 1)
            )

            self.queue.append(
                (
                    int(speed / 4),
                    self.add_text,
                    " - Turning on battery power...",
                )
            )

            self.queue.append(  # turn on battery
                ((1), self.device.write_pin_by_func, "battery", 1)
            )

            self.queue.append(
                (
                    int(speed),
                    self.add_text,
                    " - Starting low battery test...",
                )
            )

            self.queue.append(  # turn on low battery
                ((1), self.device.write_pin_by_func, "low battery", 1)
            )

            self.queue.append((int(speed), self.add_text, " - Low battery test off."))

            self.queue.append(  # turn off low battery
                ((1), self.device.write_pin_by_func, "low battery", 0)
            )

            self.queue.append(
                (
                    int(500),
                    self.add_text,
                    (
                        " - Perform the following:\n\t  1. Press the key switch: The"
                        " siren sounds\n\t  2. Press the cylinder switch: The LEDs"
                        " turn on"
                    ),
                )
            )

            self.queue.append(
                (
                    int(200),
                    self.add_text,
                    "\n\nPress the Continue button to finish testing...",
                )
            )

            self.queue.append((1, self.wait_for_button))

            self.queue.append(  # turn off battery
                ((1), self.device.write_pin_by_func, "battery", 0)
            )

            # self.queue.append((10, self.clear_text))

            self.queue.append((10, self.load_text_from_file, "instructions.txt"))

            self.queue.append(  # turn off indicator
                ((1), self.device.write_pin_by_func, "testing indicator", 0)
            )

            self.testing = True
            self.blocked = True
            # Start processing the queue
            self.process_queue()

        else:
            self.add_text("Cannot run test.")
            app_logger.warn(f"Testing for {self.eax_device.name} was blocked.")

    def process_queue(self):
        """Process the queue."""
        if self.waiting:
            return
        if self.queue:
            delay, task, *args = self.queue.pop(0)  # Get the next task
            QTimer.singleShot(
                delay, lambda: self.execute_task(task, args)
            )  # Execute the task after the delay
        else:
            self.blocked = False
            self.testing = False

    def modify_settings(self):
        self.settings_dialog.show()

    def on_settings_closed(self, result):
        global settings
        self.settings = settings
        lgr.info(f"Settings dialog closed. Result: {result}")
        self.text_edit.setStyleSheet(
            f"color: {self.settings.get(KEY_FOREGROUND_COLOR)}; background-color:"
            f" {self.settings.get(KEY_BACKGROUND_COLOR)};"
        )
        if self.settings.get(KEY_AUTO_LOGIN):
            self.actionLogout.setEnabled(False)
        else:
            self.actionLogout.setEnabled(True)

    def wait_for_button(self):
        self.waiting = True
        if not self.button_pressed:
            QTimer.singleShot(100, self.wait_for_button)
            self.test_button.setText("Continue")
        else:
            self.test_button.setText("Test")
            self.button_pressed = False
            self.waiting = False
            self.process_queue()

    def execute_task(self, task, args):
        """
        Execute a task.

        :param task: The task to execute.
        :param args: The arguments to pass to the task.
        """
        task(*args)
        self.process_queue()  # Continue processing the queue

    def program(self):
        """Program the device."""
        if not self.blocked and self.eax_device is not None:
            # Check if the firmware file exists
            if not os.path.exists(self.eax_device.get_firmware()):
                self.add_text(f"{self.eax_device.get_firmware()} not found!")
                return

            self.settings.load()

            chip = self.settings.get("chip_part")
            serial = self.settings.get("programmer_serial_number")
            command = [
                "up.exe",
                f"/part {chip}",
                f"/s {serial}",
                f"/p {self.eax_device.get_firmware()}",
                "/q1",
            ]

            if self.settings.get("debug"):
                print(" ".join(command))

            self.blocked = True

            app_logger.info(f"Programming {self.eax_device.name} args: {command}")
            self.runner = CommandRunner(command)
            self.runner.resultReady.connect(
                self.handleResult
            )  # Connect the signal to the handler
            self.runner.start()

    def handleResult(self, returncode):
        # This function gets called when the command finishes.
        # Do whatever you need to do with the return code here.
        if returncode == 0:
            self.add_text("Programming successful.")
            app_logger.info(f"Programming {self.eax_device.name} successful")
            lgr.success(f"Programming {self.eax_device.name} successful")
            if self.settings.get(KEY_AUTO_TEST):
                self.run_test()
        else:
            lgr.error(f"Programming {self.eax_device.name} failed. Error code: {returncode}")
            self.add_text(
                f"\nProgramming {self.eax_device.name} failed. Error code: {returncode}"
            )
            app_logger.error(
                f"Programming {self.eax_device.name} failed. Error code: {returncode}"
            )
        self.blocked = False

    def show_log(self):
        """Show the logs in the text area."""
        logs = AppLogger.get_table()
        self.log_view = LogView(logs, 4, 3)
        self.log_view.show()

    def do_login(self):
        loginDialog = LoginDialog(self.settings.get(KEY_LAST_USER))
        success, username = False, None

        while not success:
            if loginDialog.exec() == QDialog.Accepted:
                success, username = loginDialog.ok()
                if not success:
                    QMessageBox.critical(
                        self,
                        "Invalid credentials",
                        (
                            "The username or password you entered is incorrect. Please"
                            " try again."
                        ),
                    )
            else:
                if (
                    QMessageBox.question(
                        self,
                        "Confirmation",
                        "Are you sure you want to exit?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.No,
                    )
                    == QMessageBox.Yes
                ):
                    if self.device is not None:
                        if self.device.is_connected():
                            self.device.cleanup()
                    sys.exit(0)

        # Now 'username' contains the username of the logged-in user
        lgr.success(f"Logged in as: {username}")
        app_logger.info(f"Logged in as: {username}")

        # Block if the user is not an admin
        self.actionModify_Settings.setEnabled(db.is_admin(username))
        self.actionAdd_User.setEnabled(db.is_admin(username))
        self.actionRemove_User.setEnabled(db.is_admin(username))
        self.settings.set(KEY_LAST_USER, username)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Window Close",
            "Are you sure you want to close the window?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply == QMessageBox.Yes:
            if usb_device is not None:
                if usb_device.is_connected():
                    usb_device.cleanup()
            lgr.info("Application closed.")
            db.close()
            event.accept()
        else:
            event.ignore()

    def show(self):
        super().show()
        if not self.settings.get(KEY_AUTO_LOGIN):
            self.do_login()
        else:
            self.actionLogout.setEnabled(False)


class ManualWidget(QWidget, Ui_ManualControlDialog):
    def __init__(self, usb_handler=None):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.usb_device = usb_handler

        if self.usb_device is None or not self.usb_device.is_connected():
            QMessageBox.warning(
                self, "Error", f"USB device not connected.", QMessageBox.Ok
            )
            self.close()
            return
        self.battery_button.clicked.connect(self.toggle_battery)
        self.low_battery_button.clicked.connect(self.toggle_low_battery)
        self.test_indicator_button.clicked.connect(self.toggle_testing_indicator)
        self.indicator_button.clicked.connect(self.toggle_indicator)

    def toggle_battery(self, checked):
        if checked:
            value = 1
        else:
            value = 0
        self.usb_device.write_pin_by_func("battery", value)

    def toggle_low_battery(self, checked):
        if checked:
            value = 1
        else:
            value = 0
        self.usb_device.write_pin_by_func("low battery", value)

    def toggle_testing_indicator(self, checked):
        if checked:
            value = 1
        else:
            value = 0
        self.usb_device.write_pin_by_func("testing indicator", value)

    def toggle_indicator(self, checked):
        if checked:
            value = 1
        else:
            value = 0
        self.usb_device.write_pin_by_func("indicator", value)

    def closeEvent(self, event):
        if self.usb_device is not None:
            if self.usb_device.is_connected():
                self.usb_device.set_all_pins(0)
                self.usb_device.write_pin_by_func("indicator", 1)
        event.accept()


from serial.serialutil import SerialException
from serial.tools import list_ports, list_ports_windows
from private import Private
from ui_Settings import Ui_Settings


class SettingsDialog(QWidget, Ui_Settings):
    closed = QtCore.Signal(int)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        global settings
        self.settings = settings
        self.settings.load()
        if not self.settings.validate():
            QMessageBox.warning(
                self,
                "Error",
                f"Error loading settings. File not found.",
                QMessageBox.Ok,
            )
            self.close()
            return

        for port in Private.get_com_ports():
            self.comboBox_com_port.addItem(port)

        self.commandLinkButton_select_color.clicked.connect(self.choose_color)
        self.commandLinkButton_bg_color.clicked.connect(self.choose_background_color)

        for i in range(CHIP_PARTS.__len__()):
            self.comboBox_chip.addItem(CHIP_PARTS[i])
        self.comboBox_chip.setCurrentIndex(
            CHIP_PARTS.index(self.settings.get(KEY_CHIP_PART))
        )

        self.spinBox_autologoff_delay.setValue(self.settings.get(KEY_LOGOFF_DELAY))
        value = self.settings.get(KEY_TESTING_SPEED)
        self.dial.setValue(value)
        self.spinBox_arduino_id.setValue(self.settings.get(KEY_ARDUINO_INSTANCE_ID))
        self.lineEdit_serial.setText(self.settings.get(KEY_PROGRAMMER_SERIAL_NUMBER))
        self.checkBox_test.setChecked(self.settings.get(KEY_AUTO_TEST))
        self.checkBox_connect.setChecked(self.settings.get(KEY_AUTO_CONNECT))
        self.checkBox_debug.setChecked(self.settings.get(KEY_DEBUG))
        self.checkBox_logon.setChecked(self.settings.get(KEY_AUTO_LOGIN))
        self.pushButton_save.clicked.connect(self.save)

        self.checkBox_auto_find.setChecked(self.settings.get(KEY_AUTO_FIND))
        self.checkBox_shutdown_on_exception.setChecked(
            self.settings.get(KEY_SHUTDOWN_ON_EXCEPTION)
        )
        self.lineEdit_serial_sleep_tune.setText(str(self.settings.get(KEY_SLEEP_TUNE)))
        self.spinBox_wait_time.setValue(self.settings.get(KEY_ARDUINO_WAIT))

        lcd = self.lcdNumber
        palette = lcd.palette()
        palette.setColor(QPalette.WindowText, Qt.blue)
        lcd.setPalette(palette)

    # def dial_changed(self, value):
    # self.label_speed.setText(f"{DEFAULT_TESTING_SPEED/1000*value/100.0}s")

    def save(self):
        self.settings.set(KEY_COM_PORT, self.comboBox_com_port.currentText())
        self.settings.set(KEY_CHIP_PART, self.comboBox_chip.currentText())
        self.settings.set(KEY_PROGRAMMER_SERIAL_NUMBER, self.lineEdit_serial.text())
        self.settings.set(KEY_AUTO_TEST, self.checkBox_test.isChecked())
        self.settings.set(KEY_AUTO_CONNECT, self.checkBox_connect.isChecked())
        self.settings.set(KEY_DEBUG, self.checkBox_debug.isChecked())
        self.settings.set(KEY_AUTO_LOGIN, self.checkBox_logon.isChecked())
        self.settings.set(KEY_ARDUINO_INSTANCE_ID, self.spinBox_arduino_id.value())
        self.settings.set(KEY_TESTING_SPEED, self.dial.value())
        self.settings.set(KEY_LOGOFF_DELAY, self.spinBox_autologoff_delay.value())
        self.settings.set(KEY_AUTO_FIND, self.checkBox_auto_find.isChecked())
        self.settings.set(
            KEY_SHUTDOWN_ON_EXCEPTION, self.checkBox_shutdown_on_exception.isChecked()
        )
        self.settings.set(KEY_SLEEP_TUNE, float(self.lineEdit_serial_sleep_tune.text()))
        self.settings.set(KEY_ARDUINO_WAIT, self.spinBox_wait_time.value())
        self.settings.save()
        self.close()

    def choose_color(self):
        old_color = QColor(self.settings.get(KEY_FOREGROUND_COLOR))
        color = QColorDialog.getColor(old_color, self)
        if color.isValid():
            print(f"User selected color: {color.name()}")
            self.settings.set(KEY_FOREGROUND_COLOR, f"{color.name()}")

    def choose_background_color(self):
        old_color = QColor(self.settings.get(KEY_BACKGROUND_COLOR))
        color = QColorDialog.getColor(old_color, self)
        if color.isValid():
            print(f"User selected color: {color.name()}")
            self.settings.set(KEY_BACKGROUND_COLOR, f"{color.name()}")

    def closeEvent(self, event):
        self.settings.load()
        self.closed.emit(0)
        event.accept()


from PySide6.QtWidgets import QDialog
from ui_AddUserDialog import Ui_AddUserDialog
from PySide6.QtWidgets import QLineEdit
from user import User, SingleUser


class AddUserDialog(QDialog, Ui_AddUserDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

        self.users = db.get_users()

    def save(self):
        print(self.lineEdit_username.text())
        print(self.lineEdit_password.text())
        admin = self.checkBox.isChecked()
        db.insert_user(
            self.lineEdit_username.text(), self.lineEdit_password.text(), admin
        )
        self.close()


from ui_RemoveUserDialog import Ui_RemoveUserDialog


class RemoveUserDialog(QDialog, Ui_RemoveUserDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.us = db.to_dict()
        for user in self.us:
            self.comboBox.addItem(user["username"])

        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

    def save(self):
        selected_username = self.comboBox.currentText()
        if selected_username == "dmh":
            QMessageBox.critical(
                self,
                "Error",
                f"Cannot remove user: {selected_username}",
                QMessageBox.Ok,
            )
            self.close()
            return
        db.remove_user(selected_username)


from ui_LoginDialog import Ui_LoginDialog


class LoginDialog(QDialog, Ui_LoginDialog):
    def __init__(self, last_user=None):
        super().__init__()
        self.setupUi(self)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        if settings.get(KEY_DEBUG):
            print(db.get_users())
            lgr.debug(db.get_users())

        for user in db.to_dict():
            self.comboBox.addItem(user["username"])
        self.comboBox.setCurrentText(last_user)

        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)

    def ok(self):
        selected_username = self.comboBox.currentText()
        selected_password = self.lineEdit_password.text()
        validate = db.check_password(selected_username, selected_password)
        return (validate, selected_username)

    def cancel(self):
        return (False, None)


from PySide6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem
from ui_LogView import Ui_LogView


class LogView(QWidget, Ui_LogView):
    def __init__(self, data, *args):
        super().__init__()
        self.setupUi(self)
        self.data = data
        self.tableWidget.setRowCount(len(self.data))
        self.setData()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def setData(self):
        horHeaders = ["Date", "Level", "Message"]
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                newitem = QTableWidgetItem(self.data[i][j])
                self.tableWidget.setItem(i, j, newitem)
        self.tableWidget.setHorizontalHeaderLabels(horHeaders)


from PySide6.QtCore import QThread, Signal


class CommandRunner(QThread):
    resultReady = Signal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.run(" ".join(self.command))
        self.resultReady.emit(process.returncode)


from PySide6.QtWidgets import QMenu


class ConnectMenu(QMenu):
    menu_clicked = Signal()

    def showEvent(self, event):
        self.menu_clicked.emit()
        super().showEvent(event)


def check_requirements():
    missing = ""
    for file in FILES:
        if not os.path.exists(file):
            missing += file + "\n"
    if missing != "":
        print(f"Missing files:\n{missing}")
        return (False, missing)
    return (True, None)


if __name__ == "__main__":
    app = QApplication([])
    (success, missing) = check_requirements()
    if not success:
        QMessageBox.critical(
            None, "Error", f"Missing files:\n{missing}", QMessageBox.Ok
        )
        sys.exit(1)
    window = MainWindow(app)
    window.show()
    app.exec()
