
import os
import sys
from pathlib import Path

# Check if the script is running in a frozen state (e.g., PyInstaller)
# and redirect stdout/stderr to a log file if so.
if getattr(sys, "frozen", False) and sys.stdout is None:
    log_path = Path.cwd() / "stdout.log"
    sys.stdout = sys.stderr = open(log_path, "w", buffering=1, encoding="utf-8", errors="backslashreplace")

from qtpy import (
    QtGui,
)
from qtpy.QtGui import (
    QIcon,
    QMovie,
    QAction,
    QKeyEvent,
)
from qtpy.QtCore import (
    QTimer,
    Qt,
    QSize,
    QProcess,
    QSize,
    QByteArray,
    QObject,
    Slot,
    QLockFile,
    QDir,
    QUrl,
    Qt,
)
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QInputDialog,
    QActionGroup,
)
# import util.config_resources_rc
import icons_rc
from ui import Ui_MainWindow, Ui_ManualControlDialog
from imports import (
    createActionGroup,
    get_theme,
    get_font,
    take_screenshot,
    warning,
)
import os
import sys
import subprocess
import qdarkstyle
import asyncio
import settings
import constants
import config_loader as cfg
from constants import State
from config_loader import get_config as get_config
from arduino import AIODevice
from chipSelectDialog import ChipSelectDialog
from qasync import QEventLoop
from pathlib import Path
from typing import List, Dict
from device import Device, load_devices
from globals import logger as log
from util.resources import extract_zip_from_resources
from test_controller import MessageType, TestController, ControllerMessage, TestState
from help_dialog import HelpDialog
from log_view import LogView, SaveWorker, ProgressBar
from settings_dialog import SettingsDialog
from imports import critical, from_string
from status_widget import CustomStatusBar
from manual_widget import ManualWidget
from firmware_update import FirmwareUpdateProcess
import counter
from menu_item import MenuItem
from editor import Editor
from pathlib import Path
from firmware_update import FirmwareUpdateProcess


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    This is the main application window. It contains the primary logic for controlling the application.

    :param QMainWindow: The main window.
    :type QMainWindow: QMainWindow
    :param Ui_MainWindow: The main window UI.
    :type Ui_MainWindow: Ui_MainWindow
    """

    _state: State = State.IDLE
    log_view: LogView | None = None
    help_dialog: HelpDialog | None = None
    arduino: AIODevice | None = None
    testController: TestController | None = None
    program_process: QProcess | None = None

    def __init__(self, app, settings=None) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(constants.ICON_WINDOW))
        self.setWindowTitle(f"{constants.APP_NAME} v{constants.APP_VERSION}")

        self.show_movie()

        # Settings
        self.settings = settings.get_instance()
        self.settings_dialog = SettingsDialog(self)

        # Restore the window geometry and state
        self.restoreGeometry(self.settings.app_settings.value("mainwindow/geometry", QByteArray()))
        self.restoreState(self.settings.app_settings.value("mainwindow/windowState", QByteArray()))

        if self.settings.app_settings.value(constants.KEY_FULLSCREEN, type=bool):
            self.showFullScreen()
        else:
            self.showNormal()
        self.actionFullscreen.triggered.connect(self.toggleFullScreen)
        self.actionFullscreen.setChecked(self.settings.app_settings.value(constants.KEY_FULLSCREEN, type=bool))

        # Process for updating the firmware
        self.update_process = FirmwareUpdateProcess(self)
        self.update_process.outputReceived.connect(lambda data: self.append_text(data, prepend=""))
        self.update_process.finishedWithCode.connect(self.on_finished)

        # Quick Connection Menu
        self.connect_menu = QAction(self)
        self.menuBar().addAction(self.connect_menu)
        self.connect_menu.triggered.connect(lambda: asyncio.create_task(self.connect_task()))

        # Inactivity timer
        self.inactivityTimer = QTimer(self)
        self.inactivityTimer.setSingleShot(True)
        self.inactivityTimer.timeout.connect(self.handle_inactivity_timeout)
        self.inactivityTimer.start(settings.get_int(constants.KEY_INACTIVITY_TIMEOUT, 15) * 60 * 1000)

        # Setup the text area
        if (font_str := settings.get(constants.KEY_FONT, "")):
            self.text_edit.setFont(from_string(font_str))

        self.text_edit.setStyleSheet(f"color:{self.settings.get(constants.KEY_FOREGROUND_COLOR)};" f"background-color:{self.settings.get(constants.KEY_BACKGROUND_COLOR)};")
        self.text_edit.anchorClicked.connect(self.check_for_link)
        self.text_edit.setOpenLinks(False)

        # Connect the menu items
        self.actionExplore_Directory.triggered.connect(lambda: subprocess.Popen(f"explorer {os.getcwd()}"))
        self.actionUpdate_Firmware.triggered.connect(self.update_firmware)
        self.actionConnect.triggered.connect(lambda: asyncio.create_task(self.connect_task()))
        self.actionAbout.triggered.connect(lambda: QApplication.aboutQt())
        # self.actionChip_Select.triggered.connect(self.get_chip_part)
        self.actionChip_Select.triggered.connect(lambda: ChipSelectDialog.get_chip(self))
        self.actionShow_Logs.triggered.connect(self.show_log)
        self.actionChange_font.triggered.connect(self.choose_font)
        self.actionManual_Control.triggered.connect(self.control_manually)
        self.actionModify_Settings.triggered.connect(lambda: self.settings_dialog.show())
        self.actionHelp.triggered.connect(lambda: HelpDialog(self).show())
        self.actionStatisitics.triggered.connect(self.show_statistics)
        self.actionDark_Theme.triggered.connect(self.toggle_theme)
        self.actionScreenshot.triggered.connect(take_screenshot)
        self.program_button.clicked.connect(self.program)
        self.test_button.clicked.connect(self.on_test_clicked)
        self.actionOpen_UP_exe.triggered.connect(lambda: QProcess.startDetached(cfg.get_config().get_programmer_path()))
        self.actionEditConfig.triggered.connect(self.edit_config)

        # Set the theme
        self.set_theme(get_theme(self.settings))

        # Load the devices from the config file and add each device to the menu
        self.menuDevice.clear()
        [self.menuDevice.addAction(MenuItem(device, self)) for device in load_devices()]

        self.actionGroup: QActionGroup = createActionGroup(self, self.menuDevice.actions())
        self.actionGroup.triggered.connect(self.deviceSelect)

        self.load_file_text()

        # Initialize the counters
        self.test_counter = counter.Counter("test_count")
        self.program_counter = counter.Counter("program_count")
        self.program_fail_counter = counter.Counter("program_fail_count")

        self.setStatusBar(CustomStatusBar(self))
        self.set_status('Select a device to begin.')

        # If auto connect is enabled, try to connect to the USB device
        if self.settings.get(constants.KEY_AUTO_CONNECT):
            QTimer.singleShot(500, lambda: asyncio.create_task(self.connect_task()))

    def set_status(self, message: str, timeout: int = 0) -> None:
        """Set the status message in the status bar."""
        sb = self.statusBar()
        sb.showMessage(message, timeout)

    @property
    def state(self) -> State:
        # print(f"Getting state: {self._state}")
        return self._state

    @state.setter
    def state(self, value: State) -> None:
        """Set the state of the application and update the UI accordingly."""
        self.resetInactivityTimer()  # reset the inactivity timer
        log.debug(f"Previous state: {self._state}, New State: {value}", 1)
        if value == State.CONNECTING:
            self.actionConnect.setEnabled(False)
            # self.label_usb_icon.setText(constants.ICON_USB_YELLOW)
            self.set_status("Connecting to USB device...")
            self.usb_label.setText("USB connecting...")
            self.usb_label.setStyleSheet(
                cfg.get_config().get('window').get('usb_label').get('connecting_style')
            )
            self.show_movie(pause=False)
        elif value == State.CONNECTED:
            self.controlBox.setEnabled(True)
            self.usb_label.setStyleSheet(
                cfg.get_config().get('window').get('usb_label').get('connected_style')
            )
            self.set_status(f"Connected to {self.arduino.device.com_port}.")
            self.show_movie(pause=False)
        elif value == State.IDLE:
            self.program_button.setEnabled(True)
            self.actionConnect.setEnabled(True)
            # self.label_usb_icon.setText(constants.ICON_USB_RED)
            self.set_status("Disconnected.")
            self.show_movie(pause=True)
            if self._state == State.CONNECTED:  # only if we were connected
                self.usb_label.setStyleSheet(
                    cfg.get_config().get('window').get('usb_label').get('disconnected_style')
                )
                self.usb_label.setText(
                    cfg.get_config()
                    .get('window')
                    .get('usb_label')
                    .get('disconnected_text')
                    .format(msg="disconnected")
                )
        elif value == State.PROGRAMMING:
            self.controlBox.setEnabled(False)
            self.actionConnect.setEnabled(False)
            self.set_status("Programming...")
            self.show_movie(pause=False)
        elif value == State.TESTING:
            self.controlBox.setEnabled(True)
            self.actionConnect.setEnabled(False)
            self.set_status("Testing...")
        elif value == State.WAITING_FOR_BUTTON:
            self.controlBox.setEnabled(True)
            self.actionConnect.setEnabled(False)
            self.set_status("Waiting for input...")

        self._state = value

    def edit_config(self) -> None:
        """Open the configuration file for editing."""
        editor = Editor(self)
        editor.set_current_file('config.yaml')
        editor.show()

    def check_for_link(self, url: QUrl) -> None:
        """Check if the cursor is over a link."""
        print(url)
        if url.url() == "continue":
            if self.testController and self.testController.state == TestState.AWAITING_BUTTON:
                self.testController.notify_button_pressed()
                return
            else:
                log.warning("No test controller or not in the correct state to continue.")
        elif url.url() == "help":
            HelpDialog(self).show()

    def set_theme(self, theme: str) -> None:
        """Set the theme."""
        log.debug(f"Setting theme to {theme}")
        if theme == 'dark':
            style = qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette)
            self.actionDark_Theme.setChecked(True)
        else:
            style = qdarkstyle.load_stylesheet(palette=qdarkstyle.LightPalette)
            self.actionDark_Theme.setChecked(False)
        # self.setStyleSheet(style)

        self.set_icon(self.connect_menu, 'usb2')
        self.set_icon(self.test_button, 'test-button')
        self.set_icon(self.program_button, 'prog-button')

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
        self.set_icon(self.actionModify_Settings, 'settings', 'ico')
        self.set_icon(self.actionHelp, 'help')
        self.set_icon(self.actionStatisitics, 'bar-chart')

    def toggle_theme(self) -> None:
        """Toggle the theme between light and dark."""
        log.debug("Toggle theme")

        dark = self.settings.get_bool(constants.KEY_DARK_THEME)

        self.settings.app_settings.setValue(constants.KEY_DARK_THEME, not dark)
        self.set_theme('dark' if not dark else 'light')
        self.actionDark_Theme.setChecked(not dark)

    def set_icon(self, widget: QObject, icon_name: str, ext='png') -> None:
        """Set the icon for a widget based on the current theme."""
        dark = self.settings.get_bool(constants.KEY_DARK_THEME)
        icon_path = f":/images/icons/{'light' if dark else 'dark'}/{icon_name}.{ext}"
        icon = QIcon()
        icon.addFile(icon_path, QSize(), QIcon.Normal, QIcon.On)
        widget.setIcon(icon)

    def toggleFullScreen(self) -> bool:
        if not self.settings.app_settings.value(constants.KEY_FULLSCREEN, defaultValue=False):
            self.showFullScreen()
            self.settings.app_settings.setValue(constants.KEY_FULLSCREEN, True)
            self.actionFullscreen.setChecked(True)
            return True
        else:
            self.showNormal()
            self.settings.app_settings.setValue(constants.KEY_FULLSCREEN, False)
            self.actionFullscreen.setChecked(False)
            return False

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self.close()
        elif key == Qt.Key.Key_F11:
            self.toggleFullScreen()
        elif key == Qt.Key.Key_F12:
            self.show_statistics()
        elif key == Qt.Key.Key_F10:
            self.show_log()
        elif key == Qt.Key.Key_F1:
            HelpDialog(self).show()
        elif key == Qt.Key.Key_F5:
            self.settings_dialog.show()
        elif key == Qt.Key.Key_F6:
            self.toggle_theme()
        elif key == Qt.Key.Key_Question:
            HelpDialog(self).show()
        elif key == Qt.Key.Key_Q and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            asyncio.get_event_loop().stop()
            self.close()
        elif key == Qt.Key.Key_F2:
            take_screenshot()
        elif key == Qt.Key.Key_F3:
            self.control_manually()
        elif key == Qt.Key.Key_F4:
            self.actionConnect.trigger()
        # elif key == Qt.Key.Key_E and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
        #     logg.export_logs()
        elif key == Qt.Key.Key_R and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            is_frameless = self.windowFlags() & Qt.FramelessWindowHint
            # Toggle between frameless and regular states
            if is_frameless:
                self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
                self.settings.setValue(constants.KEY_FRAMELESS, False)
            else:
                self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
                self.settings.setValue(constants.KEY_FRAMELESS, True)
            QTimer.singleShot(10, self.show)
            # elif key == Qt.Key.Key_1 and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # log.warning(f"State: {self.state}")
            # elif (
            #     key == Qt.Key.Key_2 and
            #     event.modifiers() & Qt.KeyboardModifier.ControlModifier
            # ):
            log.warning(f"Device: {self.get_selected_device().name}")
        elif key == Qt.Key.Key_A and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # print(vars(self))
            # print(vars(self.settings))
            # print(vars(app_logger))
            # print(vars(self.arduino))
            # print(vars(db))
            # print(vars(logg))
            # self.text_edit.setAcceptRichText(True)
            # self.load_file_text()
            # print(self.arduino)
            # print(self.state)
            # print(self.testController.state)
            self.handle_inactivity_timeout()
            print(f"""
                  Checked Action: {self.get_selected_device()}
                  """)
            # print(self.label_usb_icon.size())
            # print(self.arduino)
            # print(settings.get_instance())
            # print(self.settings)
            # self.statusBar().set_value(59999)
            # self.menuBar().setEnabled(not self.menuBar().isEnabled())

    def show_movie(self, pause: bool = False) -> None:
        """Show or hide the GIF in the USB icon label."""
        if self.label_usb_icon.movie() is None:
            movie = QMovie(constants.MOVIE_ICON)
            size = QSize(120, 100)  # Set the size of the movie
            movie.setScaledSize(size)
            movie.setSpeed(200)
            self.label_usb_icon.setMovie(movie)
        self.label_usb_icon.movie().setPaused(pause)

    def is_movie_running(self) -> bool:
        """Check if the movie in the USB icon label is running."""
        if self.label_usb_icon.movie() is not None:
            return self.label_usb_icon.movie().state() == QMovie.Running
        return False

    def resetInactivityTimer(self) -> None:
        """Reset the inactivity timer."""
        log.debug(f"Resetting inactivity timer: remaining time: {self.inactivityTimer.remainingTime()/1000/60} minutes")
        self.inactivityTimer.start(
            self.settings.get_int(constants.KEY_INACTIVITY_TIMEOUT, constants.DEFAULT_SETTINGS[constants.KEY_INACTIVITY_TIMEOUT]) * 60 * 1000
        )

    def handle_inactivity_timeout(self) -> None:
        """Called when the inactivity timer times out."""
        log.debug("Inactivity timeout.")
        self.device_label.setText("Device not selected")  # clear the device label
        self.actionGroup.checkedAction().setChecked(False) if self.actionGroup.checkedAction() else None  # reset the device

    # ----- Device Select Functions ----- #

    def get_selected_device(self) -> Device:
        """Get the currently selected device from the menu."""
        return self.actionGroup.checkedAction().data() if self.actionGroup.checkedAction() else None

    @Slot(QAction)
    def deviceSelect(self, action: QAction) -> None:
        """Called when a device is selected from the menu."""
        device: Device = action.data()
        log.info(f"Device changed to: {device}")
        self.device_label.setText(f'<html><head/><body><p><span style="{device.styles}">Device: {device.name}</span> </p></body></html>')

    def choose_font(self) -> None:
        (ok, font) = get_font(self.text_edit.font())
        if ok:
            log.debug(f"User selected font: {font.toString()}")
            self.text_edit.setFont(font)
            settings.setValue('mainwindow/font', font.toString())

    # def get_chip_part(self) -> None:
    #     current_chip = self.settings.get(constants.KEY_CHIP_PART)
    #     current_selection = constants.CHIP_OPTIONS.index(current_chip)
    #     item, okPressed = QInputDialog.getItem(self, "Select Chip", "Chip:", constants.CHIP_OPTIONS, current_selection, False)
    #     if okPressed and item:
    #         self.settings_dialog.comboBox_chip.setCurrentText(item)  # update the combo box
    #         self.settings.setValue(constants.KEY_CHIP_PART, item)
    #         log.debug(f"saved chip settings: {item}")

    def append_text(self, text: str, prepend: str = "\n") -> None:
        """Add text to the text console."""
        self.text_edit.append(prepend + text)
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.ensureCursorVisible()

    def load_file_text(self, filename="instructions.md") -> None:
        """Load text from a file and add it to the text area"""
        try:
            self.text_edit.setMarkdown(Path(filename).read_text() + "\n")
            self.text_edit.moveCursor(QtGui.QTextCursor.End)
            self.text_edit.ensureCursorVisible()
        except FileNotFoundError:
            log.error(f"Instruction file not found: {filename}")

    # ----- Connection Functions ----- #

    async def connect_task(self) -> None:
        if self.state == State.CONNECTED:
            await self.disconnect_device()
        elif self.state is State.IDLE:
            from arduino import get_device
            self.arduino = get_device()
            self.arduino.connection_changed.connect(self.on_connection_changed)
            self.state = State.CONNECTING
            await self.arduino.ensure_connected()

    def on_connection_changed(self, connected: bool, message: str = None) -> None:
        """Callback for the USB device."""
        log.info(f"Connection changed: {connected}, message: {message}")
        if connected:  # device is connected
            # self.usb_label.setText(f"USB connected: {message}")
            # self.usb_label.setStyleSheet(constants.GREEN)
            self.actionConnect.setText("Disconnect")
            self.state = State.CONNECTED
            self.settings.setValue(constants.KEY_COM_PORT, self.arduino.device.com_port)  # save the port
            self.testController = TestController(self.arduino, parent=self)
            self._connect_controller_signals()
            self.usb_label.setText(cfg.get_config().get('window').get('usb_label').get('connected_text').format(msg=message))

        else:
            self.usb_label.setText(cfg.get_config().get('window').get('usb_label').get('disconnected_text').format(msg="disconnected"))
            self.usb_label.setStyleSheet(cfg.get_config().get('window').get('usb_label').get('disconnected_style'))
            log.error(f"USB: connection lost. Error: {message}")
            self.append_text(f"\n<p>USB Error: {message}</p>")
            self.actionConnect.setText("Connect")
            self.state = State.IDLE

    async def disconnect_device(self):
        # Await the asynchronous disconnect on your device.
        self.usb_label.setText(cfg.get_config().get('window').get('usb_label').get('text').format(msg="disconnected"))
        self.usb_label.setStyleSheet(cfg.get_config().get('window').get('usb_label').get('disconnected_style'))
        self.actionConnect.setText("Connect")
        if self.arduino:
            self.arduino.connection_changed.disconnect(self.on_connection_changed)
            await self.arduino.async_disconnect()
            self.arduino = None  # clear the reference to the device
        self.state = State.IDLE
        log.success("Device disconnected successfully.")

    def _connect_controller_signals(self) -> None:
        """Connect the signals from the test controller to the main window."""
        self.testController.updateText.connect(self.append_text)
        self.testController.sendMessage.connect(self._on_message_received)

    def control_manually(self) -> None:
        ManualWidget(self.arduino).show()

    # ----- Programming Functions ----- #

    def program(self) -> None:
        """Program the selected device with the firmware."""
        self.resetInactivityTimer()  # reset the inactivity timer
        if not self.get_selected_device():
            warning(self, "Please select a device.")
            return

        if self.state not in (State.IDLE, State.CONNECTED):
            return

        fw = self.get_selected_device().firmware_path
        if not os.path.exists(fw):
            self.append_text(f"{fw} not found!")
            return

        previous_state = self.state

        try:
            argv = cfg.get_config().generate_program_arguments(settings=self.settings, device=self.get_selected_device())

            log.info(f"Programming {self.get_selected_device().name}, args: {argv}")

            # create (or reuse) a QProcess
            self.program_process = QProcess(self)

            # when it finishes, grab only the exit code
            self.program_process.finished.connect(lambda code, _: self.handle_programming_result(code, previous_state))
            self.state = State.PROGRAMMING

            self.program_process.setProgram(argv[0])
            self.program_process.setArguments(argv[1:])
            self.program_process.start()
        except Exception as e:
            self.append_text(f'<br><p>Exception during programming: {e}</p>')
            log.exception(f"Exception during programming: {e}")
            self.state = previous_state  # restore the previous state

    @Slot(int, QProcess.ExitStatus)
    def handle_programming_result(self, returncode: int, previous_state: State) -> None:
        """Called when QProcess emits finished()."""
        self.state = previous_state  # restore the previous state
        if returncode == 0:
            self.append_text("<br><p>Programming successful.</p>")
            log.info(f"Programming successful for {self.get_selected_device().name}.")
            self.program_counter.increment()
            if self.settings.get(constants.KEY_AUTO_TEST):
                if self.arduino and self.arduino.device_connected:
                    self.test_button.click()
        else:
            self.program_fail_counter.increment()
            self.append_text(f"<br><p>Programming failed. Return code: {returncode}</p>")
            log.error(f"Programming failed for {self.get_selected_device().name}. Return code: {returncode}")

    def show_statistics(self) -> None:
        """Display the statistics of the programming results."""
        failed = self.program_fail_counter.value
        success = self.program_counter.value
        tests = self.test_counter.value
        log.info(f"Statistics - Failures: {failed}, Successes: {success}, Tests: {tests}")
        QMessageBox().information(self, "Statistics", f"Failures: {failed}\n" f"Successes: {success}\n" f"Tests: {tests}")

    # ----- Log Functions ----- #

    def show_log(self) -> None:
        """Display the log view widget."""
        self.log_view = LogView(log.get_logs(), self.save_logs)
        self.log_view.show()

    def save_logs(self, log_data: List[Dict[str, str]]) -> None:
        """Save the logs."""
        # Create a progress bar to show the progress of the save operation
        self.progress_bar = ProgressBar()

        # Create a worker thread to run in the background
        self.save_worker = SaveWorker(log_data)
        self.save_worker.progress_changed.connect(self.progress_bar.update_progress)
        self.save_worker.started.connect(self.progress_bar.show)
        self.save_worker.finished.connect(self.on_save_finished)
        self.save_worker.start()

    def on_save_finished(self) -> None:
        log.info("Save finished.")
        self.progress_bar.close()
        self.save_worker.quit()  # Stop the worker thread
        self.save_worker.deleteLater()  # Clean up the worker thread

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(
            self,
            "Window Close",
            "Are you sure you want to close the window?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )

        if reply == QMessageBox.StandardButton.Yes:
            log.info("Application closed.")
            # logg.info("Application closed.")
            # app_logger.info("Application closed.")
            self.settings.app_settings.setValue("mainwindow/geometry", self.saveGeometry())
            self.settings.app_settings.setValue("mainwindow/windowState", self.saveState())
            self.settings.app_settings.setValue("mainwindow/full_screen", self.isFullScreen())
            self.settings.app_settings.sync()
            event.accept()
        else:
            event.ignore()

    # ----- Firmware Update Functions ----- #

    async def _prepare_for_firmware_update(self):
        """Disconnects device if connected, preparing for firmware update."""
        if self.arduino and self.arduino.device_connected:
            try:
                # Attempt to disconnect the signal if it was connected
                self.arduino.connection_changed.disconnect(self.on_connection_changed)
            except (TypeError, RuntimeError):  # TypeError if not connected, RuntimeError if already disconnected
                log.debug("Signal already disconnected or was never connected.")
                pass

            await self.arduino.async_disconnect()
            self.arduino = None  # Ensure the old device object is cleared

            # Update UI to reflect disconnection
            self.usb_label.setStyleSheet(get_config().get('window').get('usb_label').get('disconnected_style'))
            self.usb_label.setText(get_config().get('window').get('usb_label').get('disconnected_text').format(msg="Disconnected for update"))
            # self.fixtureLabel.setText(f'{get_config().get("window").get("fixture_label").get("disconnected_text").format(msg="Fixture disconnected for update")}')
            # self.fixtureLabel.setStyleSheet(get_config().get('window').get('fixture_label').get('disconnected_style'))
            self.actionConnect.setText("Connect")
            return True

        return False

    def update_firmware(self) -> None:
        """Update the firmware on the test fixture."""
        # dialog = QMessageBox(self)
        # dialog.setWindowTitle("Select Firmware")
        # dialog.setText("Select the firmware to upload:")
        # dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        # btnFirmata = dialog.button(QMessageBox.StandardButton.Yes)
        # btnFirmata.setText("Firmata (old)")
        # btnTelemetrix = dialog.button(QMessageBox.StandardButton.No)
        # btnTelemetrix.setText("Telemetrix (new)")

        # cancelBtn = dialog.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        # dialog.setDefaultButton(cancelBtn)
        # dialog.setIcon(QMessageBox.Question)

        # dialog.exec()

        # if dialog.clickedButton() == btnFirmata:
        #     firmware_path = ".\\sketches\\StandardFirmata\\build\\arduino.avr.uno\\StandardFirmata.ino.hex"
        # elif dialog.clickedButton() == btnTelemetrix:
        #     firmware_path = ".\\sketches\\Telemetrix4Arduino\\build\\arduino.avr.uno\\Telemetrix4Arduino.ino.hex"
        # else:
        #     log.info("Firmware update cancelled.")
        #     return

        # self.set_status("Updating tester firmware...")
        # log.info("Updating tester firmware...")

        # # Get the COM port from the settings or the Arduino device
        # if self.arduino.device_connected:
        #     port = self.arduino.device.com_port
        #     self.update_process.device_connected = True
        #     asyncio.create_task(self.disconnect_device())
        # else:
        #     self.update_process.device_connected = False
        #     port = self.settings.get(constants.KEY_COM_PORT, constants.DEFAULT_SETTINGS[constants.KEY_COM_PORT])

        # self.state = State.UPDATING

        # script_path = ".\\Scripts\\UpdateFirmware.bat"
        # self.text_edit.setHtml(
        #     f"""<h1>Updating firmware...</h1>
        #                             <p>Firmware: {firmware_path}</p>
        #                             <p>Port: {port}</p>
        #                             """
        # )

        # # Define the command to execute
        # QTimer.singleShot(1000, lambda: self.update_process.run("cmd.exe", ["/c", script_path, firmware_path, port]))
        if QMessageBox.question(
            self,
            "Update Firmware",
            "Are you sure you want to update the firmware?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        ) != QMessageBox.StandardButton.Yes:
            return
        log.info("Updating firmware...")

        self.text_edit.setText(f"<h1>Updating firmware...</h1><br>")
        self.device_label.setText("Updating firmware...")

        script_path = Path("./Scripts/Install.cmd")  # The script to run for the update
        sketch_path = Path("./sketches/Telemetrix4Arduino/Telemetrix4Arduino.ino")  # The sketch to upload
        port = settings.get(constants.KEY_COM_PORT)  # Use the saved COM port from settings
        id = settings.get_int(constants.KEY_ARDUINO_INSTANCE_ID, 1)  # Use the Arduino ID from settings

        async def do_update():
            """Perform the firmware update."""
            was_disconnected = await self._prepare_for_firmware_update()
            # Store 'was_disconnected' in self if needed for on_finished logic
            self.disconnected_during_update = was_disconnected  # Example storage

            self.update_process = QProcess(self)
            self.update_process.finished.connect(self.on_finished)
            self.update_process.errorOccurred.connect(self.on_error)
            self.update_process.readyReadStandardError.connect(self.read_standard_output)
            self.update_process.readyReadStandardOutput.connect(self.read_standard_output)
            QTimer.singleShot(750, lambda: self.update_process.start('cmd.exe', ["/C", str(script_path), str(sketch_path), port, str(id)]))  # Reduced delay for testing

        self.state = State.UPDATING
        asyncio.create_task(do_update())

    def on_error(self, process_error: QProcess.ProcessError) -> None:
        log.error(f'Error updating firmware: {process_error}')
        self.append_text(f"<br><h3>Error updating firmware: {process_error}</h3>")

    def read_standard_output(self) -> None:
        output = self.update_process.readAllStandardOutput().data().decode().strip()
        if output != "":
            print(f"{output}")
            self.append_text(output)

        msg = self.update_process.readAllStandardError().data().decode().strip()
        if msg != "":
            print(f"{msg}")
            self.append_text(msg)

    def on_finished(self, returncode: int) -> None:
        """Called when the update process is finished."""
        self.state = State.IDLE

        if returncode != 0:
            log.error(f"Update process failed with exit code {returncode}.")
            self.append_text(f"<p>Update process failed with exit code {returncode}.</p>")
        else:
            log.success("Firmware update complete.")
            self.append_text("<p>Firmware update complete.</p>")

        if hasattr(self, 'disconnected_during_update') and self.disconnected_during_update:
            QTimer.singleShot(500, lambda: asyncio.create_task(self.connect_task()))  # Reconnect with a small delay
            del self.disconnected_during_update  # Clean up flag

        self.set_status("Firmware update complete.")

        # Reload the instructions after a delay
        QTimer.singleShot(3000, self.load_file_text)

    # ---------- Test Functions ----------#

    def on_test_clicked(self) -> None:
        """Called when the test button is clicked."""
        if not self.get_selected_device():
            warning(self, "Please select a device.")
        elif self.state == State.IDLE:
            warning(self, f"USB device not connected.")
        elif self.testController and self.testController.state == TestState.AWAITING_BUTTON:
            self.testController.notify_button_pressed()
        elif self.testController and self.testController.is_busy:
            self._test_task.cancel()  # Cancel the test if its running
            self.append_text("<br><p>Test cancelled.</p>")
        else:
            if self.testController is None:
                self.testController = TestController(self.arduino, parent=self)
            self._test_task = asyncio.create_task(self.testController.async_run_test(self.get_selected_device()))

    def _on_message_received(self, message: ControllerMessage) -> None:
        """Called when a message is received from the test controller."""
        if message.type in (MessageType.ERROR, MessageType.WARNING, MessageType.INFO):
            log.debug(f"{message.type}: {message.data}")
        elif message.type == MessageType.TEST_ERROR:
            log.error(f"Test Error: {message.data}")
        elif message.type == MessageType.WAITING_FOR_BUTTON:
            log.debug(f"Waiting for button press...")
            self.state = State.WAITING_FOR_BUTTON
        elif message.type == MessageType.TEST_STARTED:
            log.debug(f"Test started: {message.data}")
            self.text_edit.setText("")
            self.state = State.TESTING
        elif message.type == MessageType.TEST_FINISHED:
            log.debug(f"Test finished: {message.data}")
            self.state = State.CONNECTED
            QTimer.singleShot(1500, self.load_file_text)
            self.test_counter.increment()

        else:
            log.debug(f"{message.type}: {message.data}")



if __name__ == "__main__":

    app = QApplication(sys.argv)

    lock = QLockFile(QDir.temp().absoluteFilePath("app.lock"))
    if not lock.tryLock(100):
        critical(None, "Another instance of the application is already running.", "Application Already Running")
        sys.exit(1)

    settings = settings.get_instance()
 
    def verify_files(files: List[str]) -> bool:
        """
        Verify if the files exist in the current directory.
        :param files: List of file names to verify.
        """
        found = True
        print("checking for missing files…")
        for file in files:
            file_path = os.path.join('.', file)
            if not os.path.exists(file_path):
                print(f"File {file} does not exist.")
                found = False
        return found

    if not verify_files(constants.REQUIRED_FILES):
        print("Some files are missing. Extracting defaults from resources.")
        import util.config_resources_rc
        extract_zip_from_resources('.')

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow(app, settings)
    window.show()
    log.info("Application started.")
    with loop:
        loop.run_forever()
