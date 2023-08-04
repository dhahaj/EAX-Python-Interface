from PySide6.QtWidgets import QMenu
from PySide6.QtCore import QThread, Signal
from ui_HelpDialog import Ui_HelpDialog
from ui_LogView import Ui_LogView
from PySide6.QtWidgets import QTableWidgetItem
from ui_LoginDialog import Ui_LoginDialog
from ui_RemoveUserDialog import Ui_RemoveUserDialog
from PySide6.QtWidgets import QLineEdit
from ui_AddUserDialog import Ui_AddUserDialog
from PySide6.QtWidgets import QDialog
from ui_Settings import Ui_Settings
from PySide6 import QtCore, QtGui
from PySide6.QtCore import (
    QTimer,
    QEvent,
    Qt,
    QSize,
    QProcess,
    Signal,
    QSettings,
    QSize,
    QByteArray,
    QSystemSemaphore,
    QSharedMemory,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QColorDialog,
    QWidget,
    QFontDialog,
    QInputDialog,
)
from PySide6.QtGui import (
    QFont,
    QFontInfo,
    QColor,
    QPalette,
    QIcon,
)
# from private import Private
from multiprocessing import Semaphore
from ui_ManualControlDialog import Ui_ManualControlDialog
from ui_MainWindow import Ui_MainWindow
import atexit
import os
import sys
import subprocess
from loguru import logger as lgr
from constants import *
from applogger import AppLogger, Log
from usbhandler import USBDeviceHandler
from settings import ApplicationSettings
from userdatabase import UserDatabase
from device import Device

from command_runner import command_runner as cr
app_logger = AppLogger('logger').get_logger()
settings = ApplicationSettings('settings.json')
db = UserDatabase('users.db')


class MainWindow(QMainWindow, Ui_MainWindow):
    '''
    This is the main application window. It contains the primary logic for controlling the application.

    :param QMainWindow: The main window.
    :type QMainWindow: QMainWindow
    :param Ui_MainWindow: The main window UI.
    :type Ui_MainWindow: Ui_MainWindow
    '''
    device_changed = Signal(str)

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app

        # Settings
        self.settings = settings
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.closed.connect(self.on_settings_closed)

        # Restore the window geometry and state
        self.app_settings = QSettings('Detex Corp', 'EAX Interface')
        self.restoreGeometry(self.app_settings.value('geometry', QByteArray()))
        self.restoreState(self.app_settings.value('windowState', QByteArray()))

        if self.settings.get(KEY_FULLSCREEN):
            self.showFullScreen()

        # Process for updating the firmware
        self.update_process = QProcess(self)
        self.update_process.finished.connect(self.on_finished)
        self.update_process.errorOccurred.connect(self.on_error)
        self.update_process.readyReadStandardError.connect(
            self.read_standard_output
        )
        self.update_process.readyReadStandardOutput.connect(
            self.read_standard_output
        )
        self.update_process.setWorkingDirectory(os.getcwd())

        self.device_changed.connect(self.on_device_changed)

        # Quick Connection Menu
        icon12 = QIcon()
        icon12.addFile(
            ':/resources/icons/images/icons/usb2.png', QSize(), QIcon.Normal, QIcon.On
        )
        self.connect_menu = ConnectMenu('', None)
        self.connect_menu.setIcon(icon12)
        self.connect_menu.menu_clicked.connect(self.connect_device)

        self.menuBar().addMenu(self.connect_menu)

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
            f'color:{self.settings.get(KEY_FOREGROUND_COLOR)};background-color:{self.settings.get(KEY_BACKGROUND_COLOR)};'
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

        self.load_file_text()

        # The device
        self.eax_device = Device()

        if not self.eax_device.verify_firmware():
            self.insert_text('Missing firmware!')
            lgr.error('Missing firmware!')
            app_logger.error('Missing firmware!')

        # USB device
        self.device = None

        # If auto login and auto connect are enabled, try to connect to the USB device
        if self.settings.get(KEY_AUTO_LOGIN):
            if self.settings.get(KEY_AUTO_CONNECT):
                QTimer.singleShot(2000, self.connect_device)

    def on_device_changed(self, device):
        lgr.info(f'Device changed: {device}')
        self.device_label.setText(f'Device: {device}')
        self.eax_device.set_name(device)

        # Set the color of the device label
        if self.eax_device.get_name() == 'EAX300':
            self.device_label.setStyleSheet(YELLOW)
        elif self.eax_device.get_name() == 'EAX500':
            self.device_label.setStyleSheet(GREEN)
        else:
            self.device_label.setStyleSheet(ORANGE)

    def deviceSelect(self):
        icon = QIcon()
        icon.addFile(RADIO_OFF_ICON, QSize(), QIcon.Normal, QIcon.On)
        self.sender().setChecked(False)
        # Uncheck all other actions
        for action in self.menuDevice.actions():
            if action.text() != self.sender().text():
                action.setIcon(icon)

        # Uncheck the device label if the same action is clicked
        if self.eax_device.get_name() == self.sender().text():
            self.device_label.setStyleSheet(DEVICE_LABEL)
            self.device_label.setText('')
            self.eax_device.set_name(None)
            self.sender().setIcon(icon)
            return
        icon.addFile(RADIO_ON_ICON, QSize(), QIcon.Normal, QIcon.On)
        self.sender().setIcon(icon)
        self.device_changed.emit(self.sender().text())

    def show_help(self):
        self.help_dialog = HelpDialog()
        self.help_dialog.show()

    def browse_directory(self):
        subprocess.Popen(f'explorer {os.getcwd()}')

    def choose_font(self):
        old_font = self.text_edit.font()

        (ok, font) = QFontDialog.getFont(
            QFont(old_font.family(), old_font.pointSize()), self
        )

        if ok:
            if self.settings.get(KEY_DEBUG):
                lgr.debug(f'User selected font: {font.toString()}')
            self.text_edit.setFont(font)
            self.settings.set(KEY_FONT_FAMILY, QFontInfo(font).family())
            self.settings.set(KEY_FONT_SIZE, font.pointSize())

    def get_chip_part(self):
        self.settings.load_settings()
        current_chip = self.settings.get(KEY_CHIP_PART)
        current_selection = CHIP_PARTS.index(current_chip)
        item, okPressed = QInputDialog.getItem(
            self, 'Get item', 'Chip Select:', CHIP_PARTS, current_selection, False
        )
        if okPressed and item:
            self.settings_dialog.comboBox_chip.setCurrentText(
                item
            )  # update the combo box
            self.settings.set(KEY_CHIP_PART, item)
            lgr.debug('saved ' ' + item + ' ' to settings.')

    def eventFilter(self, watched, event):
        # Reset the inactivity timer if a mouse movement or key press event is detected
        if event.type() in (QEvent.MouseMove, QEvent.KeyPress):
            self.inactivityTimer.start(
                self.settings.get(KEY_LOGOFF_DELAY) * 60 * 1000
            )  # 60 seconds of inactivity before timeout
        return super(MainWindow, self).eventFilter(watched, event)

    def handle_inactivity_timeout(self):
        if self.settings.get(KEY_DEBUG):
            app_logger.debug('Inactivity timeout.')
            lgr.debug('Inactivity timeout.')

        if not self.settings.get(KEY_AUTO_LOGIN):
            self.perform_login()  # show the login dialog
        
        icon = QIcon()
        icon.addFile(RADIO_OFF_ICON, QSize(), QIcon.Normal, QIcon.On)
        # Uncheck all menu actions
        for action in self.menuDevice.actions():
            action.setIcon(icon)
        self.device_label.setText('') # clear the device label
        self.eax_device.set_name(None)  # reset the device


    def add_user(self):
        if self.settings.get(KEY_AUTO_LOGIN):
            if self.authenticate():
                self.add = UserAdditionDialog()
                self.add.show()

    def remove_user(self):
        if self.settings.get(KEY_AUTO_LOGIN):
            if self.authenticate():        
                self.remove = UserRemovalDialog()
                self.remove.show()

    def insert_text(self, text):
        '''Add text to the text console.'''
        self.text_edit.append('\n' + text)
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.ensureCursorVisible()

    def insert_markdown(self, text):
        self.text_edit.setMarkdown(text)
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.ensureCursorVisible()

    def load_file_text(self, filename='instructions.txt'):
        '''Load text from a file and add it to the text area.'''
        self.text_edit.setMarkdown(INSTRUCTIONS + '   \r\n')
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.ensureCursorVisible()
        return

    def aboutQt(self):
        QApplication.aboutQt()

    def connect_device(self):
        if self.connecting:
            return

        if self.device is None:
            self.device = USBDeviceHandler(
                device_connected_callback=self.notify_device_connected,
                wait=self.settings.get(KEY_ARDUINO_WAIT),
                shutdown_on_exception=self.settings.get(
                    KEY_SHUTDOWN_ON_EXCEPTION),
                sleep_tune=self.settings.get(KEY_SLEEP_TUNE),
                debug=self.settings.get(KEY_DEBUG),
            )

        if not self.device.is_connected():
            self.connecting = True
            self.label_usb_icon.setText(ICON_USB_YELLOW)
            self.usb_label.setStyleSheet(YELLOW)
            self.usb_label.setText('Connecting...')
            self.device.connect(self.notify_device_connected)

    def notify_device_connected(self, connected, message=None):
        '''Callback for the USB device.'''

        if connected:  # device is connected
            self.label_usb_icon.setText(ICON_USB_GREEN)
            self.usb_label.setStyleSheet(GREEN)
            self.usb_label.setText(f'USB: {self.device.serial_port.port}')
            self.actionConnect.setText('Disconnect')
            self.actionConnect.triggered.disconnect(
                self.connect_device
            )  # disconnect the connect action
            self.actionConnect.triggered.connect(
                self.disconnect_device
            )  # connect the disconnect action
            atexit.register(self.device.cleanup)

            # Save this port to the settings
            self.settings.set(KEY_COM_PORT, self.device.serial_port.port)

            if self.settings.get(KEY_DEBUG):
                app_logger.debug(
                    f'USB: connected to {self.device.serial_port.port}')
            lgr.success(f'USB: connected to {self.device.serial_port.port}')

        else:  # device is not connected
            lgr.error(f'Error: {message}')
            if self.settings.get(KEY_DEBUG):
                app_logger.error(f'USB: connection failed. Error: {message}')
                lgr.error(f'USB: connection failed. Error: {message}')
            if message is not None and str.__contains__(
                message, 'Incorrect Arduino ID'
            ):
                self.insert_text(f'Connection Failed. {message}')
            self.label_usb_icon.setText(ICON_USB_RED)
            self.connect_menu.setEnabled(True)
            self.actionConnect.setText('Connect')
            self.usb_label.setStyleSheet(RED)
            self.usb_label.setText('USB: connection failed')
            self.device = None

        # usb_device = self.device
        self.connecting = False

    def disconnect_device(self):
        # global usb_device
        if self.device is not None:
            atexit.unregister(self.device.cleanup)
            self.device.set_all_pins_to_value(0)
            self.actionConnect.setText('Connect')
            self.connect_menu.setEnabled(True)
            self.actionConnect.triggered.connect(self.connect_device)
            self.actionConnect.triggered.disconnect(self.disconnect_device)
            self.label_usb_icon.setText(ICON_USB_RED)
            self.usb_label.setStyleSheet(RED)
            self.usb_label.setText('USB: disconnected')
            if self.settings.get(KEY_DEBUG):
                app_logger.debug('USB: disconnected.')
                lgr.debug('USB: disconnected.')
            self.device.cleanup()
            self.device = None

            # usb_device = None

    def control_manually(self):
        self.manual = ManualWidget(self.device)
        self.manual.show()

    def execute_test(self):
        '''Run the test.'''
        if self.testing:
            self.button_pressed = True
        elif not self.blocked:
            if self.eax_device.get_name() is None:
                QMessageBox.warning(
                    self, 'Error', f'Please select a device.', QMessageBox.Ok
                )
                return
            if self.device is None:
                QMessageBox.warning(
                    self, 'Error', f'USB device not connected.', QMessageBox.Ok
                )
                return
            elif not self.device.is_connected():
                QMessageBox.warning(
                    self, 'Error', f'USB device not connected.', QMessageBox.Ok
                )
                return

            self.blinker_running = False
            app_logger.info(
                f'Testing started for {self.eax_device.selected_device}')
            lgr.info(f'Testing started for {self.eax_device.selected_device}')

            self.queue = []

            speed = self.settings.get(KEY_TESTING_SPEED)

            self.text_edit.setMarkdown(
                f'# Starting test for {self.eax_device.selected_device}... '
            )

            self.queue.append(  # turn on indicator
                (1, self.device.write_pin_by_func, 'testing indicator', 1)
            )

            self.queue.append(
                (
                    int(speed / 4),
                    self.insert_text,
                    ' - Turning on battery power...',
                )
            )

            self.queue.append(  # turn on battery
                ((1), self.device.write_pin_by_func, 'battery', 1)
            )

            self.queue.append(
                (
                    int(speed),
                    self.insert_text,
                    ' - Starting low battery test...',
                )
            )

            self.queue.append(  # turn on low battery
                ((1), self.device.write_pin_by_func, 'low battery', 1)
            )

            self.queue.append((int(speed), self.insert_text,
                              ' - Low battery test off.'))

            self.queue.append(  # turn off low battery
                ((1), self.device.write_pin_by_func, 'low battery', 0)
            )

            self.queue.append(
                (
                    int(500),
                    self.insert_text,
                    (
                        ' - Perform the following:\n\t  1. Press the key switch: The'
                        ' siren sounds\n\t  2. Press the cylinder switch: The LEDs'
                        ' turn on'
                    ),
                )
            )

            self.queue.append(
                (
                    int(200),
                    self.insert_text,
                    '\n\nPress the Continue button to finish testing...',
                )
            )

            self.queue.append((1, self.wait_for_button))

            self.queue.append(  # turn off battery
                ((1), self.device.write_pin_by_func, 'battery', 0)
            )

            self.queue.append(
                (10, self.load_file_text, 'instructions.txt'))

            self.queue.append(  # turn off indicator
                ((1), self.device.write_pin_by_func, 'testing indicator', 0)
            )

            self.testing = True
            self.blocked = True
            # Start processing the queue
            self.process_queue()

        else:
            self.insert_text('Cannot run test.')

    def process_queue(self):
        '''Process the queue.'''
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

    def modify_settings(self):
        # if auto login is enabled, force the user to login
        if self.settings.get(KEY_AUTO_LOGIN):
            if self.authenticate():
                self.settings_dialog.show()

    def authenticate(self):
        """Authenticate by showing the login dialog."""
        self.loginDialog = LoginDialog(self.settings.get(KEY_LAST_USER))
        if self.loginDialog.exec() == QDialog.Accepted:
            success, username = self.loginDialog.ok()
            if success:
                self.settings.set(KEY_LAST_USER, username)
            else:
                QMessageBox.critical(self.loginDialog,'Invalid credentials',('The username or password you entered is incorrect. Please try again.'),)
            return success
        else:
            return False

    def on_settings_closed(self, result):
        # global settings
        self.settings = settings
        lgr.info(f'Settings dialog closed. Result: {result}')
        self.text_edit.setStyleSheet(
            f'color: {self.settings.get(KEY_FOREGROUND_COLOR)}; background-color:'
            f' {self.settings.get(KEY_BACKGROUND_COLOR)};'
        )
        if self.settings.get(KEY_AUTO_LOGIN):
            self.actionLogout.setEnabled(False)
        else:
            self.actionLogout.setEnabled(True)
        if self.settings.get(KEY_FULLSCREEN):
            self.showFullScreen()
        else:
            self.showNormal()

    def wait_for_button(self):
        self.waiting = True
        icon = QIcon()
        if not self.button_pressed:
            QTimer.singleShot(100, self.wait_for_button)
            size = QSize(h=55, w=55)
            icon.addFile(
                ':/resources/icons/images/icons/forward-button.png',
                size,
                QIcon.Normal,
                QIcon.On,
            )
            self.test_button.setIcon(icon)
        else:
            size = QSize(h=100, w=100)
            icon.addFile(
                ':/resources/icons/images/icons/test-button.png',
                size,
                QIcon.Normal,
                QIcon.On,
            )
            self.test_button.setIcon(icon)
            self.button_pressed = False
            self.waiting = False
            self.process_queue()

    def perform_task(self, task, args):
        '''
        Execute a task.

        :param task: The task to execute.
        :param args: The arguments to pass to the task.
        '''
        task(*args)
        self.process_queue()  # Continue processing the queue

    def program(self):
        '''Program the device.'''
        if not self.blocked and self.eax_device.get_name() is not None:
            # Check if the firmware file exists
            if not os.path.exists(self.eax_device.get_firmware()):
                self.insert_text(f'{self.eax_device.get_firmware()} not found!')
                return

            self.settings.load_settings()

            chip = self.settings.get('chip_part')
            serial = self.settings.get('programmer_serial_number')
            command = [
                'up.exe',
                f'/part {chip}',
                f'/s {serial}',
                f'/p {self.eax_device.get_firmware()}',
                '/q1',
            ]

            if self.settings.get('debug'):
                lgr.debug(' '.join(command))

            self.blocked = True

            app_logger.info(
                f'Programming {self.eax_device.selected_device} args: {command}'
            )
            self.runner = CommandRunner(command)
            self.runner.resultReady.connect(
                self.process_result
            )  # Connect the signal to the handler
            self.runner.start()

    def process_result(self, returncode):
        # This function gets called when the command finishes.
        # Do whatever you need to do with the return code here.
        if returncode == 0:
            self.insert_text('Programming successful.')
            app_logger.info(
                f'Programming {self.eax_device.selected_device} successful')
            lgr.success(
                f'Programming {self.eax_device.selected_device} successful')
            if self.settings.get(KEY_AUTO_TEST):
                self.execute_test()
        else:
            lgr.error(
                f'Programming {self.eax_device.selected_device} failed. Error code: {returncode}'
            )
            self.insert_text(
                f'\nProgramming {self.eax_device.selected_device} failed. Error code: {returncode}'
            )
            app_logger.error(
                f'Programming {self.eax_device.selected_device} failed. Error code: {returncode}'
            )
        self.blocked = False

    def show_log(self):
        '''Show the logs in the text area.'''
        logs = AppLogger.get_table()
        self.log_view = LogView(logs, 4, 3)
        self.log_view.show()

    def perform_login(self):
        '''Show the login dialog.'''
        success, username = False, None
        # Block until the user is logged in
        while not success and self.window().isVisible():
            self.loginDialog = LoginDialog(self.settings.get(KEY_LAST_USER))
            if self.loginDialog.exec() == QDialog.Accepted:
                success, username = self.loginDialog.ok()
                if not success:
                    QMessageBox.critical(
                        self.loginDialog,
                        'Invalid credentials',
                        (
                            'The username or password you entered'
                            'is incorrect. Please try again.'
                        ),
                    )
            else:
                self.close()
        if success:
            if settings.get(KEY_AUTO_CONNECT):
                # Auto Connect
                QTimer.singleShot(1000, self.connect_device)
            lgr.success(f'Logged in as: {username}')
            app_logger.info(f'Logged in as: {username}')

            # Block if the user is not an admin
            self.actionModify_Settings.setEnabled(db.is_admin(username))
            self.actionAdd_User.setEnabled(db.is_admin(username))
            self.actionRemove_User.setEnabled(db.is_admin(username))
            # save the last user to the settings
            self.settings.set(KEY_LAST_USER, username)
        else:
            sys.exit(0)

    def closeEvent(self, event):
        lgr.debug(event.isAccepted())
        reply = QMessageBox.question(
            self,
            'Window Close',
            'Are you sure you want to close the window?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply == QMessageBox.Yes:
            lgr.info('Application closed.')
            app_logger.info('Application closed.')
            self.app_settings.setValue('geometry', self.saveGeometry())
            self.app_settings.setValue('windowState', self.saveState())
            event.accept()
        else:
            event.ignore()

    def show(self):
        super().show()
        if not self.settings.get(KEY_AUTO_LOGIN):
            self.perform_login()
        else:
            self.actionLogout.setEnabled(False)

    def update_firmware(self):
        """Update the test fixture firmware."""

        if self.settings.get(KEY_AUTO_LOGIN):
            if not self.authenticate():
                return
        
        app_logger.info('Updating firmware...')
        self.disconnected = False
        if self.device is not None:
            self.disconnected = True
            self.disconnect_device()
        id = str(self.settings.get(KEY_ARDUINO_INSTANCE_ID))
        port = self.settings.get(KEY_COM_PORT)

        # Define the PowerShell script path
        script_path = '.\\Scripts\\UpdateFirmware.PS1'
        self.update_process.setWorkingDirectory(os.getcwd())
        self.text_edit.setMarkdown(f'# Updating firmware... \n\n')

        # Define the command to execute
        self.update_process.start(
            'powershell.exe',
            ['-ExecutionPolicy', 'ByPass', '-File', script_path, id, port],
        )

    def on_error(self, error):
        lgr.error('An error occurred: ', error)
        lgr.error('System reported: ', self.update_process.errorString())
        app_logger.error('Firmware update failed: ', error)

    def read_standard_output(self):
        output = self.update_process.readAllStandardOutput().data().decode()
        self.insert_text(output)
        lgr.info(output)
        msg = self.update_process.readAllStandardError().data().decode()
        if msg != '':
            self.insert_text(msg)
            lgr.error(msg)

    def on_finished(self):
        lgr.success('The process has finished')
        app_logger.info('Firmware update complete.')
        if self.disconnected:
            self.connect_device()
        self.update_process.terminate()
        if not self.update_process.waitForFinished(3000):
            self.update_process.kill()
            lgr.error('Process did not terminate in time.')


class ManualWidget(QWidget, Ui_ManualControlDialog):
    '''
    Manual control dialog. This dialog allows the user to manually control the
    pins of the USB device.

    :param usb_handler: The USB connection handler.
    '''

    def __init__(self, usb_handler=None):
        super().__init__()
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.usb_device = usb_handler

        if self.usb_device is None or not self.usb_device.is_connected():
            QMessageBox.warning(
                self, 'Error', f'USB device not connected.', QMessageBox.Ok
            )
            self.close()
            return
        self.battery_button.clicked.connect(self.toggle_battery)
        self.low_battery_button.clicked.connect(self.toggle_low_battery)
        self.test_indicator_button.clicked.connect(
            self.toggle_testing_indicator)
        self.indicator_button.clicked.connect(self.toggle_indicator)

    def toggle_battery(self, checked):
        if checked:
            value = 1
        else:
            value = 0
        self.usb_device.write_pin_by_func('battery', value)

    def toggle_low_battery(self, checked):
        if checked:
            value = 1
        else:
            value = 0
        self.usb_device.write_pin_by_func('low battery', value)

    def toggle_testing_indicator(self, checked):
        if checked:
            value = 1
        else:
            value = 0
        self.usb_device.write_pin_by_func('testing indicator', value)

    def toggle_indicator(self, checked):
        if checked:
            value = 1
        else:
            value = 0
        self.usb_device.write_pin_by_func('indicator', value)

    def closeEvent(self, event):
        if self.usb_device is not None:
            if self.usb_device.is_connected():
                self.usb_device.set_all_pins(0)
                self.usb_device.write_pin_by_func('indicator', 1)
        event.accept()


class SettingsDialog(QWidget, Ui_Settings):
    '''
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
    '''

    closed = QtCore.Signal(ApplicationSettings)

    def __init__(self, parent):
        super().__init__()
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.settings = settings
        self.settings.load_settings()
        if not self.settings.validate_settings():
            QMessageBox.warning(
                self,
                'Error',
                f'Error loading settings. File not found.',
                QMessageBox.Ok,
            )
            self.close()
            return

        for i in range(CHIP_PARTS.__len__()):
            self.comboBox_chip.addItem(CHIP_PARTS[i])

        for port in USBDeviceHandler.get_usb_ports():
            self.comboBox_com_port.addItem(port)

        self.comboBox_com_port.setCurrentText(self.settings.get(KEY_COM_PORT))

        self.commandLinkButton_select_color.clicked.connect(self.pick_color)
        self.commandLinkButton_bg_color.clicked.connect(
            self.pick_background_color)

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_default.clicked.connect(self.reset_to_default)

        lcd = self.lcdNumber
        palette = lcd.palette()
        palette.setColor(QPalette.WindowText, Qt.blue)
        lcd.setPalette(palette)
        self.apply_changes()

    def apply_changes(self):
        self.lineEdit_serial.setText(
            self.settings.get(KEY_PROGRAMMER_SERIAL_NUMBER))
        self.comboBox_chip.setCurrentIndex(
            CHIP_PARTS.index(self.settings.get(KEY_CHIP_PART))
        )
        value = self.settings.get(KEY_TESTING_SPEED)
        self.spinBox_autologoff_delay.setValue(
            self.settings.get(KEY_LOGOFF_DELAY))
        self.dial.setValue(value)
        self.spinBox_arduino_id.setValue(
            self.settings.get(KEY_ARDUINO_INSTANCE_ID))
        self.checkBox_test.setChecked(self.settings.get(KEY_AUTO_TEST))
        self.checkBox_connect.setChecked(self.settings.get(KEY_AUTO_CONNECT))
        self.checkBox_debug.setChecked(self.settings.get(KEY_DEBUG))
        self.checkBox_logon.setChecked(self.settings.get(KEY_AUTO_LOGIN))
        self.checkBox_auto_find.setChecked(self.settings.get(KEY_AUTO_FIND))
        self.checkBox_shutdown_on_exception.setChecked(
            self.settings.get(KEY_SHUTDOWN_ON_EXCEPTION)
        )
        self.lineEdit_serial_sleep_tune.setText(
            str(self.settings.get(KEY_SLEEP_TUNE)))
        self.spinBox_wait_time.setValue(self.settings.get(KEY_ARDUINO_WAIT))
        self.checkBox_fullscreen.setChecked(self.settings.get(KEY_FULLSCREEN))

    def reset_to_default(self):
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

    def save_changes(self):
        self.settings.set(KEY_COM_PORT, self.comboBox_com_port.currentText())
        self.settings.set(KEY_CHIP_PART, self.comboBox_chip.currentText())
        self.settings.set(KEY_PROGRAMMER_SERIAL_NUMBER,
                          self.lineEdit_serial.text())
        self.settings.set(KEY_AUTO_TEST, self.checkBox_test.isChecked())
        self.settings.set(KEY_AUTO_CONNECT, self.checkBox_connect.isChecked())
        self.settings.set(KEY_DEBUG, self.checkBox_debug.isChecked())
        self.settings.set(KEY_AUTO_LOGIN, self.checkBox_logon.isChecked())
        self.settings.set(KEY_ARDUINO_INSTANCE_ID,
                          self.spinBox_arduino_id.value())
        self.settings.set(KEY_TESTING_SPEED, self.dial.value())
        self.settings.set(KEY_LOGOFF_DELAY,
                          self.spinBox_autologoff_delay.value())
        self.settings.set(KEY_AUTO_FIND, self.checkBox_auto_find.isChecked())
        self.settings.set(
            KEY_SHUTDOWN_ON_EXCEPTION, self.checkBox_shutdown_on_exception.isChecked()
        )
        self.settings.set(KEY_SLEEP_TUNE, float(
            self.lineEdit_serial_sleep_tune.text()))
        self.settings.set(KEY_ARDUINO_WAIT, self.spinBox_wait_time.value())
        self.settings.set(KEY_FULLSCREEN, self.checkBox_fullscreen.isChecked())
        self.settings.save_settings()
        self.close()

    def pick_color(self):
        old_color = QColor(self.settings.get(KEY_FOREGROUND_COLOR))
        color = QColorDialog.getColor(old_color, self)
        if color.isValid():
            lgr.debug(f'User selected color: {color.name()}')
            self.settings.set(KEY_FOREGROUND_COLOR, f'{color.name()}')

    def pick_background_color(self):
        old_color = QColor(self.settings.get(KEY_BACKGROUND_COLOR))
        color = QColorDialog.getColor(old_color, self)
        if color.isValid():
            lgr.debug(f'User selected color: {color.name()}')
            self.settings.set(KEY_BACKGROUND_COLOR, f'{color.name()}')

    def closeEvent(self, event):
        self.settings.load_settings()
        self.closed.emit((0, self.settings))
        event.accept()


class UserAdditionDialog(QDialog, Ui_AddUserDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

        self.users = db.get_users()

    def save(self):
        lgr.debug(self.lineEdit_username.text())
        lgr.debug(self.lineEdit_password.text())
        admin = self.checkBox.isChecked()
        db.insert_user(
            self.lineEdit_username.text(), self.lineEdit_password.text(), admin
        )
        self.close()


class UserRemovalDialog(QDialog, Ui_RemoveUserDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.us = db.get_users()
        for username in self.us:
            self.comboBox.addItem(username)

        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

    def save(self):
        selected_username = self.comboBox.currentText()
        if selected_username == 'dmh':
            QMessageBox.critical(
                self,
                'Error',
                f'Cannot remove user: {selected_username}',
                QMessageBox.Ok,
            )
            self.close()
            return
        db.remove_user(selected_username)


class LoginDialog(QDialog, Ui_LoginDialog):
    '''
    Login dialog. This dialog allows the user to login to the application.

    :param last_user: The last user that logged in.
    '''

    def __init__(self, last_user=None):
        super().__init__()
        self.setupUi(self)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        if settings.get(KEY_DEBUG):
            lgr.debug(db.get_users())

        for username in db.get_users():
            self.comboBox.addItem(username)
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


class LogView(QWidget, Ui_LogView):
    '''
    The LogView class represents a widget that displays logs in tabular format.

    :param data: The log data to be displayed, expected as a list of lists where each sub-list represents a log entry.
    :param *args: Optional additional arguments.
    '''

    def __init__(self, data, *args):
        super().__init__()
        self.setupUi(self)
        self.data = data
        self.tableWidget.setRowCount(len(self.data))
        self.setData()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def setData(self):
        horHeaders = ['Date', 'Level', 'Message']
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                newitem = QTableWidgetItem(self.data[i][j])
                self.tableWidget.setItem(i, j, newitem)
        self.tableWidget.setHorizontalHeaderLabels(horHeaders)


class HelpDialog(QDialog, Ui_HelpDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class CommandRunner(QThread):
    resultReady = Signal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.run(' '.join(self.command))
        self.resultReady.emit(process.returncode)


class ConnectMenu(QMenu):
    '''A custom QMenu that emits a signal when clicked.'''

    menu_clicked = Signal()

    def showEvent(self, event):
        self.menu_clicked.emit()


class SingleInstanceApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.semaphore = QSystemSemaphore('EAXInterfaceSemaphore', 1)
        self.semaphore.acquire()

        self.shared_memory = QSharedMemory('EAXInterface')
        self.shared_memory.attach()
        self.shared_memory.detach()
        self.is_running = False

        if not self.shared_memory.create(1):
            self.is_running = True
            return

        self.semaphore.release()


def check_requirements():
    missing = ''
    for file in FILES:
        if not os.path.exists(file):
            missing += file + '\n'
    if missing != '':
        lgr.critical(f'Missing files:\n{missing}')
        return (False, missing)
    return (True, None)


if __name__ == '__main__':
    with lgr.catch(message='Encountered exception from main.',
                   reraise=True,
                   exception=BaseException,
                   ):
        (success, missing) = check_requirements()
        if not success:
            QMessageBox.critical(None, 'Error', f'Missing files:\n{missing}', QMessageBox.Ok)
            sys.exit(1)

        app = SingleInstanceApp([])

        if app.is_running:
            lgr.critical(
                "Another instance of the application is already running.")
            QMessageBox.critical(
                None, 'Error', 'Another instance of the application is already running.', QMessageBox.Ok,)
            sys.exit(1)

        window = MainWindow(app)
        window.show()
        app.exec()
