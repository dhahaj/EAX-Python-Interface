from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow,QMessageBox
from PySide6.QtWidgets import QWidget
from PySide6 import QtCore

from ui_ManualControlDialog import Ui_ManualControlDialog
from ui_MainWindow import Ui_MainWindow
import os
import subprocess
from constants import *
from applogger import AppLogger
from usbhandler import USBHandler
import threading
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

        self.actionConnect.triggered.connect(self.connect)
        self.actionAbout.triggered.connect(self.aboutQt)
        self.actionShow_Logs.triggered.connect(self.show_log)
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

        self.actionLogout.triggered.connect(self._print)
        self.program_button.clicked.connect(self.program)
        self.test_button.clicked.connect(self.run_test)
        self.button_pressed = False
        self.blinker_running = False
        self.testing = False
        self.waiting = False
        self.blocked = False
        self.firmware = None
        self.device_name = None
        self.load_text_from_file()

        global settings
        self.settings = settings
        self.device = USBHandler(
            device_connected_callback=self.device_connected_callback, 
            arduino_instance_id=self.settings.get(KEY_ARDUINO_INSTANCE_ID)
        )

        # Auto Connect
        if settings.get(KEY_AUTO_CONNECT):
            QTimer.singleShot(2000, self.connect)


    def _print(self):
        print(self.sender())#.text())

    def deviceSelect(self):
        for action in self.menuDevice.actions():
            if action.text() != self.sender().text():
                action.setChecked(False)
        print(self.sender().text())
        self.statusbar.showMessage(self.sender().text())
        self.device_label.setText("Device: " + self.sender().text())
        orange = "color: rgb(229, 153, 0);"
        green = "color: green;"

        if (self.sender().text() == "EAX300") or (self.sender().text() == "EAX500"):
            self.device_label.setStyleSheet(green)
        else:
            self.device_label.setStyleSheet(orange)

        self.device_name = self.sender().text()

        if self.device_name == "EAX300":
            self.firmware = "firmware/" + self.device_name + "_59.hex"
        else:
            self.firmware = "firmware/" + self.device_name + "_591.hex"

    def quit(self):
        print("Quit")
        self.app.quit()

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
    

    def load_text_from_file(self, filename="instructions.txt"):
        """
        Load text from a file and add it to the text area.

        :param filename: The name of the file to load.
        """
        if os.path.exists(filename):
            with open(filename, "r") as file:
                content = file.read()
            self.text_edit.setMarkdown(content)
        else:
            self.add_text(f"{filename} not found!")

    def about(self):
        QMessageBox.information(self,"Going pro!","QMainWindow,Qt Designer and Resources : Going pro!")
    def aboutQt(self):
        QApplication.aboutQt()
    def connect(self):
        if self.device is not None:
            if not self.device.is_connected():
                self.device.connect(self.device_connected_callback)
                self.usb_label.setStyleSheet("color: rgb(189, 177, 46);")
                self.usb_label.setText("USB: Connecting...")
        else:
            self.device = USBHandler(
                device_connected_callback=self.device_connected_callback,
                arduino_instance_id=self.settings.get(KEY_ARDUINO_INSTANCE_ID)
            )
            self.device.connect(self.device_connected_callback)
            global usb_device
            usb_device = self.device

    def device_connected_callback(self, connected, error=None):
        self.usb_label.setText("USB: " + str(connected))
        if connected :
            self.usb_label.setStyleSheet("color: green;") 
            self.usb_label.setText("USB: " + str(self.device.serial_port.port))
        else:
            self.usb_label.setStyleSheet("color: rgb(200, 0, 0);")
            self.usb_label.setText("USB: connection failed")
            app_logger.error(f"USB: connection failed.")
            self.device = None
            global usb_device
            usb_device = None
    
    def manual_control(self):
        self.manual = ManualWidget(self.device)
        self.manual.show()

    def run_command(self, command):
        """
        Run a command in a separate thread.

        :param command: The command to run.
        """
        self.settings.load()
        process = subprocess.run(command)
        self.blocked = False
        # self.stop_blink()
        if process.returncode == 0:
            if self.settings.get("auto_test"):
                self.run_test()
            self.add_text("Programming successful.")
            app_logger.info(f"Programming {self.device_name} successful")
        else:
            self.add_text("Programming failed.")
            app_logger.error(
                f"Programming {self.device_name} failed. Error code: {process.returncode}"
            )

    def run_test(self):
        """Run the test."""
        if self.testing:
            self.button_pressed = True
        elif not self.blocked:# and self.device is not None and self.device.is_connected():
            self.blinker_running = False
            app_logger.info(f"Testing {self.device_name} started")
            # Clear the queue
            self.queue = []
            speed = self.settings.get("testing_speed")

            self.queue.append(  # turn on indicator
                (1, self.device.write_pin_by_func, "testing indicator", 1)
            )

            self.queue.append(  # Add tasks to the queue
                (100, self.add_text, f"Starting test for {self.device_name}...")
            )

            self.queue.append(
                (
                    int(DEFAULT_TESTING_SPEED * speed),
                    self.add_text,
                    "\nTurning on battery power...",
                )
            )

            self.queue.append(  # turn on battery
                ((1), self.device.write_pin_by_func, "battery", 1)
            )

            self.queue.append(
                (
                    int(DEFAULT_TESTING_SPEED * speed),
                    self.add_text,
                    "Starting low battery test...",
                )
            )

            self.queue.append(  # turn on low battery
                ((1), self.device.write_pin_by_func, "low battery", 1)
            )

            self.queue.append((int(2000 * speed), self.add_text, "Low battery off."))

            self.queue.append(  # turn off low battery
                ((1), self.device.write_pin_by_func, "low battery", 0)
            )

            self.queue.append(
                (
                    int(1000 * speed),
                    self.add_text,
                    "Perform the following:\n\t  1. Press the key switch: The siren sounds\n\t  2. Press the cylinder switch: The LEDs turn on",
                )
            )

            self.queue.append((int(100 * speed), self.add_text, "\n\nPress the Test button to continue."))

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
            self.text_edit.setText("")
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
            print("\nTask started")
            QTimer.singleShot(delay, lambda: self.execute_task(task, args))  # Execute the task after the delay
            # self.after(
            #     delay, lambda: self.execute_task(task, args)
            # )  # Execute the task after the delay
            print("Task executed\n")
        else:
            self.blocked = False
            self.testing = False

    def modify_settings(self):
        self.settings_widget = SettingsWidget()
        self.settings_widget.show()

    def wait_for_button(self):
        print(f"Waiting for button {self.button_pressed}")
        self.waiting = True
        if not self.button_pressed:
            QTimer.singleShot(100, self.wait_for_button)
        else:
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

            # self.blink_thread = threading.Thread(target=self.do_blink)
            # self.blink_thread.start()

            self.blinker_running = True
            self.settings.load()

            chip = self.settings.get("chip_part")
            serial = self.settings.get("programmer_serial_number")
            command = ["up.exe", f"/part {chip} /q1 /s {serial} /p {self.firmware}"]

            if self.settings.get("debug"):
                print(" ".join(command))

            thread = threading.Thread(target=self.run_command, args=(command,))
            self.blocked = True

            # if self.parent.settings.get("debug"):
            #     self.add_text("Running test...")
            #     self.run_test()

            app_logger.info(f"Programming {self.device_name} args: {command}")
            thread.start()

    def show_log(self):
        """Show the logs in the text area."""
        self.text_edit.setText("")
        self.add_text("Logs:")
        self.add_text(AppLogger.get_logs())

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

class ManualWidget(QWidget, Ui_ManualControlDialog):
    def __init__(self, usb_handler=None):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        global usb_device 

        self.usb_handler = usb_device

        self.battery_button.clicked.connect(self.toggle_battery)
        self.low_battery_button.clicked.connect(self.toggle_low_battery)
        self.test_indicator_button.clicked.connect(self.toggle_testing_indicator)
        self.indicator_button.clicked.connect(self.toggle_indicator)


    def toggle_battery(self, checked):
        pin = self.usb_handler.get_pin_by_function("battery")
        if checked:
            value = 1
        else:
            value = 0
        self.usb_handler.digital_write(pin, value)

    def toggle_low_battery(self, checked):
        pin = self.usb_handler.get_pin_by_function("low battery")
        if checked:
            value = 1
        else:
            value = 0
        self.usb_handler.digital_write(pin, value)

    def toggle_testing_indicator(self, checked):
        pin = self.usb_handler.get_pin_by_function("testing indicator")
        if checked:
            value = 1
        else:
            value = 0
        self.usb_handler.digital_write(pin, value)

    def toggle_indicator(self, checked):
        pin = self.usb_handler.get_pin_by_function("indicator")
        if checked:
            value = 1
        else:
            value = 0
        self.usb_handler.digital_write(pin, value)

    def closeEvent(self, event):
        if usb_device is not None:
            if usb_device.is_connected():
                usb_device.set_all_pins(0)
                usb_device.write_pin_by_func("indicator", 1)
        event.accept()


from ui_Settings import Ui_Settings
class SettingsWidget(QWidget,Ui_Settings):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        global settings
        self.settings = settings
        self.settings.load()

        if not self.settings.validate():
            QMessageBox.warning(self, 'Error', f'Error loading settings. File not found.', QMessageBox.Ok)

        CHIP_PARTS = ["PIC16F627","PIC16F627A","PIC16F628","PIC16F628A"]
        for i in range(4):
            self.comboBox_chip.addItem(CHIP_PARTS[i])
        self.comboBox_chip.setCurrentIndex(CHIP_PARTS.index(self.settings.get("chip_part")))

        value = self.settings.get("testing_speed") * 100
        self.dial_changed(value)
        self.dial.setValue(value)
        self.dial.connect(self.dial, QtCore.SIGNAL("valueChanged(int)"), self.dial_changed)
        self.spinBox_arduino_id.setValue(self.settings.get(KEY_ARDUINO_INSTANCE_ID))
        self.lineEdit_port.setText(self.settings.get("serial_port"))
        self.lineEdit_serial.setText(self.settings.get("programmer_serial_number"))
        self.checkBox_test.setChecked(self.settings.get("auto_test"))
        self.checkBox_connect.setChecked(self.settings.get("auto_connect"))
        self.checkBox_debug.setChecked(self.settings.get("debug"))
        self.checkBox_logon.setChecked(self.settings.get("skip_login"))
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
        self.settings.save()
        self.close()


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
        removed = User.remove_user_s(selected_username)
        if removed:
            self.close()
        else:
            QMessageBox.warning(self, 'Error', f'Error removing user: {selected_username}', QMessageBox.Ok)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow(app)
    window.show()
    app.exec()


