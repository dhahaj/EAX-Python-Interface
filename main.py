from imports import *
from loguru import logger as log
import subprocess
import sys
import os
import atexit
import time
import qdarkstyle
from qdarkstyle import DarkPalette, LightPalette
from PySide6.QtGui import QCursor
os.environ["QT_API"] = "pyside6"
from qtpy import QtWidgets

Yes = QMessageBox.StandardButton.Yes
No = QMessageBox.StandardButton.No
Ok = QMessageBox.StandardButton.Ok

app_logger = AppLogger.get_logger()
settings = ApplicationSettings("settings.json")
db = UserDatabase("users.db")
logg = LogManager()

def debug(msg):
    if settings.get(KEY_DEBUG):
        log.debug(msg)
    app_logger.debug(msg)
    logg.log('DEBUG', msg)

def error(msg):
    log.error(msg)
    app_logger.error(msg)
    logg.log('ERROR', msg)

def log_info(msg):
    app_logger.info(msg)
    logg.log('INFO', msg)

def info(msg):
    log.info(msg)
    app_logger.info(msg)
    logg.log('INFO', msg)


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    This is the main application window. It contains the primary logic for controlling the application.

    :param QMainWindow: The main window.
    :type QMainWindow: QMainWindow
    :param Ui_MainWindow: The main window UI.
    :type Ui_MainWindow: Ui_MainWindow
    """

    device_changed = Signal(str)

    def __init__(self, app) -> None:
        super(MainWindow, self).__init__()
        self.help_dialog = None
        self.setupUi(self)
        self.app = app
        self.setWindowIcon(QtGui.QIcon(":/resources/icons/images/icons/code.ico"))
        # Settings
        self.settings = settings
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.closed.connect(self.on_settings_closed)
        # Restore the window geometry and state
        self.app_settings = QSettings("Detex Corp", "EAX Interface")
        self.restoreGeometry(self.app_settings.value("geometry", QByteArray()))
        self.restoreState(self.app_settings.value("windowState", QByteArray()))

        if self.app_settings.value(KEY_FULLSCREEN, type=bool):
            self.showFullScreen()
        else:
            self.showNormal()
        self.actionFullscreen.setChecked(
            self.app_settings.value(KEY_FULLSCREEN, type=bool)
        )
        self.actionFullscreen.triggered.connect(self.toggleFullScreen)

        # Process for updating the firmware
        self.update_process = QProcess(self)
        self.update_process.finished.connect(self.on_finished)
        self.update_process.errorOccurred.connect(self.on_error)
        self.update_process.readyReadStandardError.connect(self.read_standard_output)
        self.update_process.readyReadStandardOutput.connect(self.read_standard_output)
        self.update_process.setWorkingDirectory(os.getcwd())

        self.device_changed.connect(self.on_device_changed)

        # Quick Connection Menu
        self.connect_menu = ConnectMenu("", None)
        self.menuBar().addMenu(self.connect_menu)
        self.set_icon(self.connect_menu, 'usb2')
        self.connect_menu.menu_clicked.connect(self.connect_device)

        self.loginDialog = None

        # Inactivity timer
        self.inactivityTimer = QTimer()
        self.inactivityTimer.setSingleShot(True)
        self.inactivityTimer.timeout.connect(self.handle_inactivity_timeout)
        self.installEventFilter(self)
        for widget in QApplication.instance().allWidgets():
            widget.installEventFilter(self)

        # Setup the text area
        self.text_edit.setFont(
            QFont(
                self.settings.get(KEY_FONT_FAMILY),
                self.settings.get(KEY_FONT_SIZE),
            )
        )
        self.text_edit.setStyleSheet(
            f"color:{self.settings.get(KEY_FOREGROUND_COLOR)};background-color:{self.settings.get(KEY_BACKGROUND_COLOR)};"
        )

        # Connect the menu items
        self.actionExplore_Directory.triggered.connect(self.browse_directory)
        self.actionUpdate_Firmware.triggered.connect(self.update_firmware)
        self.actionConnect.triggered.connect(self.connect_device)
        self.actionAbout.triggered.connect(self.aboutQt)
        self.actionChip_Select.triggered.connect(self.get_chip_part)
        self.actionShow_Logs.triggered.connect(self.show_log)
        self.actionChange_font.triggered.connect(self.choose_font)
        self.actionManual_Control.triggered.connect(self.control_manually)
        self.actionModify_Settings.triggered.connect(self.modify_settings)
        self.actionAdd_User.triggered.connect(self.add_user)
        self.actionRemove_User.triggered.connect(self.remove_user)
        self.actionHelp.triggered.connect(self.show_help)
        self.actionStatisitics.triggered.connect(self.show_statistics)
        self.actionDark_Theme.triggered.connect(self.toggle_theme)

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
        self.actionLogout.triggered.connect(self.perform_login)
        self.program_button.clicked.connect(self.program)
        self.test_button.clicked.connect(self.execute_test)

        self.button_pressed = False
        self.blinker_running = False
        self.testing = False
        self.waiting = False
        self.blocked = False
        self.connecting = False
        self.firmware = None
        self.device_name = None
        self.log_view = None
        self.is_dark = False

        self.text_edit.cursorPositionChanged.connect(self.check_for_link)

        self.load_file_text()

        self.eax_device = Device()

        if not self.eax_device.verify_firmware():
            self.insert_text("Missing firmware!")
            log.error("Missing firmware!")
            app_logger.error("Missing firmware!")

        # USB device
        self.arduino = None

        self.set_icon(self.test_button, 'test-button')
        self.set_icon(self.program_button, 'prog-button')
        self.set_icon(self.actionStatisitics, 'bar-chart')
        for action in self.menuDevice.actions():
                self.set_icon(action, 'radio-off-button')
        self.set_icon(self.actionExit, 'logout2')
        self.set_icon(self.actionLogout, 'remove-user')
        self.set_icon(self.actionChange_font, 'size')

        style = ""
        if self.settings.get_bool(KEY_DARK_THEME):
            style = qdarkstyle.load_stylesheet(palette=DarkPalette)
            self.actionDark_Theme.setChecked(True)
        else:
            style = qdarkstyle.load_stylesheet(palette=LightPalette)
            self.actionDark_Theme.setChecked(False)
        self.setStyleSheet(style)

        # If auto login and auto connect are enabled, try to connect to the USB device
        if self.settings.get(KEY_AUTO_LOGIN):
            if self.settings.get(KEY_AUTO_CONNECT):
                QTimer.singleShot(2000, self.connect_device)

    def check_for_link(self) -> None:
        cursor = self.text_edit.textCursor()
        current_position = cursor.position()
        anchor = self.text_edit.anchorAt(self.text_edit.mapFromGlobal(QCursor.pos()))
        
        if anchor:
            print(current_position)
            # QDesktopServices.openUrl(QUrl(anchor))
            cursor.setPosition(current_position)  # reset the position to avoid cursor moving to the link start
            self.text_edit.setTextCursor(cursor)
            self.help_dialog = HelpDialog()
            self.help_dialog.show()

    def toggle_theme(self) -> None:
        print("Toggle theme")
        style = ""
        if self.app_settings.value(KEY_DARK_THEME) == "false":
            style = qdarkstyle.load_stylesheet(palette=DarkPalette)
            self.app_settings.setValue(KEY_DARK_THEME, True)
            self.actionDark_Theme.setChecked(True)
        else:
            style = qdarkstyle.load_stylesheet(palette=LightPalette)
            self.app_settings.setValue(KEY_DARK_THEME, False)
            self.actionDark_Theme.setChecked(False)
        self.set_icon(self.connect_menu, 'usb2')
        self.set_icon(self.test_button, 'test-button')
        self.set_icon(self.program_button, 'prog-button')

        name = self.eax_device.get_name()
        for action in self.menuDevice.actions():
            if action.text() == name:
                # action.setIcon(icon)
                self.set_icon(action, 'radio-on-button')
            else:
                self.set_icon(action, 'radio-off-button')
 
        self.setStyleSheet(style)
        self.settings_dialog.setStyleSheet(style)
        self.set_icon(self.actionExit, 'logout2')
        self.set_icon(self.actionExplore_Directory, 'folder')
        self.set_icon(self.actionUpdate_Firmware, 'ps')
        self.set_icon(self.actionConnect, 'plug')
        self.set_icon(self.actionAbout, 'information')
        self.set_icon(self.actionChip_Select, 'chip')
        self.set_icon(self.actionShow_Logs, 'files')
        self.set_icon(self.actionChange_font, 'size')
        self.set_icon(self.actionManual_Control, 'gear')
        self.set_icon(self.actionModify_Settings, 'settings')
        self.set_icon(self.actionAdd_User, 'follow')
        self.set_icon(self.actionRemove_User, 'remove-user')
        self.set_icon(self.actionHelp, 'help')
        self.set_icon(self.actionStatisitics, 'bar-chart')
        self.set_icon(self.actionLogout, 'logout')

    def set_icon(self, widget, icon_name):
        theme = self.get_current_theme()  # this function returns 'dark' or 'light'
        icon_path = f":/resources/icons/images/icons/{theme}/{icon_name}.png"
        icon = QIcon()
        icon.addFile(
            icon_path,
            QSize(),
            QIcon.Normal,
            QIcon.On,
        )
        widget.setIcon(icon)

    def get_current_theme(self) -> str:
        # if self.app_settings.value(KEY_DARK_THEME) == "false":
        if self.settings.get_bool(KEY_DARK_THEME):
            return "light"
        else:
            return "dark"

    def toggleFullScreen(self) -> bool:
        if self.app_settings.value(KEY_FULLSCREEN, defaultValue=False) == "false":
            self.showFullScreen()
            self.app_settings.setValue(KEY_FULLSCREEN, True)
            self.actionFullscreen.setChecked(True)
            return True
        else:
            self.showNormal()
            self.app_settings.setValue(KEY_FULLSCREEN, False)
            self.actionFullscreen.setChecked(False)
            return False

    def keyPressEvent(self, event) -> None:
        key = event.key()

        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_F11:
            self.toggleFullScreen()
        elif key == Qt.Key_F12:
            self.show_statistics()
        elif key == Qt.Key_F10:
            self.show_log()
        elif key == Qt.Key_F1:
            self.show_help()
        elif key == Qt.Key_F5:
            self.settings_dialog.show()
        elif key == Qt.Key_F6:
            self.toggle_theme()
        elif key == Qt.Key.Key_Question:
            self.aboutQt()
        elif key == Qt.Key_Q and event.modifiers() & Qt.ControlModifier:
            exit()
        elif key == Qt.Key_F2:
            screen = QtGui.QGuiApplication.primaryScreen()
            QtCore.QCoreApplication.processEvents()
            pixmap = screen.grabWindow(self.winId())
            img = pixmap.toImage()
            t = time.time()
            img.save(f"screenshot-{t}.png")
            QtCore.QCoreApplication.processEvents()
        elif key == Qt.Key_F3:
            self.control_manually()

    def on_device_changed(self, device) -> None:
        log.info(f"Device changed: {device}")
        self.device_label.setText(f"Device: {device}")
        self.eax_device.set_name(device)

        # Set the color of the device label
        if self.eax_device.get_name() == "EAX300":
            self.device_label.setStyleSheet(YELLOW)
        elif self.eax_device.get_name() == "EAX500":
            self.device_label.setStyleSheet(GREEN)
        else:
            self.device_label.setStyleSheet(ORANGE)

    def deviceSelect(self) -> None:
        # icon = QIcon()
        # icon.addFile(RADIO_OFF_ICON, QSize(), QIcon.Normal, QIcon.On)
        self.sender().setChecked(False)
        # Uncheck all other actions
        for action in self.menuDevice.actions():
            if action.text() != self.sender().text():
                # action.setIcon(icon)
                self.set_icon(action, 'radio-off-button')

        # Uncheck the device label if the same action is clicked
        if self.eax_device.get_name() == self.sender().text():
            self.device_label.setStyleSheet(DEVICE_LABEL)
            self.device_label.setText("")
            self.eax_device.set_name(None)
            # self.sender().setIcon(icon)
            self.set_icon(self.sender(), 'radio-off-button')
            return
        # icon.addFile(RADIO_ON_ICON, QSize(), QIcon.Normal, QIcon.On)
        # self.sender().setIcon(icon)
        self.set_icon(self.sender(), 'radio-on-button')
        self.device_changed.emit(self.sender().text())

    def show_help(self) -> None:
        try:
            self.help_dialog.show()
        except:
            self.help_dialog = HelpDialog()
            self.help_dialog.show()

    @staticmethod
    def browse_directory() -> None:
        subprocess.Popen(f"explorer {os.getcwd()}")

    def choose_font(self) -> None:
        old_font = self.text_edit.font()

        (ok, font) = QFontDialog.getFont(
            QFont(old_font.family(), old_font.pointSize()), self
        )

        if ok:
            debug(f"User selected font: {font.toString()}")
            self.text_edit.setFont(font)
            self.settings.set(KEY_FONT_FAMILY, QFontInfo(font).family())
            self.app_settings.setValue(KEY_FONT_FAMILY, QFontInfo(font).family())
            self.settings.set(KEY_FONT_SIZE, font.pointSize())
            self.app_settings.setValue(KEY_FONT_SIZE, font.pointSize())

    def get_chip_part(self) -> None:
        self.settings.load_settings()
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
            self.app_settings.setValue(KEY_CHIP_PART, item)
            log.debug(f"saved chip settings: {item}")

    def eventFilter(self, watched, event) -> bool:
        # Reset the inactivity timer if a mouse movement or key press event is detected
        if event.type() in (QEvent.MouseMove, QEvent.KeyPress):
            self.inactivityTimer.start(
                self.settings.get(KEY_LOGOFF_DELAY) * 60 * 1000
            )  # 60 seconds of inactivity before timeout
        return super(MainWindow, self).eventFilter(watched, event)

    def handle_inactivity_timeout(self) -> None:
        debug("Inactivity timeout.")

        if not self.settings.get(KEY_AUTO_LOGIN):
            self.perform_login()  # show the login dialog

        icon = QIcon()
        icon.addFile(RADIO_OFF_ICON, QSize(), QIcon.Normal, QIcon.On)
        # Uncheck all menu actions
        for action in self.menuDevice.actions():
            action.setIcon(icon)
        self.device_label.setText("")  # clear the device label
        self.eax_device.set_name(None)  # reset the device

    def input_callback(self, msg) -> None:
        pin = msg[0]
        value = msg[1]
        log.debug(f"Pin: {pin} Value: {value}")
        self.device_label.setText(f"Pin: {pin} Value: {value}")

    def add_user(self)  -> None:
        if self.settings.get(KEY_AUTO_LOGIN):
            if self.authenticate():
                self.add = UserAdditionDialog()
                self.add.show()
        else:
            self.add = UserAdditionDialog()
            self.add.show()

    def remove_user(self) -> None:
        if self.settings.get(KEY_AUTO_LOGIN):
            if self.authenticate():
                self.remove = UserRemovalDialog()
                self.remove.show()
        else:
            self.remove = UserRemovalDialog()
            self.remove.show()

    def insert_text(self, text) -> None:
        """Add text to the text console."""
        self.text_edit.append("\n" + text)
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.ensureCursorVisible()

    def load_file_text(self, filename="instructions.md") -> None:
        """Load text from a file and add it to the text area"""
        with open(filename, "r") as f:
            self.text_edit.setMarkdown(f.read() + "\n")
            self.text_edit.moveCursor(QtGui.QTextCursor.End)
            self.text_edit.ensureCursorVisible()
            return

    def aboutQt(self) -> None:
        QApplication.aboutQt()

    def connect_device(self) -> None:
        if self.connecting:
            return

        if self.arduino is None:
            self.arduino = USBDeviceHandler(
                device_connected_callback=self.notify_device_connected,
                wait=self.settings.get(KEY_ARDUINO_WAIT),
                shutdown_on_exception=self.settings.get(KEY_SHUTDOWN_ON_EXCEPTION),
                sleep_tune=self.settings.get(KEY_SLEEP_TUNE),
                debug=self.settings.get(KEY_DEBUG),
            )

        if not self.arduino.is_connected():
            self.connecting = True
            self.label_usb_icon.setText(ICON_USB_YELLOW)
            self.usb_label.setStyleSheet(YELLOW)
            self.usb_label.setText("Connecting...")
            self.arduino.connect(self.notify_device_connected)
            self.arduino.attach_callback(self.input_callback)

    def notify_device_connected(self, connected, message=None) -> None:
        """Callback for the USB device."""
        if connected:  # device is connected
            self.label_usb_icon.setText(ICON_USB_GREEN)
            self.usb_label.setStyleSheet(GREEN)
            self.usb_label.setText(f"USB: {self.arduino.serial_port.port}")
            self.actionConnect.setText("Disconnect")
            self.actionConnect.triggered.disconnect(
                self.connect_device
            )  # disconnect the connect action
            self.actionConnect.triggered.connect(
                self.disconnect_device
            )  # connect the disconnect action
            atexit.register(self.arduino.cleanup)

            # Save this port to the settings
            self.settings.set(KEY_COM_PORT, self.arduino.serial_port.port)
            self.app_settings.setValue(KEY_COM_PORT, self.arduino.serial_port.port)

            log_info(f"USB: connected to {self.arduino.serial_port.port}")
            log.success(f"USB: connected to {self.arduino.serial_port.port}")

        else:  # device is not connected
            error(f"USB: connection failed. Error: {message}")
            if message is not None and str.__contains__(
                message, "Incorrect Arduino ID"
            ):
                self.insert_text(f"Connection Failed. {message}")
            self.label_usb_icon.setText(ICON_USB_RED)
            self.connect_menu.setEnabled(True)
            self.actionConnect.setText("Connect")
            self.usb_label.setStyleSheet(RED)
            self.usb_label.setText("USB: connection failed")
            self.arduino = None

        # usb_device = self.device
        self.connecting = False

    def disconnect_device(self) -> None:
        # global usb_device
        if self.arduino is not None:
            atexit.unregister(self.arduino.cleanup)
            self.arduino.set_all_pins_to_value(0)
            self.actionConnect.setText("Connect")
            self.connect_menu.setEnabled(True)
            self.actionConnect.triggered.connect(self.connect_device)
            self.actionConnect.triggered.disconnect(self.disconnect_device)
            self.label_usb_icon.setText(ICON_USB_RED)
            self.usb_label.setStyleSheet(RED)
            self.usb_label.setText("USB: disconnected")
            debug("USB: disconnected.")
            self.arduino.cleanup()
            self.arduino = None

            # usb_device = None

    def control_manually(self) -> None:
        self.manual = ManualWidget(self.arduino)
        self.manual.show()

    def execute_test(self) -> None:
        """Start testing the device."""
        if self.testing:
            self.button_pressed = True
        elif not self.blocked:
            if not self.eax_device.is_selected():
                QMessageBox.warning(self, "Error", f"Please select a device.", Ok)
                return
            if self.arduino is None:
                QMessageBox.warning(self, "Error", f"USB device not connected.", Ok)
                return
            elif not self.arduino.is_connected():
                QMessageBox.warning(self, "Error", f"USB device not connected.", Ok)
                return

            self.blinker_running = False
            info(f"Testing started for {self.eax_device.selected_device}")

            self.queue = []

            speed = int(self.settings.get(KEY_TESTING_SPEED))

            self.text_edit.setMarkdown(
                f"# Starting test for {self.eax_device.selected_device}... "
            )

            self.queue.append((1, self.arduino.test_indicator_on))

            self.queue.append(
                (
                    1,
                    self.insert_text,
                    "\n • Battery power on → Siren chirps and both LEDs flash  \n",
                )
            )

            self.queue.append((1, self.arduino.battery_on))

            self.queue.append(
                (
                    speed,
                    self.insert_text,
                    "\n • Starting low battery test → LEDs flash alternating \n",
                )
            )

            self.queue.append((1, self.arduino.low_battery_on))

            self.queue.append(
                (
                    speed,
                    self.insert_text,
                    "\n • Low battery test off → LEDs turn off.\n",
                )
            )

            self.queue.append((1, self.arduino.low_battery_off))

            self.queue.append(
                (
                    500,
                    self.insert_text,
                    (
                        " • Perform the following:\n"
                        " \t1. Press the key switch → The siren sounds\n"
                        " \t2. Press the cylinder switch → The LEDs turn on\n"
                    ),
                )
            )

            self.queue.append(
                (
                    200,
                    self.insert_text,
                    "\n\nPress the Continue button to finish testing...",
                )
            )

            self.queue.append((1, self.wait_for_button))

            self.queue.append((1, self.arduino.battery_off))

            self.queue.append((10, self.load_file_text, "instructions.md"))

            self.queue.append((1, self.arduino.test_indicator_off))

            self.testing = True
            self.blocked = True
            # Start processing the queue
            self.process_queue()

        else:
            self.insert_text("Cannot run test.")

    def process_queue(self) -> None: 
        """Process the programming queue."""
        if self.waiting:
            return
        if self.queue:
            delay, task, *args = self.queue.pop(0)  # Get the next task
            QTimer.singleShot(
                delay, lambda: self.perform_task(task, args)
            )  # Execute the task after the delay
        else:
            self.blocked = False
            self.testing = False

    def modify_settings(self) -> None:
        # if auto login is enabled, force the user to login
        if self.settings.get(KEY_AUTO_LOGIN):
            if self.authenticate():
                self.settings_dialog.show()
        else:
            self.settings_dialog.show()

    def authenticate(self) ->  bool:
        """Authenticate via the login dialog."""
        self.loginDialog = LoginDialog(self.settings.get(KEY_LAST_USER))
        if self.loginDialog.exec() == QDialog.Accepted:
            success, username = self.loginDialog.ok()
            if success:
                self.settings.set(KEY_LAST_USER, username)
                self.app_settings.setValue(KEY_LAST_USER, username)
            else:
                QMessageBox.critical(
                    self.loginDialog,
                    "Invalid credentials",
                    "The username or password you entered is incorrect. Please try again.",
                )
            return success
        else:
            return False

    def on_settings_closed(self, result) -> None:
        # global settings
        self.settings = settings
        log.info(f"Settings dialog closed. Result: {result}")
        self.text_edit.setStyleSheet(
            f"color: {self.settings.get(KEY_FOREGROUND_COLOR)}; background-color:"
            f" {self.settings.get(KEY_BACKGROUND_COLOR)};"
        )
        if self.settings.get(KEY_AUTO_LOGIN):
            self.actionLogout.setEnabled(False)
        else:
            self.actionLogout.setEnabled(True)
        if self.settings.get(KEY_FULLSCREEN):
            self.showFullScreen()
        else:
            self.showNormal()

    def wait_for_button(self) -> None:
        """Waiting for the test button to be pressed."""
        self.waiting = True
        # icon = QIcon()
        if not self.button_pressed:
            # QTimer.singleShot(100, self.wait_for_button)
            # size = QSize(h=55, w=55)
            # icon.addFile(
            #     ":/resources/icons/images/icons/forward-button.png",
            #     size,
            #     QIcon.Normal,
            #     QIcon.On,
            # )
            # self.test_button.setIcon(icon)
            self.set_icon(self.test_button, 'forward-button')
        else:
            self.set_icon(self.test_button, 'test-button')
            self.button_pressed = False
            self.waiting = False
            self.process_queue()

    def perform_task(self, task, args) -> None:
        """
        Execute a task.

        :param task: The task to execute.
        :param args: The arguments to pass to the task.
        """
        task(*args)
        self.process_queue()  # Continue processing the queue

    def program(self) -> None:
        """Program the device."""
        if not self.blocked and self.eax_device.is_selected():
            # Check if the firmware file exists
            if not os.path.exists(self.eax_device.get_firmware()):
                self.insert_text(f"{self.eax_device.get_firmware()} not found!")
                return

            self.settings.load_settings()  # reload the settings
            chip = self.settings.get("chip_part")
            serial = self.settings.get("programmer_serial_number")

            command = [
                "C:\\Program Files (x86)\\ASIX\\UP\\up.exe",
                f"/part {chip}",
                f"/s {serial}",
                f"/p {self.eax_device.get_firmware()}",
                "/q1",
            ]

            self.blocked = True

            info(f"Programming {self.eax_device.selected_device}, args: {command}")
            self.runner = CommandRunner(command)
            self.runner.resultReady.connect(
                self.process_result
            )  # Connect the signal to the handler
            self.runner.start()

    def process_result(self, returncode) -> None:
        # This function gets called when the command finishes.
        # Do whatever you need to do with the return code here.
        if returncode == 0:
            self.insert_text("Programming successful.")
            info(f"Programming {self.eax_device.selected_device} successful")
            log.success(f"Programming {self.eax_device.selected_device} successful")
            if self.settings.get(KEY_AUTO_TEST):
                self.execute_test()
            return
        elif returncode == 2:
            self.insert_text(
                f" \n Programming {self.eax_device.selected_device} failed. Error code: {returncode} (Check Programmer Serial Number?)"
            )
        elif returncode == 7:
            self.insert_text(
                f"## Programming {self.eax_device.selected_device} failed. Error code: {returncode} (Check chip part number)"
            )
        error(f"Programming {self.eax_device.selected_device} failed. Error code: {returncode}")
        log.error(
            f"Programming {self.eax_device.selected_device} failed. Error code: {returncode}"
        )
        app_logger.error(
            f"Programming {self.eax_device.selected_device} failed. Error code: {returncode}"
        )
        self.blocked = False

    def show_statistics(self) -> None:
        (fail, success) = logg.count_programming_errors(), logg.count_programming_successes()
        QMessageBox().information(
            self,
            "Programming Statistics",
            f"Successful: {success} \nFailed: {fail}",
        )

    def show_log(self) -> None:
        """Display the log view window."""
        # logs = AppLogger.get_table()
        logs = logg.get_all_logs()
        print(logs[0])
        self.log_view = LogView(logs,4,3)
        self.log_view.show()

    def perform_login(self) -> None:
        """Show the login dialog."""
        success, username = False, None
        # Block until the user is logged in
        while not success and self.window().isVisible():
            self.loginDialog = LoginDialog(self.settings.get(KEY_LAST_USER))
            if self.loginDialog.exec() == QDialog.Accepted:
                success, username = self.loginDialog.ok()
                if not success:
                    QMessageBox.critical(
                        self.loginDialog,
                        "Invalid credentials",
                        "The username or password you entered is incorrect. Please try again.",
                    )
            else:
                self.close()
        if success:
            if settings.get(KEY_AUTO_CONNECT):
                # Auto Connect
                QTimer.singleShot(1000, self.connect_device)
            log.success(f"Logged in as: {username}")
            app_logger.info(f"Logged in as: {username}")

            # Block if the user is not an admin
            self.actionModify_Settings.setEnabled(db.is_admin(username))
            self.actionAdd_User.setEnabled(db.is_admin(username))
            self.actionRemove_User.setEnabled(db.is_admin(username))
            self.actionUpdate_Firmware.setEnabled(db.is_admin(username))
            # save the last user to the settings
            self.settings.set(KEY_LAST_USER, username)
            self.app_settings.setValue(KEY_LAST_USER, username)
        else:
            sys.exit(0)

    def closeEvent(self, event) -> None:
        log.debug(event.isAccepted())
        reply = QMessageBox.question(
            self,
            "Window Close",
            "Are you sure you want to close the window?",
            Yes | No,
            Yes,
        )

        if reply == Yes:
            log.info("Application closed.")
            app_logger.info("Application closed.")
            self.app_settings.setValue("geometry", self.saveGeometry())
            self.app_settings.setValue("windowState", self.saveState())
            # self.app_settings.setValue(KEY_DARK_THEME, self.actionDark_Theme.isChecked())
            self.app_settings.setValue("full_screen", self.isFullScreen())
            event.accept()
        else:
            event.ignore()

    def show(self) -> None:
        
        super().show()
        if not self.settings.get(KEY_AUTO_LOGIN):
            self.perform_login()
        else:
            self.actionLogout.setEnabled(False)

    def update_firmware(self) -> None:
        """Update the firmware on the test fixture."""

        if self.settings.get(KEY_AUTO_LOGIN):
            if not self.authenticate():
                return

        self.device_label.setText("Firmware Update...")
        info("Updating firmware...")
        self.disconnected = False
        if self.arduino is not None:
            self.disconnected = True
            self.disconnect_device()
        id = str(self.settings.get(KEY_ARDUINO_INSTANCE_ID))
        port = self.settings.get(KEY_COM_PORT)

        # Define the PowerShell script path
        script_path = ".\\Scripts\\UpdateFirmware.PS1"
        self.update_process.setWorkingDirectory(os.getcwd())
        self.text_edit.setMarkdown(f"# Updating firmware... \n\n")

        # Define the command to execute
        self.update_process.start(
            "powershell.exe",
            ["-ExecutionPolicy", "ByPass", "-File", script_path, id, port],
        )

    def on_error(self, error) -> None:
        log.error("An error occurred: ", error)
        log.error("System reported: ", self.update_process.errorString())
        app_logger.error("Firmware update failed: ", error)

    def read_standard_output(self) -> None:
        output = self.update_process.readAllStandardOutput().data().decode()
        self.insert_text(output)
        log.info(output)
        msg = self.update_process.readAllStandardError().data().decode()
        if msg != "":
            self.insert_text(msg)
            log.error(msg)

    def on_finished(self) -> None:
        log.success("The process has finished")
        app_logger.info("Firmware update complete.")
        if self.eax_device.selected_device is not None:
            self.device_label.setText(f"Device: {self.eax_device.selected_device}")
        else:
            self.device_label.setText("Firmware Update Complete.")
        if self.disconnected:
            self.connect_device()
        self.update_process.terminate()
        if not self.update_process.waitForFinished(3000):
            self.update_process.kill()
            log.error("Process did not terminate in time.")


class ManualWidget(QWidget, Ui_ManualControlDialog):
    """
    Manual control dialog. This dialog allows the user to manually control the
    pins of the USB device.

    :param usb_handler: The USB connection handler.
    """

    def __init__(self, usb_handler=None):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.usb_device = usb_handler
        self.usb_device.attach_callback(self.callback)

        if self.usb_device is None or not self.usb_device.is_connected():
            QMessageBox.warning(self, "Error", f"USB device not connected.", Ok)
            self.close()
            return
        self.battery_button.clicked.connect(self.toggle_battery)
        self.low_battery_button.clicked.connect(self.toggle_low_battery)
        self.test_indicator_button.clicked.connect(self.toggle_testing_indicator)
        self.indicator_button.clicked.connect(self.toggle_indicator)

    def callback(self, msg):
        pin = msg[0]
        value = msg[1]
        log.debug(f"Pin: {pin} Value: {value}")
        self.label.setText(f"Pin: {pin} Value: {value}")

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
        self.usb_device.write_pin_by_func("test indicator", value)

    def toggle_indicator(self, checked):
        if checked:
            value = 1
        else:
            value = 0
        self.usb_device.write_pin_by_func("indicator", value)

    def closeEvent(self, event):
        if self.usb_device is not None:
            if self.usb_device.is_connected():
                self.usb_device.set_all_pins_to_value(0)
                self.usb_device.write_pin_by_func("indicator", 1)
        event.accept()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_F2:
            screen = QtGui.QGuiApplication.primaryScreen()
            QtCore.QCoreApplication.processEvents()
            pixmap = screen.grabWindow(self.winId())
            img = pixmap.toImage()
            t = time.time()
            img.save(f"screenshot-{t}.png")
            QtCore.QCoreApplication.processEvents()


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

    closed = QtCore.Signal(ApplicationSettings)

    def __init__(self, parent):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.app_settings = QSettings("Detex Corp", "EAX Interface")
        self.settings = settings
        self.settings.load_settings()
        if not self.settings.validate_settings():
            QMessageBox.warning(
                self,
                "Error",
                f"Error loading settings. File not found.",
                Ok,
            )
            self.close()
            return

        self.commandLinkButton_select_color.clicked.connect(self.pick_color)
        self.commandLinkButton_bg_color.clicked.connect(self.pick_background_color)

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_default.clicked.connect(self.reset_to_default)

        lcd = self.lcdNumber
        self.apply_changes()
        style = ""
        if self.app_settings.value(KEY_DARK_THEME, False):
            style = qdarkstyle.load_stylesheet(palette=DarkPalette)
        else:
            style = qdarkstyle.load_stylesheet(palette=LightPalette)
        self.setStyleSheet(style)

    def apply_changes(self) -> None:
        # self.lineEdit_serial.setText(self.settings.get(KEY_PROGRAMMER_SERIAL_NUMBER))
        self.lineEdit_serial.setText(
            self.app_settings.value(KEY_PROGRAMMER_SERIAL_NUMBER)
        )
        for chip_part in CHIP_PARTS:
            self.comboBox_chip.addItem(chip_part)
        self.comboBox_chip.setCurrentText(
            self.app_settings.value(KEY_CHIP_PART, CHIP_PARTS[3])
        )
        value = self.app_settings.value(KEY_TESTING_SPEED, 2200)
        self.dial.setValue(int(value))

        self.comboBox_com_port.setCurrentText(
            self.app_settings.value(KEY_COM_PORT, "COM1")
        )
        for port in USBDeviceHandler.get_usb_ports():
            self.comboBox_com_port.addItem(port)

        # self.spinBox_autologoff_delay.setValue(self.settings.get(KEY_LOGOFF_DELAY))
        self.spinBox_autologoff_delay.setValue(
            self.app_settings.value(KEY_LOGOFF_DELAY, 15)
        )

        # self.spinBox_arduino_id.setValue(self.settings.get(KEY_ARDUINO_INSTANCE_ID))
        self.spinBox_arduino_id.setValue(
            self.app_settings.value(KEY_ARDUINO_INSTANCE_ID, 1)
        )

        # self.checkBox_test.setChecked(self.settings.get(KEY_AUTO_TEST))
        self.checkBox_test.setChecked(
            str_to_bool(self.app_settings.value(KEY_AUTO_TEST, True))
        )

        # self.checkBox_connect.setChecked(self.settings.get(KEY_AUTO_CONNECT))
        self.checkBox_connect.setChecked(
            str_to_bool(self.app_settings.value(KEY_AUTO_CONNECT, True))
        )

        # self.checkBox_debug.setChecked(self.settings.get(KEY_DEBUG))
        self.checkBox_debug.setChecked(str_to_bool(self.app_settings.value(KEY_DEBUG, True)))

        # self.checkBox_logon.setChecked(self.settings.get(KEY_AUTO_LOGIN))
        self.checkBox_logon.setChecked(
            str_to_bool(self.app_settings.value(KEY_AUTO_LOGIN, True))
        )

        # self.checkBox_auto_find.setChecked(self.settings.get(KEY_AUTO_FIND))
        self.checkBox_auto_find.setChecked(
            str_to_bool(self.app_settings.value(KEY_AUTO_FIND, True))
        )

        self.checkBox_shutdown_on_exception.setChecked(
            # self.settings.get(KEY_SHUTDOWN_ON_EXCEPTION)
            str_to_bool(self.app_settings.value(KEY_SHUTDOWN_ON_EXCEPTION, True))
        )

        # self.lineEdit_serial_sleep_tune.setText(str(self.settings.get(KEY_SLEEP_TUNE)))
        self.lineEdit_serial_sleep_tune.setText(
            str(self.app_settings.value(KEY_SLEEP_TUNE, 1.0))
        )

        # self.spinBox_wait_time.setValue(self.settings.get(KEY_ARDUINO_WAIT))
        self.spinBox_wait_time.setValue(self.app_settings.value(KEY_ARDUINO_WAIT, 1))

        # self.checkBox_fullscreen.setChecked(self.settings.get(KEY_FULLSCREEN))
        self.checkBox_fullscreen.setChecked(
            str_to_bool(self.app_settings.value(KEY_FULLSCREEN, False))
        )

    def reset_to_default(self) -> None:
        defaults = [DEFAULT_SETTINGS[key] for key in DEFAULT_SETTINGS.keys()]
        self.comboBox_com_port.setCurrentIndex(0)
        self.lineEdit_serial.setText(defaults[1])
        self.comboBox_chip.setCurrentIndex(CHIP_PARTS.index(defaults[2]))
        self.dial.setValue(int(defaults[4]))
        self.checkBox_test.setChecked(defaults[5])
        self.checkBox_logon.setChecked(defaults[9])
        self.checkBox_connect.setChecked(defaults[10])
        self.spinBox_arduino_id.setValue(defaults[11])
        self.checkBox_debug.setChecked(defaults[12])
        self.spinBox_autologoff_delay.setValue(defaults[14])
        self.spinBox_wait_time.setValue(defaults[17])
        self.checkBox_shutdown_on_exception.setChecked(defaults[18])
        self.checkBox_auto_find.setChecked(defaults[19])
        self.lineEdit_serial_sleep_tune.setText(str(defaults[20]))
        self.checkBox_fullscreen.setChecked(defaults[21])

    def save_changes(self) -> None:
        self.app_settings.setValue(KEY_COM_PORT, self.comboBox_com_port.currentText())
        self.app_settings.setValue(KEY_CHIP_PART, self.comboBox_chip.currentText())
        self.app_settings.setValue(
            KEY_PROGRAMMER_SERIAL_NUMBER, self.lineEdit_serial.text()
        )
        self.app_settings.setValue(KEY_AUTO_TEST, self.checkBox_test.isChecked())
        self.app_settings.setValue(KEY_AUTO_CONNECT, self.checkBox_connect.isChecked())
        self.app_settings.setValue(KEY_DEBUG, self.checkBox_debug.isChecked())
        self.app_settings.setValue(KEY_AUTO_LOGIN, self.checkBox_logon.isChecked())
        self.app_settings.setValue(
            KEY_ARDUINO_INSTANCE_ID, self.spinBox_arduino_id.value()
        )
        self.app_settings.setValue(KEY_TESTING_SPEED, self.dial.value())
        self.app_settings.setValue(
            KEY_LOGOFF_DELAY, self.spinBox_autologoff_delay.value()
        )
        self.app_settings.setValue(KEY_AUTO_FIND, self.checkBox_auto_find.isChecked())
        self.app_settings.setValue(
            KEY_SHUTDOWN_ON_EXCEPTION, self.checkBox_shutdown_on_exception.isChecked()
        )
        self.app_settings.setValue(
            KEY_SLEEP_TUNE, float(self.lineEdit_serial_sleep_tune.text())
        )
        self.app_settings.setValue(KEY_ARDUINO_WAIT, self.spinBox_wait_time.value())
        self.app_settings.setValue(KEY_FULLSCREEN, self.checkBox_fullscreen.isChecked())
        # self.settings.save_settings()
        self.close()
        return

        self.settings.set(KEY_SLEEP_TUNE, float(self.lineEdit_serial_sleep_tune.text()))
        self.settings.set(KEY_ARDUINO_WAIT, self.spinBox_wait_time.value())
        self.settings.set(KEY_FULLSCREEN, self.checkBox_fullscreen.isChecked())

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
        self.settings.set(KEY_FULLSCREEN, self.checkBox_fullscreen.isChecked())
        self.settings.save_settings()
        self.close()

    def pick_color(self) -> None:
        old_color = QColor(self.settings.get(KEY_FOREGROUND_COLOR))
        color = QColorDialog.getColor(old_color, self)
        if color.isValid():
            log.debug(f"User selected color: {color.name()}")
            self.settings.set(KEY_FOREGROUND_COLOR, f"{color.name()}")
            self.app_settings.setValue(KEY_FOREGROUND_COLOR, f"{color.name()}")

    def pick_background_color(self):
        old_color = QColor(self.settings.get(KEY_BACKGROUND_COLOR))
        color = QColorDialog.getColor(old_color, self)
        if color.isValid():
            log.debug(f"User selected color: {color.name()}")
            self.settings.set(KEY_BACKGROUND_COLOR, f"{color.name()}")
            self.app_settings.setValue(KEY_BACKGROUND_COLOR, f"{color.name()}")

    def closeEvent(self, event) -> None:
        self.settings.load_settings()
        self.closed.emit((0, self.settings))
        event.accept()

    def keyPressEvent(self, event) -> None:
        key = event.key()

        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_F2:
            screen = QtGui.QGuiApplication.primaryScreen()
            QtCore.QCoreApplication.processEvents()
            pixmap = screen.grabWindow(self.winId())
            img = pixmap.toImage()
            t = time.time()
            img.save(f"screenshot-{t}.png")
            QtCore.QCoreApplication.processEvents()


class UserAdditionDialog(QDialog, Ui_AddUserDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

        self.users = db.get_users()

    def save(self):
        log.debug(self.lineEdit_username.text())
        log.debug(self.lineEdit_password.text())
        admin = self.checkBox.isChecked()
        db.insert_user(
            self.lineEdit_username.text(), self.lineEdit_password.text(), admin
        )
        self.close()


class UserRemovalDialog(QDialog, Ui_RemoveUserDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.us = db.get_users()
        for username in self.us:
            self.comboBox.addItem(username)

        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

    def save(self):
        selected_username = self.comboBox.currentText()
        if selected_username == "dmh":
            QMessageBox.critical(
                self,
                "Error",
                f"Cannot remove user: {selected_username}",
                Ok,
            )
            self.close()
            return
        db.remove_user(selected_username)


class LoginDialog(QDialog, Ui_LoginDialog):
    """
    Login dialog. This dialog allows the user to login to the application.

    :param last_user: The last user that logged in.
    """

    def __init__(self, last_user=None):
        super().__init__()
        self.setupUi(self)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        self.app_settings = QSettings("Detex Corp", "Login Dialog")
        self.restoreGeometry(self.app_settings.value("geometry", QByteArray()))

        for username in db.get_users():
            self.comboBox.addItem(username)
        self.comboBox.setCurrentText(last_user)

        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)

        self.app_settings = QSettings("Detex Corp", "Login Dialog")
        self.restoreGeometry(self.app_settings.value("geometry", QByteArray()))

    def ok(self) -> tuple:
        self.app_settings.setValue("geometry", self.saveGeometry())
        selected_username = self.comboBox.currentText()
        selected_password = self.lineEdit_password.text()
        validate = db.check_password(selected_username, selected_password)
        return (validate, selected_username)

    def cancel(self) -> None:
        return (False, None)

    def keyPressEvent(self, event) -> None: 
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_F2:
            screen = QtGui.QGuiApplication.primaryScreen()
            QtCore.QCoreApplication.processEvents()
            pixmap = screen.grabWindow(self.winId())
            img = pixmap.toImage()
            t = time.time()
            img.save(f"screenshot-{t}.png")
            QtCore.QCoreApplication.processEvents()


class LogView(QWidget, Ui_LogView):
    """
    The LogView class represents a widget that displays logs in tabular format.

    :param data: The log data to be displayed, expected as a list of lists where each sub-list represents a log entry.
    :param *args: Optional additional arguments.
    """

    def __init__(self, data, *args):
        super().__init__()
        self.setupUi(self)
        self.tableWidget.setSortingEnabled(True)
        self.data = data
        self.tableWidget.setRowCount(len(self.data))
        self.setData()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.app_settings = QSettings("Detex Corp", "Log View")
        self.restoreGeometry(self.app_settings.value("geometry", QByteArray()))

    def setData(self) -> None:
        with log.catch(
            message="Encountered exception from main.",
            reraise=True,
            exception=BaseException,
        ):
            horHeaders = ["timestamp", "level", "message"]
            self.tableWidget.setHorizontalHeaderLabels(horHeaders)
            print(f"data: {type(self.data[0])}")
            for i in range(len(self.data)):
                timestamp = QTableWidgetItem(self.data[i].get("timestamp"))
                level = QTableWidgetItem(self.data[i].get("level"))
                message = QTableWidgetItem(self.data[i].get("message"))
                
                # print(f"Item: {item}")
                self.tableWidget.setItem(i, 0, timestamp)
                self.tableWidget.setItem(i, 1, level)
                self.tableWidget.setItem(i, 2, message)

                # for j in range(len(self.data[i])):
                #     # print(f"Setting column: {j}")
                #     try:
                #         newitem = QTableWidgetItem(self.data[i][j])
                #         # print(f"Setting item: {i},{j} {self.data[i][j]}")
                #         self.tableWidget.setItem(i, j, newitem)
                #     except Exception as e:
                #         # print(e)
                #         pass

    def closeEvent(self, event) -> None:
        self.app_settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def keyPressEvent(self, event) -> None:
        key = event.key()

        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_F2:
            screen = QtGui.QGuiApplication.primaryScreen()
            QtCore.QCoreApplication.processEvents()
            pixmap = screen.grabWindow(self.winId())
            img = pixmap.toImage()
            t = time.time()
            img.save(f"screenshot-{t}.png")
            QtCore.QCoreApplication.processEvents()


class HelpDialog(QDialog, Ui_HelpDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.app_settings = QSettings("Detex Corp", "Help Dialog")
        self.restoreGeometry(self.app_settings.value("geometry", QByteArray()))
        # self.toolBox.currentChanged.connect(self.on_tab_clicked)
        self.label.installEventFilter(self)
        self.label_2.installEventFilter(self)
        self.label_3.installEventFilter(self)
        parent_settings = QSettings("Detex Corp", "EAX Interface")
        if parent_settings.value(KEY_DARK_THEME) == "false":
            self.setStyleSheet(qdarkstyle.load_stylesheet(palette=LightPalette))
            print("Light mode")
        else:
            self.setStyleSheet(qdarkstyle.load_stylesheet(palette=DarkPalette))
            print("Dark mode")

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            if obj == self.label:
                obj.setMovie(QMovie("firmware_update.gif"))
            elif obj == self.label_2:
                obj.setMovie(QMovie("testing.gif"))
            elif obj == self.label_3:
                obj.setMovie(QMovie("setting.gif"))
            print("Left click")
            obj.movie().start()
            return True
        return super().eventFilter(obj, event)

    # def on_tab_clicked(self, index) -> None:
    #     print(f"Tab clicked: {index}")

    def closeEvent(self, event) -> None:
        self.app_settings.setValue("geometry", self.saveGeometry())
        self.deleteLater()
        event.accept()


class CommandRunner(QThread):
    resultReady = Signal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        print("Running command: ", self.command)
        print(" ".join(self.command))
        process = subprocess.run(self.command, shell=True)
        self.resultReady.emit(process.returncode)


class ConnectMenu(QMenu):
    """A custom QMenu that emits a signal when clicked."""

    menu_clicked = Signal()

    def showEvent(self, event):
        self.menu_clicked.emit()


class TelemetrixWorker(QObject):
    toggleStateChanged = Signal()  # Signal to notify about a state change

    def run(self):
        # Your code that interacts with Telemetrix, and waits for input
        # When a toggle state change occurs:
        self.toggleStateChanged.emit()


class SingleInstanceApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.semaphore = QSystemSemaphore("EAXInterfaceSemaphore", 1)
        self.semaphore.acquire()

        self.shared_memory = QSharedMemory("EAXInterface")
        self.shared_memory.attach()
        self.shared_memory.detach()
        self.is_running = False

        if not self.shared_memory.create(1):
            self.is_running = True
            return

        self.semaphore.release()


def str_to_bool(s) -> bool:
    if s is None:
        return False
    return s.lower().strip(' ') in ['true', 'yes', '1']


def check_requirements() -> tuple:
    missing = ""
    for file in FILES:
        if not os.path.exists(file):
            missing += file + "\n"
    if missing != "":
        log.critical(f"Missing files:\n{missing}")
        return (False, missing)
    return (True, None)


if __name__ == "__main__":
    with log.catch(
        message="Encountered exception from main.",
        reraise=True,
        exception=BaseException,
    ):
        (success, missing) = check_requirements()
        print("Starting app")
        if not success:
            QMessageBox.critical(None, "Error", f"Missing files:\n{missing}", Ok)
            sys.exit(1)
        print("Success")

        # import pdb; pdb.set_trace()
        # app = SingleInstanceApp([])
        app = QApplication()
        print ("Checking for running instances")
        # if app.is_running:
        #     log.critical("Another instance of the application is already running.")
        #     QMessageBox.critical(
        #         None,
        #         "Error",
        #         "Another instance of the application is already running.",
        #         Ok,
        #     )
        #     sys.exit(1)

        window = MainWindow(app)
        window.show()
        print("Starting application")
        info("Application started.")
        sys.exit(app.exec())
