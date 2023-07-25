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

import resource_rc #You need to manually import the compiled resource file

app_logger = AppLogger("logger").get_logger()
timer = QTimer()
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
        self.button_pressed = True
        self.blinker_running = False
        self.button_pressed = True
        self.testing = False
        self.waiting = False
        self.blocked = False
        self.firmware = None
        self.device_name = None
        self.load_text_from_file()

        self.settings = Settings("settings.json")

        global usb_device 
        usb_device = USBHandler(device_connected_callback=self.device_connected_callback)
        self.device = usb_device

    def _print(self):
        print(self.sender())#.text())
    def deviceSelect(self):
        for action in self.menuDevice.actions():
            if action.text() != self.sender().text():
                action.setChecked(False)
        print(self.sender().text())
        self.statusbar.showMessage(self.sender().text())
        self.device_label.setText("Device: " + self.sender().text())
        if (self.sender().text() == "EAX300") or (self.sender().text() == "EAX500"):
            self.device_label.setStyleSheet("color: rgb(0, 200, 0);")
        else:
            self.device_label.setStyleSheet("color: rgb(200, 0, 0);")

        self.device_name = self.sender().text()
        self.firmware = "firmware/" + self.device_name + "_591.hex"

    def quit(self):
        print("Quit")
        self.app.quit()

    def add_user(self):
        self.add_user_dialog = AddUserDialog()
        self.add_user_dialog.show()

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
        self.device.connect(self.device_connected_callback)

    def device_connected_callback(self, connected):
        self.usb_label.setText("USB: " + str(connected))
        if connected :
            self.usb_label.setStyleSheet("color: rgb(0, 200, 0);") 
        else:
            self.usb_label.setStyleSheet("color: rgb(200, 0, 0);")
            app_logger.error(f"USB connection failed.")
    
    def manual_control(self):
        self.manual = ManualWidget(self.device)
        self.manual.show()

    def run_command(self, command):
        """
        Run a command in a separate thread.

        :param command: The command to run.
        """
        self.settings.__load__()
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
        self.settings_widget = SettingsWidget(self.settings)
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
            self.settings.__load__()

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


from ui_Settings import Ui_Settings
class SettingsWidget(QWidget,Ui_Settings):
    def __init__(self,settings):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.settings = settings
        self.settings.__load__()

        CHIP_PARTS = ["PIC16F627","PIC16F627A","PIC16F628","PIC16F628A"]
        for i in range(4):
            self.comboBox_chip.addItem(CHIP_PARTS[i])
        self.comboBox_chip.setCurrentIndex(CHIP_PARTS.index(self.settings.get("chip_part")))

        value = self.settings.get("testing_speed") * 100
        self.dial_changed(value)
        self.dial.setValue(value)
        self.dial.connect(self.dial, QtCore.SIGNAL("valueChanged(int)"), self.dial_changed)
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
        self.settings.set("testing_speed",self.dial.value()/100)
        self.settings.__save__()
        self.close()


from PySide6.QtWidgets import QDialog
from ui_AddUserDialog import Ui_AddUserDialog
from user import (User, SingleUser)
class AddUserDialog(QDialog,Ui_AddUserDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

        self.users = User("users.json")

    def save(self):
        print(self.lineEdit_username.text())
        print(self.lineEdit_password.text())
        admin = self.checkBox.isChecked()
        User.add_user(self.lineEdit_username.text(),self.lineEdit_password.text(),admin)
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow(app)
    window.show()
    app.exec()



# from login import Login
# # from eax500 import MainWindow
# from settings import Settings
# from applogger import AppLogger
# from user import User
# from usbhandler import USBHandler


# if __name__ == "__main__":
#     """
#     The main function for the EAX500 application. It loads the settings, instantiates the system logger,
#     loads the users, and starts the login process. If the login is successful, or if the settings indicate
#     to skip the login, the main window is created and the main loop is started. The USB connection then attempts
#     to create a connection with the EAX500 fixture.
#     """
#     settings = Settings("settings.json")  # Create a settings object
#     settings.load()  # Load the settings from the settings.json file

#     app_logger = AppLogger("logger").get_logger()  # Create a logger object
#     app_logger.info(
#         "Starting the EAX500 application."
#     )  # Log the start of the application

#     users = User("users.json")  # Create a user object
#     users.load()  # Load the users from the users.json file

#     # if skip login is false, create a login window
#     if not settings.get("skip_login"):
#         login = Login()
#         while not login.is_logged_in():
#             login.run()
#         user = login.get_user()
#         app_logger.info(f"User {user['username']} logged in.")
#     else:
#         user = None

#     main_window = MainWindow()  # Create a main window object
#     main_window.window.mainloop()  # Start the main loop

#     # Create a USBHandler object
#     usb_handler = USBHandler(
#         arduino_instance_id=settings.get("arduino_instance_id"), # Provide the Arduino instance ID for this particular EAX500 fixture
#         device_connected_callback=main_window.device_connected_callback, # Set a callback function for the device
#     )
#     usb_handler.connect()  # Attempt to connect to the EAX500 fixture

#     app_logger.info("Closing the EAX500 application.")
#     # usb_handler = USBHandler()

