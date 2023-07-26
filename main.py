from PySide6 import QtCore, QtGui
from PySide6.QtCore import QTimer, QEvent, Slot
from PySide6.QtWidgets import (QApplication, QMainWindow,QMessageBox, QColorDialog, QWidget, QFontDialog, QPushButton, QVBoxLayout)
from PySide6.QtGui import (QFont, QFontInfo, QColor, QMouseEvent)

from ui_ManualControlDialog import Ui_ManualControlDialog
from ui_MainWindow import Ui_MainWindow

import os, sys, subprocess, threading
from constants import *
from applogger import AppLogger
from usbhandler import USBHandler
from settings import Settings
from user import User
from rich import print

import resource_rc #You need to manually import the compiled resource file


app_logger = AppLogger("logger").get_logger()
timer = QTimer()
settings = Settings("settings.json")
users = User("users.json")
usb_device = None


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,app):
        super().__init__()
        self.setupUi(self)
        self.app = app

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

        self.text_edit.setFont(
            QFont(self.settings.get(KEY_FONT_FAMILY), 
                  self.settings.get(KEY_FONT_SIZE),
            )
        )
        self.text_edit.setStyleSheet(f"color: {self.settings.get(KEY_FOREGROUND_COLOR)}; background-color: {self.settings.get(KEY_BACKGROUND_COLOR)};")

        self.actionConnect.triggered.connect(self.connect)
        self.actionAbout.triggered.connect(self.aboutQt)
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
        self.firmware = None
        self.device_name = None
        self.connecting = False
        self.load_text_from_file()

        # USB
        self.device = USBHandler(
            port=self.settings.get(KEY_COM_PORT),
            device_connected_callback=self.device_connected_callback, 
            arduino_instance_id=self.settings.get(KEY_ARDUINO_INSTANCE_ID)
        )

        # Auto Connect
        if settings.get(KEY_AUTO_CONNECT):
            QTimer.singleShot(2000, self.connect)

    def deviceSelect(self):
        for action in self.menuDevice.actions():
            if action.text() != self.sender().text():
                action.setChecked(False)
        self.device_label.setText("Device: " + self.sender().text())
        orange = "color: rgb(229, 153, 0);"
        green = "color: green;"
        yellow = "color: rgb(189, 177, 46);"

        if (self.sender().text() == "EAX300"):
            self.device_label.setStyleSheet(yellow)
        elif (self.sender().text() == "EAX500"):
            self.device_label.setStyleSheet(green)
        else:
            self.device_label.setStyleSheet(orange)

        self.device_name = self.sender().text()

        if self.device_name == "EAX300":
            self.firmware = "firmware/" + self.device_name + "_59.hex"
        else:
            self.firmware = "firmware/" + self.device_name + "_591.hex"

    def choose_font(self):
        old_font = self.text_edit.font()
        
        (ok, font) = QFontDialog.getFont(QFont(old_font.family(),old_font.pointSize()), self)
        
        if ok:
            if self.settings.get(KEY_DEBUG):
                print(f"User selected font: {font.toString()}")
            self.text_edit.setFont(font)
            self.settings.set(KEY_FONT_FAMILY, QFontInfo(font).family())
            self.settings.set(KEY_FONT_SIZE, font.pointSize())

    def quit(self):
        print("Quit")
        self.app.quit()

    def eventFilter(self, watched, event):
        if event.type() in (QEvent.MouseMove, QEvent.KeyPress):
            # Reset the inactivity timer if a mouse movement or key press event is detected
            self.inactivityTimer.start(self.settings.get(KEY_LOGOFF_DELAY) * 60 * 1000)  # 60 seconds of inactivity before timeout
        return super(MainWindow, self).eventFilter(watched, event)

    def onInactivityTimeout(self):
        if self.settings.get(KEY_DEBUG):
            print("Inactivity timeout.")
        app_logger.info("Inactivity timeout.")
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
        self.text_edit.append("\n"+text)
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
        
        self.text_edit.setMarkdown(INSTRUCTIONS+"   \r\n")
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
        QMessageBox.information(self,"Going pro!","QMainWindow,Qt Designer and Resources : Going pro!")
    
    def aboutQt(self):
        QApplication.aboutQt()
    
    def connect(self):
        if self.connecting:
            return
        if self.device is not None:
            if not self.device.is_connected():
                self.connecting = True
                self.device.connect(self.device_connected_callback)
                self.usb_label.setStyleSheet("color: rgb(189, 177, 46);")
                self.usb_label.setText("USB: Connecting...")
        else:
            self.device = USBHandler(
                port=self.settings.get(KEY_COM_PORT),
                device_connected_callback=self.device_connected_callback,
                arduino_instance_id=self.settings.get(KEY_ARDUINO_INSTANCE_ID)
            )
            self.device.connect(self.device_connected_callback)

    def device_connected_callback(self, connected, error=None):
        global usb_device
        self.usb_label.setText("USB: " + str(connected))
        if connected :
            self.usb_label.setStyleSheet("color: green;") 
            self.usb_label.setText("USB: " + str(self.device.serial_port.port))
            self.actionConnect.setText("Disconnect")
            self.actionConnect.triggered.connect(self.disconnect)
            self.actionConnect.triggered.disconnect(self.connect)
        else:
            self.actionConnect.setText("Connect")
            self.usb_label.setStyleSheet("color: rgb(200, 0, 0);")
            self.usb_label.setText("USB: connection failed")
            app_logger.error(f"USB: connection failed.")
            self.device = None
        usb_device = self.device
        self.connecting = False
        
    def disconnect(self):
        global usb_device
        if self.device is not None:
            self.device.set_all_pins(0)
            self.actionConnect.setText("Connect")
            self.actionConnect.triggered.connect(self.connect)
            self.actionConnect.triggered.disconnect(self.disconnect)
            self.usb_label.setStyleSheet("color: rgb(200, 0, 0);")
            self.usb_label.setText("USB: disconnected")
            app_logger.info(f"USB: disconnected.")
            self.device.cleanup()
            self.device = None
            usb_device = None
    
    def manual_control(self):
        self.manual = ManualWidget(self.device)
        self.manual.show()

    def run_test(self):
        """Run the test."""
        if self.testing:
            self.button_pressed = True
        elif not self.blocked:# and self.device is not None and self.device.is_connected():
            self.blinker_running = False
            app_logger.info(f"# Testing {self.device_name} started")
            # Clear the queue
            self.queue = []
            speed = self.settings.get("testing_speed")

            # self.text_edit.setText("")
            self.text_edit.setMarkdown(f"# Starting test for {self.device_name}... ")

            self.queue.append(  # turn on indicator
                (1, self.device.write_pin_by_func, "testing indicator", 1)
            )

            self.queue.append(
                (
                    int(DEFAULT_TESTING_SPEED * speed),
                    self.add_text,
                    " - Turning on battery power...",
                )
            )

            self.queue.append(  # turn on battery
                ((1), self.device.write_pin_by_func, "battery", 1)
            )

            self.queue.append(
                (
                    int(DEFAULT_TESTING_SPEED * speed),
                    self.add_text,
                    " - Starting low battery test...",
                )
            )

            self.queue.append(  # turn on low battery
                ((1), self.device.write_pin_by_func, "low battery", 1)
            )

            self.queue.append((int(2000 * speed), self.add_text, " - Low battery test off."))

            self.queue.append(  # turn off low battery
                ((1), self.device.write_pin_by_func, "low battery", 0)
            )

            self.queue.append(
                (
                    int(1000 * speed),
                    self.add_text,
                    " - Perform the following:\n\t  1. Press the key switch: The siren sounds\n\t  2. Press the cylinder switch: The LEDs turn on",
                )
            )

            self.queue.append((int(100 * speed), self.add_text, "\n\nPress the Continue button to finish testing..."))

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
            app_logger.error(f"Testing {self.device} blocked.")

    def process_queue(self):
        """Process the queue."""
        if self.waiting:
            return
        if self.queue:
            delay, task, *args = self.queue.pop(0)  # Get the next task
            QTimer.singleShot(delay, lambda: self.execute_task(task, args))  # Execute the task after the delay
        else:
            self.blocked = False
            self.testing = False

    def modify_settings(self):
        self.settings_dialog.show()

    def on_settings_closed(self, result):
        print(f"Settings dialog closed. Result: {result}")
        self.text_edit.setStyleSheet(f"color: {self.settings.get(KEY_FOREGROUND_COLOR)}; background-color: {self.settings.get(KEY_BACKGROUND_COLOR)};")
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
        if not self.blocked and self.firmware is not None:
            # Check if the firmware file exists
            if not os.path.exists(self.firmware):
                self.add_text(f"{self.firmware} not found!")
                return

            self.settings.load()

            chip = self.settings.get("chip_part")
            serial = self.settings.get("programmer_serial_number")
            command = ["up.exe", f"/part {chip}",f"/s {serial}",f"/p {self.firmware}","/q1"]

            if self.settings.get("debug"):
                print(" ".join(command))

            self.blocked = True

            app_logger.info(f"Programming {self.device_name} args: {command}")
            self.runner = CommandRunner(command)
            self.runner.resultReady.connect(self.handleResult)  # Connect the signal to the handler
            self.runner.start()

    def handleResult(self, returncode):
        # This function gets called when the command finishes.
        # Do whatever you need to do with the return code here.
        print(returncode)
        if returncode == 0:
            if self.settings.get(KEY_AUTO_TEST):
                self.run_test()
            self.add_text("Programming successful.")
            app_logger.info(f"Programming {self.device_name} successful")
        else:
            self.add_text(f"\nProgramming {self.device_name} failed. Error code: {returncode}")
            app_logger.error(
                f"Programming {self.device_name} failed. Error code: {returncode}"
            )
        self.blocked = False

    def show_log(self):
        """Show the logs in the text area."""
        self.text_edit.setText("")
        self.add_text("Logs:")
        self.add_text(AppLogger.get_logs())

    def do_login(self):
        loginDialog = LoginDialog(self.settings.get(KEY_LAST_USER))
        success, username = False, None

        while not success:
            if loginDialog.exec() == QDialog.Accepted:
                success, username = loginDialog.ok()
                if not success:
                    QMessageBox.critical(self, "Invalid credentials", "The username or password you entered is incorrect. Please try again.")
            else:
                if QMessageBox.question(self, "Confirmation", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                    if self.device is not None:
                        if self.device.is_connected():
                            self.device.cleanup()
                    sys.exit(0)

        # Now 'username' contains the username of the logged-in user
        print(f"Logged in as: {username}")
        app_logger.info(f"Logged in as: {username}")
        self.statusbar.showMessage(f"Logged in as: {username}")

        # Block if the user is not an admin
        self.actionModify_Settings.setEnabled(users.is_admin(username))
        self.actionAdd_User.setEnabled(users.is_admin(username))
        self.actionRemove_User.setEnabled(users.is_admin(username))
        self.settings.set(KEY_LAST_USER, username)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            if usb_device is not None:
                if usb_device.is_connected():
                    usb_device.cleanup()
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

        if self.usb_device is None:
            QMessageBox.warning(self, 'Error', f'USB device not connected.', QMessageBox.Ok)

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


from ui_SettingsDialog import Ui_Settings

class SettingsDialog(QWidget, Ui_Settings):
    
    closed = QtCore.Signal(int)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        global settings
        self.settings = settings
        self.settings.load()

        self.commandLinkButton_select_color.clicked.connect(self.choose_color)
        self.commandLinkButton_bg_color.clicked.connect(self.choose_background_color)

        if not self.settings.validate():
            QMessageBox.warning(self, 'Error', f'Error loading settings. File not found.', QMessageBox.Ok)

        for i in range(CHIP_PARTS.__len__()):
            self.comboBox_chip.addItem(CHIP_PARTS[i])
        self.comboBox_chip.setCurrentIndex(CHIP_PARTS.index(self.settings.get(KEY_CHIP_PART)))
        
        self.spinBox_autologoff_delay.setValue(self.settings.get(KEY_LOGOFF_DELAY))
        value = self.settings.get(KEY_TESTING_SPEED) * 100
        self.dial_changed(value)
        self.dial.setValue(value)
        self.dial.connect(self.dial, QtCore.SIGNAL("valueChanged(int)"), self.dial_changed)
        self.spinBox_arduino_id.setValue(self.settings.get(KEY_ARDUINO_INSTANCE_ID))
        self.lineEdit_port.setText(self.settings.get(KEY_COM_PORT))
        self.lineEdit_serial.setText(self.settings.get(KEY_PROGRAMMER_SERIAL_NUMBER))
        self.checkBox_test.setChecked(self.settings.get(KEY_AUTO_TEST))
        self.checkBox_connect.setChecked(self.settings.get(KEY_AUTO_CONNECT))
        self.checkBox_debug.setChecked(self.settings.get(KEY_DEBUG))
        self.checkBox_logon.setChecked(self.settings.get(KEY_AUTO_LOGIN))
        self.pushButton_save.clicked.connect(self.save)

    def dial_changed(self, value):
        self.label_speed.setText(f"{DEFAULT_TESTING_SPEED/1000*value/100.0}s")

    def save(self):
        self.settings.set("chip_part",self.comboBox_chip.currentText())
        self.settings.set("serial_port",self.lineEdit_port.text())
        self.settings.set("programmer_serial_number",self.lineEdit_serial.text())
        self.settings.set("auto_test",self.checkBox_test.isChecked())
        self.settings.set("auto_connect",self.checkBox_connect.isChecked())
        self.settings.set("debug",self.checkBox_debug.isChecked())
        self.settings.set("skip_login",self.checkBox_logon.isChecked())
        self.settings.set(KEY_ARDUINO_INSTANCE_ID,self.spinBox_arduino_id.value())
        self.settings.set("testing_speed",self.dial.value()/100)
        self.settings.set("auto_logoff_delay",self.spinBox_autologoff_delay.value())
        self.settings.save()
        self.close()

    def choose_color(self):
        old_color = QColor(self.settings.get(KEY_FOREGROUND_COLOR))
        color = QColorDialog.getColor(old_color, self)
        if color.isValid():
            print(f"User selected color: {color.name()}")
            self.settings.set(KEY_FOREGROUND_COLOR, f"{color.name()};")

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
from user import (User, SingleUser)
class AddUserDialog(QDialog,Ui_AddUserDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

        self.users = User("users.json")

    def save(self):
        print(self.lineEdit_username.text())
        print(self.lineEdit_password.text())
        admin = self.checkBox.isChecked()
        User.add_user(self.lineEdit_username.text(),self.lineEdit_password.text(),admin)
        self.close()

from ui_RemoveUserDialog import Ui_RemoveUserDialog

class RemoveUserDialog(QDialog, Ui_RemoveUserDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.us = User.load_users()
        for user in self.us:
            self.comboBox.addItem(user["username"])

        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

    def save(self):
        selected_username = self.comboBox.currentText()
        if selected_username == "dmh":
            QMessageBox.critical(self, 'Error', f'Cannot remove user: {selected_username}', QMessageBox.Ok)
            self.close()
            return
        removed = User.remove_user_s(selected_username)
        if removed:
            self.close()
        else:
            QMessageBox.warning(self, 'Error', f'Error removing user: {selected_username}', QMessageBox.Ok)


from ui_LoginDialog import Ui_LoginDialog

class LoginDialog(QDialog, Ui_LoginDialog):
    def __init__(self, last_user=None):
        super().__init__()
        self.setupUi(self)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
    
        if settings.get(KEY_DEBUG):
            print(users.get_users())

        for user in users.get_users():
            self.comboBox.addItem(user["username"])
        self.comboBox.setCurrentText(last_user)

        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)
        
    def ok(self):
        selected_username = self.comboBox.currentText()
        selected_password = self.lineEdit_password.text()
        validate = users.validate_credentials(selected_username, selected_password)
        return (validate, selected_username)

    def cancel(self):
        return (False, None)


from PySide6.QtCore import QThread, Signal

class CommandRunner(QThread):
    resultReady = Signal(int)  
    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.run(" ".join(self.command))
        self.resultReady.emit(process.returncode)


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
        QMessageBox.critical(None, "Error", f"Missing files:\n{missing}", QMessageBox.Ok)
        sys.exit(1)
    window = MainWindow(app)
    window.show()
    app.exec()


