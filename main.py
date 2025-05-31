
import os
import sys
from pathlib import Path

# Check if the script is running in a frozen state (e.g., PyInstaller)
# and redirect stdout/stderr to a log file if so.
if getattr(sys, "frozen", False) and sys.stdout is None:
    log_path = Path.cwd() / "stdout.log"
    sys.stdout = sys.stderr = open(log_path, "w", buffering=1, encoding="utf-8", errors="backslashreplace")


from qtpy import (
    QtCore,
    QtGui,
)
from qtpy.QtGui import (
    QFont,
    QFontInfo,
    QIcon,
    QMovie,
    QCursor,
    QAction,
    QKeyEvent,
)
from qtpy.QtCore import (
    QTimer,
    QEvent,
    Qt,
    QSize,
    QProcess,
    QSize,
    QByteArray,
    QObject,
    Signal,
    Slot,
    QLockFile,
    QDir,
)
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QWidget,
    QInputDialog,
)

# import util.config_resources_rc
import icons_rc
from ui import Ui_MainWindow, Ui_ManualControlDialog
from imports import (
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
from config_loader import get_instance as get_config
from arduino import AIODevice
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
from imports import critical
from status_widget import CustomStatusBar
from manual_widget import ManualWidget

from pathlib import Path
from PySide6.QtCore    import Qt
from PySide6.QtGui     import QPainter, QPixmap
from PySide6.QtWidgets import QTextEdit

class BackgroundTextEdit(QTextEdit):
    """
    QTextEdit with a single, non-tiled background image.

    Parameters
    ----------
    image_path : str | Path
        File (or resource) path to the bitmap.
    scaled : bool, default False
        If True the image is scaled to fit the viewport while
        preserving aspect ratio.  If False the original bitmap
        is drawn at 1:1 pixels and centred.
    parent : QWidget | None
    """
    def __init__(self, image_path: str | Path, *, scaled: bool = False, parent=None):
        super().__init__(parent)
        self._pixmap = QPixmap(str(image_path))
        self._scaled  = bool(scaled)

        # QTextEdit’s own auto-repeat is irrelevant now, but keep a
        # transparent viewport so our painting shows through.
        self.viewport().setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)

    # ------------------------------------------------------------------ public
    def setBackgroundImage(self, image_path: str | Path, *, scaled: bool | None = None) -> None:
        """Change the bitmap (and optionally the scaling flag) at runtime."""
        self._pixmap = QPixmap(str(image_path))
        if scaled is not None:
            self._scaled = bool(scaled)
        self.viewport().update()

    # ------------------------------------------------------------- paintEvent
    def paintEvent(self, event):
        # 1.  Paint the background once.
        if not self._pixmap.isNull():
            p = QPainter(self.viewport())

            if self._scaled:
                img = self._pixmap.scaled(
                    self.viewport().size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            else:
                img = self._pixmap

            x = (self.viewport().width()  - img.width())  // 2
            y = (self.viewport().height() - img.height()) // 2
            p.drawPixmap(x, y, img)

        # 2.  Let QTextEdit render its contents on top.
        super().paintEvent(event)




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

    def __init__(self, app, settings=None) -> None:
        super(MainWindow, self).__init__()
        QtCore.qWarning("This is a test")
        self.setupUi(self)
        self.setWindowIcon(QIcon(constants.ICON_WINDOW))
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.show_movie()

        # Settings
        self.settings = settings.get_instance()
        self.settings_dialog = SettingsDialog(self)

        # Restore the window geometry and state
        self.restoreGeometry(self.settings.app_settings.value("mainwindow/geometry", QByteArray()))
        self.restoreState(self.settings.app_settings.value("mainwindow/windowState", QByteArray()))

        # log.debug(f"Settings: {self.settings.app_settings.allKeys()}")

        if self.settings.app_settings.value(constants.KEY_FULLSCREEN, type=bool):
            self.showFullScreen()
        else:
            self.showNormal()
        self.actionFullscreen.triggered.connect(self.toggleFullScreen)
        self.actionFullscreen.setChecked(
            self.settings.app_settings.value(constants.KEY_FULLSCREEN, type=bool)
        )

        if self.settings.get_bool(constants.KEY_FRAMELESS):
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # Process for updating the firmware
        self.update_process = FirmwareUpdateProcess(self)
        self.update_process.outputReceived.connect(lambda data: self.append_text(data, prepend=""))
        self.update_process.finishedWithCode.connect(self.on_finished)

        self.program_process: QProcess | None = None

        # self.device_changed.connect(self.on_device_changed)

        # Quick Connection Menu
        self.connect_menu = QAction(self)
        self.menuBar().addAction(self.connect_menu)
        self.connect_menu.triggered.connect(lambda: asyncio.create_task(self.connect_task()))

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
                self.settings.get(constants.KEY_FONT_FAMILY),
                self.settings.get_int(constants.KEY_FONT_SIZE),
            )
        )
        # self.text_edit.setStyleSheet(
        #     f"color:{self.settings.get(constants.KEY_FOREGROUND_COLOR)};" f"background-color:{self.settings.get(constants.KEY_BACKGROUND_COLOR)};"
        # )

        # Connect the menu items
        self.actionExplore_Directory.triggered.connect(
            lambda: subprocess.Popen(f"explorer {os.getcwd()}")
        )
        self.actionUpdate_Firmware.triggered.connect(self.update_firmware)
        self.actionConnect.triggered.connect(lambda: asyncio.create_task(self.connect_task()))
        self.actionAbout.triggered.connect(lambda: QApplication.aboutQt())
        self.actionChip_Select.triggered.connect(self.get_chip_part)
        self.actionShow_Logs.triggered.connect(self.show_log)
        self.actionChange_font.triggered.connect(self.choose_font)
        self.actionManual_Control.triggered.connect(self.control_manually)
        self.actionModify_Settings.triggered.connect(lambda: self.settings_dialog.show())
        self.actionHelp.triggered.connect(self.show_help)
        self.actionStatisitics.triggered.connect(self.show_statistics)
        self.actionDark_Theme.triggered.connect(self.toggle_theme)
        self.actionScreenshot.triggered.connect(take_screenshot)
        self.program_button.clicked.connect(self.program)
        self.test_button.clicked.connect(self.on_test_clicked)
        self.actionOpen_UP_exe.triggered.connect(
            lambda: QProcess.startDetached(cfg.get_instance().get_programmer_path())
        )

        # Set the theme
        self.set_theme(get_theme(self.settings))

        # Remove the default actions from the device menu
        self.menuDevice.clear()

        # Load the devices from the config file and add each device to the menu
        for device in load_devices():
            action = QAction(device._device_name, self)
            action.setFont(self.font())
            action.setCheckable(True)
            action.setData(device)  # Store the device object in the action
            self.set_icon(action, 'radio-off-button')
            action.triggered.connect(self.deviceSelect)
            self.menuDevice.addAction(action)

        self.load_file_text()
        self.text_edit.cursorPositionChanged.connect(self.check_for_link)

        self.eax_device = Device()

        # Set the default device
        # if not self.eax_device.verify_firmware():
        #     self.insert_text("Missing firmware!")

        self.setStatusBar(CustomStatusBar())
        self.set_status('Select a device to begin.')

        # If auto connect is enabled, try to connect to the USB device
        if self.settings.get(constants.KEY_AUTO_CONNECT):
            QTimer.singleShot(1200, lambda: asyncio.create_task(self.connect_task()))

        # btextedit = BackgroundTextEdit(image_path=':/cloud)', scaled=True)
        # self.verticalLayout.replaceWidget(self.text_edit, btextedit)
        # self.text_edit = btextedit

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
        log.debug(f"Previous state: {self._state}, New State: {value}", 1)
        if value == State.CONNECTING:
            self.actionConnect.setEnabled(False)
            # self.label_usb_icon.setText(constants.ICON_USB_YELLOW)
            self.set_status("Connecting to USB device...")
            self.usb_label.setText("USB connecting...")
            self.usb_label.setStyleSheet(
                cfg.get_instance().get('window').get('usb_label').get('connecting_style')
            )
            self.show_movie(pause=False)
        elif value == State.CONNECTED:
            self.controlBox.setEnabled(True)
            self.usb_label.setStyleSheet(
                cfg.get_instance().get('window').get('usb_label').get('connected_style')
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
                    cfg.get_instance().get('window').get('usb_label').get('disconnected_style')
                )
                self.usb_label.setText(
                    cfg.get_instance()
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
            self.controlBox.setEnabled(False)
            self.actionConnect.setEnabled(False)
            self.set_status("Testing...")
        elif value == State.WAITING_FOR_BUTTON:
            self.controlBox.setEnabled(True)
            self.actionConnect.setEnabled(False)
            self.set_status("Waiting for input...")

        self._state = value

    def check_for_link(self) -> None:
        """Check if the cursor is over a link."""
        cursor = self.text_edit.textCursor()
        current_position = cursor.position()
        anchor = self.text_edit.anchorAt(self.text_edit.mapFromGlobal(QCursor.pos()))
        if anchor:
            # print(anchor)

            if anchor == "continue":
                if self.testController and self.testController.state == TestState.AWAITING_BUTTON:
                    self.testController.notify_button_pressed()
                    return

            else:
                # reset the position to avoid cursor moving to the link start
                cursor.setPosition(current_position)
                self.text_edit.setTextCursor(cursor)
                self.help_dialog = HelpDialog()
                self.help_dialog.show()

    def set_theme(self, theme: str) -> None:
        """Set the theme."""
        log.info(f"Setting theme to {theme}")
        if theme == 'dark':
            # style = qdarkstyle.load_stylesheet(qt_api='pyside2')
            style = qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette)
            self.actionDark_Theme.setChecked(True)
        else:
            style = qdarkstyle.load_stylesheet(palette=qdarkstyle.LightPalette)
            self.actionDark_Theme.setChecked(False)
        # self.setStyleSheet(style)

        self.set_icon(self.connect_menu, 'usb2')
        self.set_icon(self.test_button, 'test-button')
        self.set_icon(self.program_button, 'prog-button')

        # for action in self.menuDevice.actions():
        #     if action.text() == self.eax_device.name:
        #         self.set_icon(action, 'radio-on-button')
        #     else:
        #         self.set_icon(action, 'radio-off-button')

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
        log.info("Toggle theme")
        if self.settings.get_bool(constants.KEY_DARK_THEME):
            self.settings.app_settings.setValue(constants.KEY_DARK_THEME, False)
            self.set_theme('light')
            self.actionDark_Theme.setChecked(False)
        else:
            self.settings.app_settings.setValue(constants.KEY_DARK_THEME, True)
            self.set_theme('dark')
            self.actionDark_Theme.setChecked(True)

    def set_icon(self, widget: QObject, icon_name: str, ext='png') -> None:
        if get_theme(self.settings) == 'dark':
            icon_path = f":/images/icons/light/{icon_name}.{ext}"
        else:
            icon_path = f":/images/icons/dark/{icon_name}.{ext}"
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
            self.show_help()
        elif key == Qt.Key.Key_F5:
            self.settings_dialog.show()
        elif key == Qt.Key.Key_F6:
            self.toggle_theme()
        elif key == Qt.Key.Key_Question:
            self.show_help()
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
            print(self.text_edit.toHtml())
            # print(self.label_usb_icon.size())
            # print(self.arduino)
            # print(settings.get_instance())
            # print(self.settings)
            # self.statusBar().set_value(59999)
            # self.menuBar().setEnabled(not self.menuBar().isEnabled())

    def show_movie(self, pause: bool = False) -> None:
        """Show or hide the GIF in the USB icon label."""
        if self.label_usb_icon.movie() is None:
            movie = QMovie(":/resources/images/icons/infinity-16570.gif")
            movie.setScaledSize(self.label_usb_icon.size())
            movie.setSpeed(200)
            self.label_usb_icon.setMovie(movie)
        self.label_usb_icon.movie().setPaused(pause)

    def is_movie_running(self) -> bool:
        """Check if the movie in the USB icon label is running."""
        if self.label_usb_icon.movie() is not None:
            return self.label_usb_icon.movie().state() == QMovie.Running
        return False

    def get_selected_device(self) -> Device:
        """Get the currently selected device from the menu."""
        for action in self.menuDevice.actions():
            if action.isChecked():
                return action.data()
        return None

    def deviceSelect(self) -> None:
        """Called when a device is selected from the menu."""

        # Uncheck all other actions
        for action in self.menuDevice.actions():
            if action != self.sender():
                action.setChecked(False)
                self.set_icon(action, 'radio-off-button')

        # Set the icon
        self.set_icon(self.sender(), 'radio-on-button')

        device: Device = self.sender().data()

        log.info(f"Device changed to: {device.styles}")
        self.device_label.setText(
            f'''<html><head/><body><p><span style="{device.styles}">Device: {device.name}</span> </p></body></html>'''
        )
        # self.device_label.setStyleSheet(f"color: {device.label_color}; {device.font_size};")

    def show_help(self) -> None:
        self.help_dialog = HelpDialog()
        self.help_dialog.show()

    def choose_font(self) -> None:
        old_font = self.text_edit.font()

        (ok, font) = get_font(old_font)

        if ok:
            log.debug(f"User selected font: {font.toString()}")
            self.text_edit.setFont(font)
            self.settings.setValue(constants.KEY_FONT_FAMILY, QFontInfo(font).family())
            self.settings.setValue(constants.KEY_FONT_FAMILY, QFontInfo(font).family())
            self.settings.setValue(constants.KEY_FONT_SIZE, font.pointSize())
            self.settings.setValue(constants.KEY_FONT_SIZE, font.pointSize())

    def get_chip_part(self) -> None:
        current_chip = self.settings.get(constants.KEY_CHIP_PART)
        current_selection = constants.CHIP_OPTIONS.index(current_chip)
        item, okPressed = QInputDialog.getItem(
            self, "Select Chip", "Chip:", constants.CHIP_OPTIONS, current_selection, False
        )
        if okPressed and item:
            self.settings_dialog.comboBox_chip.setCurrentText(item)  # update the combo box
            self.settings.setValue(constants.KEY_CHIP_PART, item)
            log.debug(f"saved chip settings: {item}")

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Event filter to handle inactivity timeout."""
        if event.type() in (QEvent.MouseMove, QEvent.KeyPress):
            self.inactivityTimer.start(
                self.settings.get_int(constants.KEY_INACTIVITY_TIMEOUT, 10) * 60 * 1000
            )
        return super(MainWindow, self).eventFilter(watched, event)

    def handle_inactivity_timeout(self) -> None:
        """Called when the inactivity timer times out."""
        log.debug("Inactivity timeout.")
        self.device_label.setText("")  # clear the device label
        # reset the device
        for action in self.menuDevice.actions():
            action.setChecked(False)
            self.set_icon(action, 'radio-off-button')

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
        elif self.state is not State.IDLE:
            return
        else:
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
            self.usb_label.setText(cfg.get_instance().get('window').get('usb_label').get('connected_text').format(msg=message))

        else:
            self.usb_label.setText(cfg.get_instance().get('window').get('usb_label').get('disconnected_text').format(msg="disconnected"))
            self.usb_label.setStyleSheet(cfg.get_instance().get('window').get('usb_label').get('disconnected_style'))
            log.error(f"USB: connection lost. Error: {message}")
            self.append_text(f"\n<p>USB Error: {message}</p>")
            self.actionConnect.setText("Connect")
            self.state = State.IDLE

    async def disconnect_device(self):
        # Await the asynchronous disconnect on your device.
        self.usb_label.setText(cfg.get_instance().get('window').get('usb_label').get('text').format(msg="disconnected"))
        self.usb_label.setStyleSheet(cfg.get_instance().get('window').get('usb_label').get('disconnected_style'))
        self.actionConnect.setText("Connect")
        if self.arduino:
            self.arduino.connection_changed.disconnect(self.on_connection_changed)
            await self.arduino.async_disconnect()
            self.arduino = None  # clear the reference to the device
        self.state = State.IDLE
        log.info("Device disconnected successfully.")

    def _connect_controller_signals(self) -> None:
        """Connect the signals from the test controller to the main window."""
        self.testController.updateText.connect(self.append_text)
        self.testController.sendMessage.connect(self._on_message_received)

    def control_manually(self) -> None:
        ManualWidget(self.arduino).show()

    # ----- Programming Functions ----- #

    def program(self) -> None:
        """Program the selected device with the firmware."""
        if not self.get_selected_device():
            warning(self, "Please select a device.")
            return

        if self.state not in (State.IDLE, State.CONNECTED):
            return

        fw = self.get_selected_device().firmware_path
        if not os.path.exists(fw):
            self.append_text(f"{fw} not found!")
            return

        try:

            argv = cfg.get_instance().generate_program_arguments(settings=self.settings, device=self.get_selected_device())

            log.info(f"Programming {self.get_selected_device().name}, args: {argv}")

            # create (or reuse) a QProcess
            self.program_process = QProcess(self)

            # when it finishes, grab only the exit code
            previous_state = self.state
            self.program_process.finished.connect(lambda code, _: self.handle_programming_result(code, previous_state))
            self.state = State.PROGRAMMING

            # start it
            self.program_process.setProgram(argv[0])
            self.program_process.setArguments(argv[1:])
            self.program_process.start()
        except Exception as e:
            self.append_text(f'<br><p>"Exception during programming: {e}</p>')
            log.exception(f"Exception during programming: {e}")
            self.state = State.IDLE

    @Slot(int, QProcess.ExitStatus)
    def handle_programming_result(self, returncode: int, previous_state: State) -> None:
        """Called when QProcess emits finished()."""
        self.state = previous_state  # restore the previous state
        if returncode == 0:
            self.append_text("<br><p>Programming successful.</p>")
            log.info(f"Programming successful for {self.get_selected_device().name}.")
            if self.settings.get(constants.KEY_AUTO_TEST) and self.arduino.device_connected:
                self.test_button.click()
                return
        else:
            self.append_text(f"<br><p>Programming failed. Return code: {returncode}</p>")
            log.error(f"Programming failed for {self.get_selected_device().name}. Return code: {returncode}")

    def show_statistics(self) -> None:
        """Display the statistics of the programming results."""
        failed = len(log.search_logs("failed", "handle_programming_result"))
        success = len(log.search_logs("success", "handle_programming_result"))
        QMessageBox().information(self, "Statistics", f"Failures: {failed}\n" f"Successes: {success}\n")

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

    def increment_counter(self) -> None:
        """Set the progress value in the status bar."""
        if self.settings.get_bool(constants.KEY_COUNTER_ENABLED, False):
            self.settings.setValue(constants.KEY_TEST_COUNT, self.settings.get_int(constants.KEY_TEST_COUNT) + 1)
        sb = self.statusBar()
        sb.update_counter()
        log.increment_tests_run(self.get_selected_device().name)

    # ---------- Test Functions ----------#

    def on_test_clicked(self) -> None:
        """Called when the test button is clicked."""
        if not self.get_selected_device():
            warning(self, "Please select a device.")
        elif self.state == State.IDLE:
            warning(self, f"USB device not connected.")
        elif self.testController and self.testController.state == TestState.AWAITING_BUTTON:
            self.testController.notify_button_pressed()
            return
        elif self.testController and self.testController.is_busy:
            return
        else:
            if self.testController is None:
                self.testController = TestController(self.arduino, parent=self)
            self.text_edit.setText("")
            asyncio.create_task(self.testController.async_run_test(self.get_selected_device()))

    def _on_message_received(self, message: ControllerMessage) -> None:
        """Called when a message is received from the test controller."""
        if message.type in (MessageType.ERROR, MessageType.WARNING, MessageType.INFO):
            print(f"{message.type}: {message.data}")
        elif message.type == MessageType.TEST_ERROR:
            print(f"Test Error: {message.data}")
        elif message.type == MessageType.WAITING_FOR_BUTTON:
            print(f"Waiting for button press...")
            self.state = State.WAITING_FOR_BUTTON
        elif message.type == MessageType.TEST_STARTED:
            print(f"Test started: {message.data}")
            self.state = State.TESTING
        elif message.type == MessageType.TEST_FINISHED:
            print(f"Test finished: {message.data}")
            self.state = State.CONNECTED
            QTimer.singleShot(1500, self.load_file_text)
            self.increment_counter()

        else:
            print(f"{message.type}: {message.data}")


class FirmwareUpdateProcess(QProcess):
    """Process to update the firmware."""

    # emit decoded stdout whenever new data arrives
    outputReceived = Signal(str)
    # emit exit code when finished
    finishedWithCode = Signal(int, QProcess.ExitStatus, bool)

    def __init__(self, parent: MainWindow = None):
        super().__init__(parent)
        self.parent: MainWindow = parent
        self.setWorkingDirectory(os.getcwd())
        self.errorOccurred.connect(self._on_error)
        self.finished.connect(self._on_finished)
        self.readyReadStandardOutput.connect(self._read_standard_output)
        self.readyReadStandardError.connect(self._read_standard_error)
        self.device_connected = False

    @Slot()
    def _read_standard_output(self):
        """Read the standard output of the process."""
        output = self.readAllStandardOutput().data().decode()
        self.outputReceived.emit(output)

    @Slot()
    def _read_standard_error(self):
        """Read the standard error of the process."""
        error = self.readAllStandardError().data().decode()
        self.outputReceived.emit(error)

    @Slot(int, QProcess.ExitStatus)
    def _on_finished(self, exit_code, exit_status):
        self.finishedWithCode.emit(exit_code, exit_status, self.device_connected)

    @Slot(QProcess.ProcessError)
    def _on_error(self, error: QProcess.ProcessError):
        self.parent.on_error(error)
        self.finishedWithCode.emit(-1, QProcess.ExitStatus.NormalExit, self.device_connected)

    def run(self, program: str, args: list[str] = None):
        """Convenience method to start a process."""
        self.setProgram(program)
        self.setArguments(args or [])
        self.start()


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

    if not verify_files(
        [
            "instructions.md",
            "Scripts/Upload.ps1",
            "Scripts/UpdateFirmware.ps1",
            "sketches/Telemetrix4Arduino/build/arduino.avr.uno/Telemetrix4Arduino.ino.hex",
            "sketches/StandardFirmata/build/arduino.avr.uno/StandardFirmata.ino.hex",
            "firmware/EAX300_59.hex",
            "firmware/EAX500_591.hex",
            "firmware/EAX505_591.hex",
            "firmware/EAX525_591.hex",
        ]
    ):
        print("Some files are missing. Extracting defaults from resources.")
        import util.config_resources_rc

        extract_zip_from_resources('.')

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow(app, settings)
    window.setWindowTitle(f"{constants.APP_NAME} v{constants.APP_VERSION}")
    window.show()
    log.info("Application started.")
    with loop:
        loop.run_forever()
