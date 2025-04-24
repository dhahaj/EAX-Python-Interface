from re import A
from qtpy import (
    QtCore,
    QtGui,
)
from qtpy.QtGui import (
    QFont,
    QFontInfo,
    QColor,
    QIcon,
    QMovie,
    QCursor,
    QAction,
    QKeyEvent,
    QShowEvent,
)
from qtpy.QtCore import (
    QTimer,
    QEvent,
    Qt,
    QSize,
    QProcess,
    Signal,
    QSize,
    QByteArray,
    QSystemSemaphore,
    QSharedMemory,
    QObject,
    QThread,
    Signal,
    QFile,
    QIODevice,
)
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QColorDialog,
    QWidget,
    QInputDialog,
    QTableWidgetItem,
    QDialog,
    QLabel,
    QStatusBar,
)
from ui import (
    Ui_MainWindow,
    Ui_HelpDialog,
    Ui_LogView,
    Ui_Settings,
    Ui_ManualControlDialog,
    Ui_ProgressBar,
    Ui_StatusBarWidget
)
from imports import (
    get_stylesheet,
    get_theme,
    get_font,
    take_screenshot,
    clean_backups,
    error,
    info,
    warning,
    debug,

)
from loguru import logger as log
import sys
import subprocess
import qdarkstyle
from math import ceil
from arduino import AIODevice
from config_loader import ConfigLoader
from rich import print
import asyncio
from qasync import QEventLoop
import io
import zipfile
import os
from pathlib import Path
from typing import List, Dict, Tuple, Any
import constants
from constants import State
from settings import ApplicationSettings
from device import Device
import applogger


class LogView(QWidget, Ui_LogView):
    """
    A widget for displaying logs entries. 

    :param data: The log data to be displayed, expected as a list of dict objects.
    :param callback: Optional callback function to be called when the dialog is closed and entries have been removed.
    :param *args: Optional additional arguments.
    """

    def __init__(self, data, callback=None, *args):
        super().__init__()
        self.setupUi(self)
        self.load_data(data)
        self.tableWidget.itemChanged.connect(self.on_item_changed)
        self.data = data
        self.callback = callback
        self.data_changed = False

        self.settings = ApplicationSettings()
        self.app_settings = self.settings.app_settings
        self.restoreGeometry(self.app_settings.value("logwindow/geometry", QByteArray()))
        self.setStyleSheet(get_stylesheet(self.settings))

    def on_item_changed(self, item) -> None:
        row, col = item.row(), item.column()

        row_data = [self.tableWidget.item(row, column).text(
        ) for column in range(self.tableWidget.columnCount())]
        print(f"Row {row_data}")
        new_value = item.text()
        original_data = self.data[row]

        print(f"Original data: {original_data}")
        print(
            f"Data at row {row}, column {col} has been changed to: {new_value}")

        if col == 1:
            logg.update_log(row_data[0], timestamp=new_value)
        elif col == 2:
            logg.update_log(row_data[0], level=new_value)
        elif col == 3:
            logg.update_log(row_data[0], message=new_value)

    def delete_selected_rows(self) -> None:
        """Deletes the currently selected rows from the table."""
        selected_rows = set(index.row()
                            for index in self.tableWidget.selectedIndexes())
        self.data_changed = True
        for row in sorted(selected_rows, reverse=True):
            self.tableWidget.removeRow(row)

    def load_data(self, data) -> None:
        horHeaders = ["id", "timestamp", "level", "message"]
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setHorizontalHeaderLabels(horHeaders)

        for i in range(len(data)):
            timestamp = QTableWidgetItem(data[i].get("timestamp"))
            level = QTableWidgetItem(data[i].get("level"))
            message = QTableWidgetItem(data[i].get("message"))
            id = QTableWidgetItem(str(data[i].get("id")))
            self.tableWidget.setItem(i, 0, id)
            self.tableWidget.setItem(i, 1, timestamp)
            self.tableWidget.setItem(i, 2, level)
            self.tableWidget.setItem(i, 3, message)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def closeEvent(self, event) -> None:
        self.app_settings.setValue("logwindow/geometry", self.saveGeometry())
        if self.data_changed and self.callback is not None:
            self.callback(self.extract_data())
        self.deleteLater()
        event.accept()

    def keyPressEvent(self, event) -> None:
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_F2:
            take_screenshot()
        elif key == Qt.Key_Delete:
            self.delete_selected_rows()
        super().keyPressEvent(event)

    def extract_data(self) -> List[Dict[str, str]]:
        """Extracts data from the table and returns as a list of dictionaries."""
        # progress = QProgressBar(self)
        # progress.setRange(0, self.tableWidget.rowCount())
        # progress.setWindowModality(Qt.WindowModal)
        # progress.setWindowTitle("Saving data...")
        # progress.show()

        data = []
        for i in range(self.tableWidget.rowCount()):
            timestamp = self.tableWidget.item(i, 1).text()
            level = self.tableWidget.item(i, 2).text()
            message = self.tableWidget.item(i, 3).text()
            data.append({"timestamp": timestamp,
                        "level": level, "message": message})
        return data


class HelpDialog(QDialog, Ui_HelpDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.settings = ApplicationSettings()
        self.app_settings = self.settings.app_settings
        self.restoreGeometry(self.app_settings.value("helpwindow/geometry", QByteArray()))
        # self.toolBox.currentChanged.connect(self.on_tab_clicked)
        self.label.installEventFilter(self)
        self.label_2.installEventFilter(self)
        self.label_3.installEventFilter(self)
        self.setStyleSheet(get_stylesheet(self.settings))

    def eventFilter(self, obj: QLabel, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            if obj == self.label:
                obj.setMovie(QMovie(":/resources/firmware_update.gif"))
            elif obj == self.label_2:
                obj.setMovie(QMovie(":/resources/testing.gif"))
            elif obj == self.label_3:
                obj.setMovie(QMovie(":/resources/setting.gif"))
            obj.movie().setScaledSize(QSize(750, 750))
            obj.movie().setSpeed(180)
            obj.movie().start()
            event.accept()
        return super().eventFilter(obj, event)

    def closeEvent(self, event: QEvent) -> None:
        self.app_settings.setValue("helpwindow/geometry", self.saveGeometry())
        self.deleteLater()
        event.accept()


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    This is the main application window. It contains the primary logic for controlling the application.

    :param QMainWindow: The main window.
    :type QMainWindow: QMainWindow
    :param Ui_MainWindow: The main window UI.
    :type Ui_MainWindow: Ui_MainWindow
    """
    device_changed = Signal(str)
    _state: State = State.IDLE
    connecting: bool = False
    log_view: LogView | None = None
    help_dialog: HelpDialog | None = None
    arduino: AIODevice | None = None
    eax_device: Device | None = None

    def __init__(self, app) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/resources/icons/images/icons/code.ico"))
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Settings
        self.settings: ApplicationSettings = ApplicationSettings('settings.ini')
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.saved.connect(self.on_settings_closed)

        # Restore the window geometry and state
        self.restoreGeometry(self.settings.app_settings.value("mainwindow/geometry", QByteArray()))
        self.restoreState(self.settings.app_settings.value("mainwindow/windowState", QByteArray()))

        print(f"Settings: {self.settings.app_settings.allKeys()}")

        if self.settings.app_settings.value(constants.KEY_FULLSCREEN, type=bool):
            self.showFullScreen()
        else:
            self.showNormal()
        self.actionFullscreen.setChecked(self.settings.app_settings.value(constants.KEY_FULLSCREEN, type=bool))
        self.actionFullscreen.triggered.connect(self.toggleFullScreen)

        if self.settings.get_bool(constants.KEY_FRAMELESS):
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # Process for updating the firmware
        self.update_process = QProcess(self)
        self.update_process.finished.connect(self.on_finished)
        self.update_process.errorOccurred.connect(self.on_error)
        self.update_process.readyReadStandardError.connect(self.read_standard_output)
        self.update_process.readyReadStandardOutput.connect(self.read_standard_output)
        self.update_process.setWorkingDirectory(os.getcwd())

        self.device_changed.connect(self.on_device_changed)

        # Quick Connection Menu
        self.connect_menu = ConnectMenu(self)
        self.menuBar().addAction(self.connect_menu)

        # Inactivity timer
        self.inactivityTimer = QTimer()
        self.inactivityTimer.setSingleShot(True)
        self.inactivityTimer.timeout.connect(self.handle_inactivity_timeout)
        self.installEventFilter(self)
        for widget in QApplication.instance().allWidgets():
            widget.installEventFilter(self)
        print(self.settings.get(constants.KEY_FONT_FAMILY))

        # Setup the text area
        self.text_edit.setFont(
            QFont(
                self.settings.get(constants.KEY_FONT_FAMILY),
                self.settings.get_int(constants.KEY_FONT_SIZE),
            )
        )
        self.text_edit.setStyleSheet(
            f"color:{self.settings.get(constants.KEY_FOREGROUND_COLOR)};"
            f"background-color:{self.settings.get(constants.KEY_BACKGROUND_COLOR)};"
        )

        # Connect the menu items
        self.actionExplore_Directory.triggered.connect(lambda: subprocess.Popen(f"explorer {os.getcwd()}"))
        self.actionUpdate_Firmware.triggered.connect(self.update_firmware)
        self.actionConnect.triggered.connect(self.connect_device)
        self.actionAbout.triggered.connect(self.aboutQt)
        self.actionChip_Select.triggered.connect(self.get_chip_part)
        self.actionShow_Logs.triggered.connect(self.show_log)
        self.actionChange_font.triggered.connect(self.choose_font)
        self.actionManual_Control.triggered.connect(self.control_manually)
        self.actionModify_Settings.triggered.connect(self.modify_settings)
        self.actionHelp.triggered.connect(self.show_help)
        self.actionStatisitics.triggered.connect(self.show_statistics)
        self.actionDark_Theme.triggered.connect(self.toggle_theme)
        self.actionScreenshot.triggered.connect(take_screenshot)
        self.program_button.clicked.connect(self.program)
        self.test_button.clicked.connect(self.on_test_clicked)

        # Remove the default actions from the device menu
        for action in self.menuDevice.actions():
            self.menuDevice.removeAction(action)

        # Load the devices from the config file and add them to the menu
        config = ConfigLoader()
        for device in config.devices:
            action = QAction(device, self)
            action.setFont(self.font())
            action.setCheckable(True)
            action.triggered.connect(self.deviceSelect)
            self.menuDevice.addAction(action)

        self.text_edit.cursorPositionChanged.connect(self.check_for_link)
        self.load_file_text()

        self.eax_device = Device()

        # Set the default device
        if not self.eax_device.verify_firmware():
            self.insert_text("Missing firmware!")
            log.critical("Missing firmware!")
            app_logger.critical("Missing firmware!")

        # Set the theme
        self.set_theme(get_theme(self.settings))

        print(logg.check_integrity())
        logg.backup_database()
        # db.backup_database()
        clean_backups("backups", 5)

        self.setStatusBar(CustomStatusBar())
        self.set_status('Select a device to begin.')

        # If auto login and auto connect are enabled, try to connect to the USB device
        if self.settings.get(constants.KEY_AUTO_CONNECT):
            QTimer.singleShot(2000, self.connect_device)

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
        log.debug(f"Setting state to {value}")
        self._state = value

        if value == State.CONNECTING:
            self.test_button.setEnabled(False)
            # self.program_button.setEnabled(False)
            self.actionConnect.setEnabled(False)
            self.label_usb_icon.setText(constants.ICON_USB_YELLOW)
            self.set_status("Connecting to USB device...")
        elif value == State.CONNECTED:
            self.test_button.setEnabled(True)
            self.program_button.setEnabled(True)
            self.actionConnect.setEnabled(True)
            self.label_usb_icon.setText(constants.ICON_USB_GREEN)
            self.set_status(f"Connected to {self.arduino.device.com_port}.")
        elif value == State.IDLE:
            self.test_button.setEnabled(False)
            self.program_button.setEnabled(True)
            self.actionConnect.setEnabled(True)
            self.label_usb_icon.setText(constants.ICON_USB_RED)
            self.set_status("Disconnected.")
        elif value == State.PROGRAMMING:
            self.test_button.setEnabled(False)
            self.program_button.setEnabled(False)
            self.actionConnect.setEnabled(False)
            self.set_status("Programming...")

    def focusOutEvent(self, event) -> None:
        super().focusOutEvent(event)

    def focusInEvent(self, event) -> None:
        # Close the settings dialog if the user clicks outside of it
        if event.reason() == Qt.FocusReason.ActiveWindowFocusReason:
            if self.settings_dialog.isVisible():
                self.settings_dialog.close()
        super().focusInEvent(event)

    def check_for_link(self) -> None:
        """Check if the cursor is over a link."""
        cursor = self.text_edit.textCursor()
        current_position = cursor.position()
        anchor = self.text_edit.anchorAt(self.text_edit.mapFromGlobal(QCursor.pos()))
        if anchor:
            print(anchor)
            # debug(current_position)
            # QDesktopServices.openUrl(QUrl(anchor))
            # reset the position to avoid cursor moving to the link start
            cursor.setPosition(current_position)
            self.text_edit.setTextCursor(cursor)
            self.help_dialog = HelpDialog()
            self.help_dialog.show()

    def set_theme(self, theme: str) -> None:
        """Set the theme."""
        log.info(f"Setting theme to {theme}")
        if theme == 'dark':
            style = qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette)
            self.actionDark_Theme.setChecked(True)
        else:
            style = qdarkstyle.load_stylesheet(palette=qdarkstyle.LightPalette)
            self.actionDark_Theme.setChecked(False)
        self.setStyleSheet(style)

        self.set_icon(self.connect_menu, 'usb2')
        self.set_icon(self.test_button, 'test-button')
        self.set_icon(self.program_button, 'prog-button')

        for action in self.menuDevice.actions():
            if action.text() == self.eax_device.name:
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
        self.set_icon(self.actionModify_Settings, 'settings', 'ico')
        # self.set_icon(self.actionAdd_User, 'follow')
        # self.set_icon(self.actionRemove_User, 'remove-user')
        self.set_icon(self.actionHelp, 'help')
        self.set_icon(self.actionStatisitics, 'bar-chart')
        # self.set_icon(self.actionLogout, 'logout')

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
            icon_path = f":/resources/icons/images/icons/light/{icon_name}.{ext}"
        else:
            icon_path = f":/resources/icons/images/icons/dark/{icon_name}.{ext}"
        icon = QIcon()
        icon.addFile(
            icon_path,
            QSize(),
            QIcon.Normal,
            QIcon.On,
        )
        widget.setIcon(icon)

    def toggleFullScreen(self) -> bool:
        if self.settings.app_settings.value(constants.KEY_FULLSCREEN, defaultValue=False) == "false":
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
            self.aboutQt()
        elif key == Qt.Key.Key_Q and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            asyncio.get_event_loop().stop()
            self.close()
        elif key == Qt.Key.Key_F2:
            take_screenshot()
        elif key == Qt.Key.Key_F3:
            self.control_manually()
        elif key == Qt.Key.Key_F4:
            self.actionConnect.trigger()
        elif key == Qt.Key.Key_E and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            logg.export_logs()
        elif key == Qt.Key.Key_R and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            is_frameless = self.windowFlags() & Qt.FramelessWindowHint
            # Toggle between frameless and regular states
            if is_frameless:
                self.setWindowFlags(self.windowFlags() & ~
                                    Qt.FramelessWindowHint)
                self.settings.setValue(constants.KEY_FRAMELESS, False)
            else:
                self.setWindowFlags(self.windowFlags() |
                                    Qt.FramelessWindowHint)
                self.settings.setValue(constants.KEY_FRAMELESS, True)
            QTimer.singleShot(10, self.show)
        # elif key == Qt.Key.Key_1 and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # log.warning(f"State: {self.state}")
        # elif (
        #     key == Qt.Key.Key_2 and
        #     event.modifiers() & Qt.KeyboardModifier.ControlModifier
        # ):
            log.warning(f"Device: {self.eax_device.name}")
        elif key == Qt.Key.Key_A and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # print(vars(self))
            # print(vars(self.settings))
            # print(vars(app_logger))
            # print(vars(self.arduino))
            # print(vars(db))
            # print(vars(logg))
            self.text_edit.setAcceptRichText(True)
            self.load_file_text()
            print(self.arduino)

    def on_device_changed(self, device: str) -> None:
        """ Called when the device is changed. """
        log.info(f"Device changed: {device}")
        self.device_label.setText(f"Device: {device}")
        self.eax_device.name = device

        # Set the color of the device label
        if self.eax_device.name == "EAX300":
            self.device_label.setStyleSheet(constants.YELLOW)
        elif self.eax_device.name == "EAX500":
            self.device_label.setStyleSheet(constants.GREEN)
        else:
            self.device_label.setStyleSheet(constants.ORANGE)

    def deviceSelect(self) -> None:
        """ Called when a device is selected from the menu. """
        self.sender().setChecked(False)

        # Uncheck all other actions
        for action in self.menuDevice.actions():
            if action.text() != self.sender().text():
                # action.setIcon(icon)
                self.set_icon(action, 'radio-off-button')

        # Uncheck the device label if the same action is clicked
        if self.eax_device.name == self.sender().text():
            self.device_label.setStyleSheet(constants.DEVICE_LABEL)
            self.device_label.setText("")
            self.eax_device.name = None
            # self.sender().setIcon(icon)
            self.set_icon(self.sender(), 'radio-off-button')
            return

        # Set the theme
        self.set_icon(self.sender(), 'radio-on-button')

        # Signal the device changed
        self.device_changed.emit(self.sender().text())

    def show_help(self) -> None:
        try:
            self.help_dialog.show()
        except:
            self.help_dialog = HelpDialog()
            self.help_dialog.show()

    def choose_font(self) -> None:
        old_font = self.text_edit.font()

        (ok, font) = get_font(old_font)

        if ok:
            debug(f"User selected font: {font.toString()}")
            self.text_edit.setFont(font)
            self.settings.setValue(constants.KEY_FONT_FAMILY, QFontInfo(font).family())
            self.settings.setValue(constants.KEY_FONT_FAMILY, QFontInfo(font).family())
            self.settings.setValue(constants.KEY_FONT_SIZE, font.pointSize())
            self.settings.setValue(constants.KEY_FONT_SIZE, font.pointSize())

    def get_chip_part(self) -> None:
        current_chip = self.settings.get(constants.KEY_CHIP_PART)
        current_selection = constants.CHIP_OPTIONS.index(current_chip)
        item, okPressed = QInputDialog.getItem(
            self, "Get item", "Chip Select:", constants.CHIP_OPTIONS, current_selection, False
        )
        if okPressed and item:
            self.settings_dialog.comboBox_chip.setCurrentText(item)  # update the combo box
            self.settings.setValue(constants.KEY_CHIP_PART, item)
            self.settings.app_settings.setValue(constants.KEY_CHIP_PART, item)
            log.debug(f"saved chip settings: {item}")

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        # Handle mouse clicks on the scroll area
        # if watched.objectName() == "qt_scrollarea_viewport":
        #     if event.type() == QEvent.MouseButtonPress:
        #         if event.button() == Qt.LeftButton:
        #             log.info("Left mouse button clicked!")
        #             if self.settings.get_bool(constants.KEY_TOUCHSCREEN_ENABLED):
        #                 self.test_button.click()
        #                 return True  # event was handled

        # Reset the inactivity timer if a mouse movement or key press event is detected
        if event.type() in (QEvent.MouseMove, QEvent.KeyPress):
            self.inactivityTimer.start(
                self.settings.get_int(constants.KEY_INACTIVITY_TIMEOUT, 10) * 60 * 1000
            )  # 60 seconds of inactivity before timeout
        return super(MainWindow, self).eventFilter(watched, event)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.activateWindow()
        self.setFocus()

    def _pass(self):
        """Dummy function."""
        pass

    def handle_inactivity_timeout(self) -> None:
        """ Called when the inactivity timer times out. """
        debug("Inactivity timeout.")

        icon = QIcon()
        icon.addFile(constants.RADIO_OFF_ICON, QSize(), QIcon.Normal, QIcon.On)
        # Uncheck all menu actions
        [action.setIcon(icon) for action in self.menuDevice.actions()]
        self.device_label.setText("")  # clear the device label
        self.eax_device.name = None  # reset the device

    def insert_text(self, text: str) -> None:
        """Add text to the text console."""
        self.text_edit.append("\n" + text)
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.ensureCursorVisible()

    def load_file_text(self, filename="instructions.md") -> None:
        """Load text from a file and add it to the text area"""

        self.text_edit.setMarkdown(Path(filename).read_text() + "\n")
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.ensureCursorVisible()

        # with open(filename, "r") as f:
        #     self.text_edit.setMarkdown(f.read() + "\n")

    def aboutQt(self) -> None:
        QApplication.aboutQt()

    ''' Connection Functions '''

    async def connect_task(self) -> None:
        """Setup the USB device."""
        self.arduino = AIODevice(
            wait=self.settings.get(constants.KEY_ARDUINO_WAIT),
            shutdown_on_exception=self.settings.get(constants.KEY_SHUTDOWN_ON_EXCEPTION),
            sleep_tune=self.settings.get(constants.KEY_SLEEP_TUNE),
            debug=self.settings.get(constants.KEY_DEBUG),
        )
        self.arduino.connection_changed.connect(self.on_connection_changed)
        await self.arduino.async_connect()
        self.arduino.start_monitoring()

    def on_connection_changed(self, connected: bool, message: str = None) -> None:
        """Callback for the USB device."""
        log.info(f"Connection changed: {connected}, message: {message}")
        if connected:  # device is connected
            self.usb_label.setText(f"USB connected: {message}")
            self.actionConnect.setText("Disconnect")
            self.state = State.CONNECTED
        else:
            self.usb_label.setText("USB disconnected")
            error(f"USB: connection lost. Error: {message}")
            self.insert_text(f"<h2>USB Error: {message}</h2>")
            self.state = State.IDLE

    def connect_device(self) -> None:
        if self.state == State.CONNECTING:
            return
        elif self.state == State.CONNECTED:
            asyncio.create_task(self.disconnect_device())
        elif self.state == State.IDLE:
            self.state = State.CONNECTING
            asyncio.create_task(self.connect_task())

    async def disconnect_device(self):
        # Await the asynchronous disconnect on your device.
        # if self.usb_device is None:
        #     return
        await self.arduino.async_disconnect()
        self.device_connected = False
        log.info("Device disconnected successfully.")
        self.actionConnect.setText("Connect")
        # self.usb_device = None
        self.state = State.IDLE

    def control_manually(self) -> None:
        self.manual = ManualWidget(self.arduino)
        self.manual.show()

    def modify_settings(self) -> None:
        self.settings_dialog.show()

    # @Slot(Tuple[int, QObject])

    def on_settings_closed(self, result: Tuple) -> None:
        return_val, settings = result
        app_logger.info(f"Settings dialog closed. Result: {return_val}")
        self.text_edit.setStyleSheet(
            f"color: {self.settings.get(constants.KEY_FOREGROUND_COLOR)};"
            f"background-color: {self.settings.get(constants.KEY_BACKGROUND_COLOR)};"
        )
        if self.settings.get(constants.KEY_FULLSCREEN):
            self.showFullScreen()
        else:
            self.showNormal()

        if settings.qfont:
            print(settings.qfont)
            self.text_edit.setFont(settings.qfont)

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
        if not self.eax_device.is_selected:
            warning(self, "Please select a device.")
            return

        if (self.state == State.IDLE or self.state == State.CONNECTED):
            # Check if the firmware file exists
            if not os.path.exists(self.eax_device.firmware_path):
                self.insert_text(
                    f"{self.eax_device.firmware_path} not found!")
                return

            # self.settings.load_settings()  # reload the settings
            chip = self.settings.get("chip_part")
            # serial = self.settings.get("programmer_serial_number")
            programmer_path = self.settings.get("programmer_path")

            command = [
                programmer_path,
                "/part",
                chip,
                "/p",
                self.eax_device.firmware_path,
                "/q1",
            ]

            self.state = State.PROGRAMMING

            logg.info(f"Programming {self.eax_device._selected_device}, args: {command}")

            self.program_thread = ProgrammingThread(command)
            self.program_thread.resultReady.connect(self.handle_programming_result)
            self.program_thread.start()

    def handle_programming_result(self, returncode=0) -> None:
        # This function gets called when the command finishes.
        # Do whatever you need to do with the return code here.
        self.program_thread.quit()
        if returncode == 0:
            self.insert_text("<p>Programming successful.</p>")
            log.info(f"Programming {self.eax_device._selected_device} successful")
            logg.success(f"Programming {self.eax_device._selected_device} successful")
            if self.settings.get(constants.KEY_AUTO_TEST):
                if self.arduino.device_connected:
                    self.state = State.CONNECTED
                else:
                    self.state = State.IDLE
                self.test_button.click()
                return
        else:
            self.insert_text(f"<p>Programming failed. Return code: {returncode}</p>")
            logg.error(f"Programming {self.eax_device._selected_device} failed. Error code: {returncode}")
            log.error(f"Programming {self.eax_device._selected_device} failed. Error code: {returncode}")

        if self.arduino.device_connected:
            self.state = State.CONNECTED
        else:
            self.state = State.IDLE

    def show_statistics(self) -> None:
        (fail, success) = logg.count_programming_errors(
        ), logg.count_programming_successes()
        tested = logg.count_devices_tested()
        QMessageBox().information(
            self,
            "Statistics",
            f"Total Tests: {tested}\nSuccessful: {success}\nFailed: {fail}",
        )

    def show_log(self) -> None:
        """Display the log view widget."""
        logs = logg.get_all_logs()
        self.log_view = LogView(logs, self.save_logs)
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
            logg.info("Application closed.")
            app_logger.info("Application closed.")
            self.settings.app_settings.setValue("mainwindow/geometry", self.saveGeometry())
            self.settings.app_settings.setValue("mainwindow/windowState", self.saveState())
            self.settings.app_settings.setValue("mainwindow/full_screen", self.isFullScreen())
            self.settings.app_settings.sync()
            event.accept()
        else:
            event.ignore()

    def update_firmware(self) -> None:
        """Update the firmware on the test fixture."""
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Select Firmware")
        dialog.setText("Select the firmware to upload:")
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        btnFirmata = dialog.button(QMessageBox.StandardButton.Yes)
        btnFirmata.setText("Firmata (old)")
        btnTelemetrix = dialog.button(QMessageBox.StandardButton.No)
        btnTelemetrix.setText("Telemetrix (new)")

        cancelBtn = dialog.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        dialog.setDefaultButton(cancelBtn)
        dialog.setIcon(QMessageBox.Question)

        dialog.exec()

        if dialog.clickedButton() == cancelBtn:
            app_logger.info("Firmware update cancelled.")
            return
        elif dialog.clickedButton() == btnFirmata:
            firmware_path = ".\\sketches\\StandardFirmata\\build\\arduino.avr.uno\\StandardFirmata.ino.hex"
        elif dialog.clickedButton() == btnTelemetrix:
            firmware_path = ".\\sketches\\Telemetrix4Arduino\\build\\arduino.avr.uno\\Telemetrix4Arduino.ino.hex"
        else:
            app_logger.info("Firmware update cancelled.")
            return

        self.state = State.UPDATING

        self.set_status("Firmware Update...")
        info("Updating firmware...")
        self.disconnected = False
        if self.arduino.device_connected:
            self.disconnected = True
            asyncio.create_task(self.disconnect_device())

        port = self.settings.get(constants.KEY_COM_PORT, constants.DEFAULT_SETTINGS[constants.KEY_COM_PORT])

        # Define the PowerShell script path
        # script_path = ".\\Scripts\\UpdateFirmware.PS1"
        script_path = ".\\Scripts\\Upload.ps1"
        self.update_process.setWorkingDirectory(os.getcwd())
        self.text_edit.setMarkdown(f"# Updating firmware... \n\n")

        # Define the command to execute
        self.update_process.start(
            "powershell.exe",
            # ["-ExecutionPolicy", "ByPass", "-File", script_path, firmware_path, port],
            ["-File", script_path, firmware_path, port],
        )

    def on_error(self, error: QProcess.ProcessError) -> None:
        app_logger.error("An error occurred: ", error)
        app_logger.error("System reported: ", self.update_process.errorString())
        app_logger.error("Firmware update failed: ", error)
        logg.critical("Firmware update failed: ", error)

    def read_standard_output(self) -> None:
        output = self.update_process.readAllStandardOutput().data().decode()
        self.insert_text(output)
        app_logger.info(output)
        msg = self.update_process.readAllStandardError().data().decode()
        if msg != "":
            self.insert_text(msg)
            app_logger.error(msg)

    def on_finished(self) -> None:
        app_logger.success("The process has finished")
        app_logger.info("Firmware update complete.")
        if self.eax_device._selected_device:
            self.device_label.setText(
                f"Device: {self.eax_device._selected_device}")
        else:
            self.device_label.setText("Firmware Update Complete.")
        self.state = State.IDLE
        if self.disconnected:
            self.connect_device()
        self.update_process.terminate()
        if not self.update_process.waitForFinished(3000):
            self.update_process.kill()
            app_logger.error("Process did not terminate in time.")

    def increment_counter(self) -> None:
        """Set the progress value in the status bar."""
        if self.settings.get_bool(constants.KEY_COUNTER_ENABLED, False):
            self.settings.setValue(
                constants.KEY_TEST_COUNT, self.settings.get_int(constants.KEY_TEST_COUNT) + 1)
        sb = self.statusBar()
        sb.update_counter()

    def on_test_clicked(self) -> None:
        """Called when the test button is clicked."""
        if not self.eax_device.is_selected:
            warning(self, "Please select a device.")
        elif self.state is State.WAITING_FOR_BUTTON:
            # notify the input event
            if hasattr(self, 'input_event') and not self.input_event.is_set():
                self.input_event.set()
        elif self.state == State.IDLE:
            warning(self, f"USB device not connected.")
        elif self.state is not State.CONNECTED:
            warning(self, f"Cannot run test.")
        else:
            asyncio.create_task(self.run_test())

    async def run_test(self) -> None:
        """Run the test."""

        self.increment_counter()

        model = self.eax_device.name

        # app_logger.info(f"Testing started for {model.name}")
        app_logger.info(f"Testing started for {model}")
        logg.info(f"Testing started for {model}")

        self.state = State.TESTING

        speed = self.settings.get_int(constants.KEY_TESTING_SPEED, constants.DEFAULT_SETTINGS[constants.KEY_TESTING_SPEED]) / 1000

        self.text_edit.setMarkdown(f"# Starting test for {model}... \n\n")

        await self.arduino.write_pin_by_func("test indicator", 1)
        self.insert_text("<br><p>🔷 Battery Power ON</p>")
        await self.arduino.write_pin_by_func("battery", 1)

        await asyncio.sleep(speed)

        self.insert_text("<p>🔷 Testing Low battery function ➾ The LED's blink alternately</p>")
        await self.arduino.write_pin_by_func("low battery", 1)

        await asyncio.sleep(speed)

        self.insert_text("<p>🔷 Stopping Low Battery Test ➾ Both LED's are OFF</p>")
        await self.arduino.write_pin_by_func("low battery", 0)

        await asyncio.sleep(speed)

        self.insert_text("<p>🔷 Press the OKC switch ➾ The LEDs blink in unison</p>")

        await asyncio.sleep(speed/4)

        self.insert_text("<p>🔷 Press the key switch ➾ The siren sounds</p>")

        self.insert_text("<br><p>⌛<em>Press the Test/Continue Button when finished</em></p>")

        self.state = State.WAITING_FOR_BUTTON

        # Wait for the button to be pressed
        try:
            self.input_event = asyncio.Event()
            timeout = self.settings.get_int(constants.KEY_BUTTON_TIMEOUT, constants.DEFAULT_SETTINGS[constants.KEY_BUTTON_TIMEOUT])
            await asyncio.wait_for(self.input_event.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            pass

        self.insert_text("✨Test complete.")

        if self.settings.get_bool(constants.KEY_COUNTER_ENABLED, False):
            logg.info(f"Test complete for {model}. (Cycle count: {self.settings.get_int(constants.KEY_TEST_COUNT, 0)})")
        else:
            logg.info(f"Test complete for {model}.")

        await self.arduino.write_pin_by_func("test indicator", 0)
        await self.arduino.write_pin_by_func("battery", 0)
        await self.arduino.write_pin_by_func("low battery", 0)

        await asyncio.sleep(speed/3)

        self.state = State.CONNECTED

        self.load_file_text()


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
        self.settings = ApplicationSettings()
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
                await self._arduino.write_pin_by_func("test indicator", 1)

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
    saved = Signal(Any)

    def __init__(self, parent: MainWindow = None):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setupUi(self)
        # self.app_settings = settings.app_settings
        self.settings: ApplicationSettings = parent.settings
        self._parent = parent

        self.background_color: QColor = None
        self.foreground_color: QColor = None
        self.qfont: QFont = None

        self.pushButton_background_color.clicked.connect(self.pick_background_color)
        self.pushButton_foreground_color.clicked.connect(self.pick_color)
        self.pushButton_change_font.clicked.connect(self.change_font)

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_default.clicked.connect(self.reset_to_default)
        self.resetCounterButton.clicked.connect(self.reset_counter)
        self.initialize_settings()

        # Set the theme
        self.setStyleSheet(get_stylesheet(self.settings))

    def initialize_settings(self) -> None:
        config = ConfigLoader()

        self.lineEdit_serial.setText(self.settings.app_settings.value(constants.KEY_PROGRAMMER_SERIAL_NUMBER, config.get_default_setting(constants.KEY_PROGRAMMER_SERIAL_NUMBER)))

        chip_options = config.chip_options
        for chip_part in chip_options:
            self.comboBox_chip.addItem(chip_part)

        self.comboBox_chip.setCurrentText(self.settings.app_settings.value(constants.KEY_CHIP_PART, config.get_default_setting(constants.KEY_CHIP_PART)))

        value = self.settings.get_int(constants.KEY_TESTING_SPEED, config.get_default_setting(constants.KEY_TESTING_SPEED))
        self.dial.setValue(value)

        self.comboBox_com_port.setCurrentText(self.settings.app_settings.value(constants.KEY_COM_PORT, config.get_default_setting(constants.KEY_COM_PORT)))

        for port in AIODevice.get_usb_ports():
            self.comboBox_com_port.addItem(port)

        self.spinBox_autologoff_delay.setValue(self.settings.get_int(constants.KEY_INACTIVITY_TIMEOUT, config.get_default_setting(constants.KEY_INACTIVITY_TIMEOUT)))
        self.spinBox_arduino_id.setValue(self.settings.get_int(constants.KEY_ARDUINO_INSTANCE_ID, config.get_default_setting(constants.KEY_ARDUINO_INSTANCE_ID)))
        self.checkBox_test.setChecked(self.settings.get_bool(constants.KEY_AUTO_TEST, config.get_default_setting(constants.KEY_AUTO_TEST)))
        self.checkBox_connect.setChecked(self.settings.get_bool(constants.KEY_AUTO_CONNECT, config.get_default_setting(constants.KEY_AUTO_CONNECT)))
        self.checkBox_debug.setChecked(self.settings.get_bool(constants.KEY_DEBUG, config.get_default_setting(constants.KEY_DEBUG)))
        self.checkBox_auto_find.setChecked(self.settings.get_bool(constants.KEY_AUTO_FIND, config.get_default_setting(constants.KEY_AUTO_FIND)))
        self.checkBox_shutdown_on_exception.setChecked(self.settings.get_bool(constants.KEY_SHUTDOWN_ON_EXCEPTION, config.get_default_setting(constants.KEY_SHUTDOWN_ON_EXCEPTION)))
        self.lineEdit_serial_sleep_tune.setText(str(self.settings.app_settings.value(constants.KEY_SLEEP_TUNE, config.get_default_setting(constants.KEY_SLEEP_TUNE))))
        self.spinBox_wait_time.setValue(self.settings.get_int(constants.KEY_ARDUINO_WAIT, config.get_default_setting(constants.KEY_ARDUINO_WAIT)))
        self.checkBox_fullscreen.setChecked(self.settings.get_bool(constants.KEY_FULLSCREEN, config.get_default_setting(constants.KEY_FULLSCREEN)))
        self.checkBox_touchscreen.setChecked(self.settings.get_bool(constants.KEY_TOUCHSCREEN_ENABLED, config.get_default_setting(constants.KEY_TOUCHSCREEN_ENABLED)))
        self.checkBox_frameless.setChecked(self.settings.get_bool(constants.KEY_FRAMELESS, config.get_default_setting(constants.KEY_FRAMELESS)))
        self.counterCheckbox.setChecked(self.settings.get_bool(constants.KEY_COUNTER_ENABLED, constants.DEFAULT_SETTINGS[constants.KEY_COUNTER_ENABLED]))

    def reset_to_default(self) -> None:
        config = ConfigLoader()
        default_settings = config.settings

        self.comboBox_com_port.setCurrentText(default_settings[constants.KEY_COM_PORT])
        self.lineEdit_serial.setText(default_settings[constants.KEY_PROGRAMMER_SERIAL_NUMBER])
        self.comboBox_chip.setCurrentText(default_settings[constants.KEY_CHIP_PART])
        self.dial.setValue(default_settings[constants.KEY_TESTING_SPEED])
        self.checkBox_test.setChecked(default_settings[constants.KEY_AUTO_TEST])
        self.checkBox_connect.setChecked(default_settings[constants.KEY_AUTO_CONNECT])
        self.spinBox_arduino_id.setValue(default_settings[constants.KEY_ARDUINO_INSTANCE_ID])
        self.checkBox_debug.setChecked(default_settings[constants.KEY_DEBUG])
        self.spinBox_autologoff_delay.setValue(default_settings[constants.KEY_INACTIVITY_TIMEOUT])
        self.spinBox_wait_time.setValue(default_settings[constants.KEY_ARDUINO_WAIT])
        self.checkBox_shutdown_on_exception.setChecked(default_settings[constants.KEY_SHUTDOWN_ON_EXCEPTION])
        self.checkBox_auto_find.setChecked(default_settings[constants.KEY_AUTO_FIND])
        self.lineEdit_serial_sleep_tune.setText(str(default_settings[constants.KEY_SLEEP_TUNE]))
        self.checkBox_fullscreen.setChecked(default_settings[constants.KEY_FULLSCREEN])
        self.checkBox_touchscreen.setChecked(default_settings[constants.KEY_TOUCHSCREEN_ENABLED])
        self.checkBox_frameless.setChecked(default_settings[constants.KEY_FRAMELESS])
        self.counterCheckbox.setChecked(constants.DEFAULT_SETTINGS[constants.KEY_COUNTER_ENABLED])

    def save_changes(self) -> None:
        if self.background_color:
            self.settings.setValue(constants.KEY_BACKGROUND_COLOR,
                                   self.background_color.name())
        if self.foreground_color:
            self.settings.app_settings.setValue(constants.KEY_FOREGROUND_COLOR,
                                                self.foreground_color.name())
        if self.qfont:
            self.settings.setValue(constants.KEY_FONT_FAMILY, QFontInfo(self.qfont).family())
            self.settings.setValue(constants.KEY_FONT_SIZE, QFontInfo(self.qfont).pointSize())
            self.settings.setValue(constants.KEY_FONT_WEIGHT, QFontInfo(self.qfont).weight())
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
        self.settings.setValue(constants.KEY_TOUCHSCREEN_ENABLED, self.checkBox_touchscreen.isChecked())
        self.settings.setValue(constants.KEY_TOUCHSCREEN_ENABLED, self.checkBox_touchscreen.isChecked())
        self.settings.setValue(constants.KEY_FRAMELESS, self.checkBox_frameless.isChecked())
        self.settings.setValue(constants.KEY_COUNTER_ENABLED, self.counterCheckbox.isChecked())
        self.saved.emit((0, self))
        self.close()

    def pick_color(self, *args) -> None:
        print(args)
        self.foreground_color = self.choose_color(
            self.settings.get(constants.KEY_FOREGROUND_COLOR, "#ffffff"))
        app_logger.debug(f"User selected color: {self.foreground_color.name()}")

    def pick_background_color(self, *args) -> None:
        print(args)
        self.background_color = self.choose_color(
            self.settings.get(constants.KEY_BACKGROUND_COLOR, "#000000"))
        app_logger.debug(f"User selected color: {self.background_color.name()}")

    def choose_color(self, color_name: str) -> QColor:
        new_color = QColorDialog.getColor(color_name)
        if new_color.isValid():
            return new_color
        else:
            return QColor(color_name)

    def change_font(self) -> None:
        ok, font = get_font([
            self.settings.get(constants.KEY_FONT_FAMILY, self._parent.font().family()),
            self.settings.get_int(constants.KEY_FONT_SIZE, self._parent.font().pointSize()),
            self.settings.get_int(constants.KEY_FONT_WEIGHT, self._parent.font().weight())
        ])
        if ok:
            print(font)
            self.qfont = font

    def closeEvent(self, event) -> None:
        # self.settings.load_settings()
        self.saved.emit((0, self))
        # self.destroy()
        event.accept()

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

    def reset_counter(self) -> None:
        self.settings.setValue(constants.KEY_TEST_COUNT, 0)
        sb = self._parent.statusBar()
        sb.widget.lcdNumber.display(0)


class SaveWorker(QThread):
    """
    A worker thread for saving log data to the database.

    :param data: The log data to be saved.
    """
    progress_changed = Signal(int)

    def __init__(self, data: List[Dict[str, str]]):
        super(SaveWorker, self).__init__()
        self.data = data
        self.length = self.data.__len__()
        self.setObjectName("SaveWorker")

    def run(self):
        logg.clear_all_logs()
        for entry in self.data:
            log_entry = f"{entry['timestamp']} - logger - {entry['level']} - {entry['message']}"
            app_logger.info(log_entry)
            logg.insert_log(entry['timestamp'], "logger", entry['level'], entry['message'])
            progress = ceil(self.data.index(entry) / self.length * 100)
            self.progress_changed.emit(progress)
        super(SaveWorker, self).exec()


class ProgressBar(QWidget, Ui_ProgressBar):
    """
    A progress bar dialog window.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.settings = ApplicationSettings()
        self.setStyleSheet(get_stylesheet(self.settings))

    def update_progress(self, value: int) -> None:
        self.progressBar.setValue(value)
        if value == 100:
            self.close()


class ProgrammingThread(QThread):
    resultReady = Signal(int)

    def __init__(self, command: List[str]):
        super(ProgrammingThread, self).__init__()
        self.command = command
        # set thread name
        self.setObjectName("ProgrammingThread")

    def run(self) -> None:
        debug(f"Running command: {self.command}")
        debug(" ".join(self.command))
        process = subprocess.run(self.command, shell=True)
        self.resultReady.emit(process.returncode)
        super(ProgrammingThread, self).exec()

    def quit(self):
        """Override the quit method to ensure the thread is stopped properly."""
        print("Stopping ProgrammingThread...")
        return super().quit()


class ConnectMenu(QAction):
    """A custom QMenu that emits a signal when clicked."""

    def __init__(self, parent: MainWindow):
        super().__init__(parent)
        parent.set_icon(self, 'usb2')
        self.triggered.connect(parent.connect_device)


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


class StatusWidget(QWidget, Ui_StatusBarWidget):
    """
    A custom status bar widget that displays a message and a counter.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class CustomStatusBar(QStatusBar):
    """
    A custom status bar that is able to display a persistant message.
    """

    def __init__(self):
        super().__init__()
        self.widget = StatusWidget()
        self.addPermanentWidget(self.widget, 1)

        self.widget.lcdNumber.setDigitCount(5)
        self.settings = ApplicationSettings()
        if self.settings.get_bool(constants.KEY_COUNTER_ENABLED, False):
            self.widget.lcdNumber.display(self.settings.get_int(constants.KEY_TEST_COUNT, 0))

        self._persistent_message = ""

        app = QApplication.instance()
        if app:
            app.installEventFilter(self)      # catch status‐tips anywhere

    def eventFilter(self, watched, event):
        # catch hover‐tips
        if event.type() == QEvent.StatusTip:
            tip = event.tip()
            if tip:
                # a new hover tip arrived → show it
                self.widget.status.setText(tip)
            else:
                # tip="" means “clear the hover tip” → go back to real text
                self.widget.status.setText(self._persistent_message)
            return True
        return super().eventFilter(watched, event)

    def clearMessage(self):
        self.widget.status.clear()
        super().clearMessage()
        if self._persistent_message:
            self.widget.status.setText(self._persistent_message)

    def showMessage(self, message: str, timeout: int = 0) -> None:
        self._persistent_message = message
        self.widget.status.setText(message)
        if timeout > 0:
            QTimer.singleShot(timeout, lambda: self.clearMessage())

    def update_counter(self) -> None:
        # IF the persistant counter is enabled, increment the counter in the settings
        # so that it can be restored on the next run. Otherwise, just increment the counter in the widget.
        if self.settings.get_bool(constants.KEY_COUNTER_ENABLED, False):
            self.widget.lcdNumber.display(self.settings.get_int(constants.KEY_TEST_COUNT, 0))
        else:
            current_value = self.widget.lcdNumber.value()
            self.widget.lcdNumber.display(current_value + 1)


def extract_zip_from_resources(path: str) -> None:
    """Extracts a ZIP file from the resources and extracts its contents to the specified path."""
    # Open the ZIP file stored in resources
    zip_file = QFile(":/resources/default_resources.zip")
    if zip_file.open(QIODevice.ReadOnly):
        # Read the contents into a QByteArray
        zip_data = zip_file.readAll()
        # Use BytesIO to treat the QByteArray as a file-like object
        zip_file_like = io.BytesIO(zip_data)
        # Now, use the zipfile module to extract files from the ZIP archive
        with zipfile.ZipFile(zip_file_like, 'r') as zip_ref:
            # List all files in the ZIP file
            zip_ref.printdir()
            # Extract all files (you can specify a directory if you want to extract it somewhere)
            zip_ref.extractall(path)
            print("ZIP file extracted successfully.")
    else:
        print("Failed to open the ZIP file from resources.")


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


if __name__ == "__main__":
    # with log.catch(
    #     message="Encountered exception from main.",
    #     reraise=True,
    #     exception=BaseException,
    # ):
    # app = SingleInstanceApp(sys.argv)
    # debug("Checking for running instances")
    # if app.is_running:
    #     log.critical(
    #         "Another instance of the application is already running.")
    #     critical(
    #         None,
    #         "Another instance of the application is already running.",
    #     )
    #     sys.exit(1)

    if not verify_files([
        "settings.ini",
        "instructions.md",
        "config.yaml",
        "Scripts/Upload.ps1",
        "Scripts/UpdateFirmware.ps1",
        "sketches/Telemetrix4Arduino/build/arduino.avr.uno/Telemetrix4Arduino.ino.hex",
        "sketches/StandardFirmata/build/arduino.avr.uno/StandardFirmata.ino.hex",
        "firmware/EAX300_59.hex",
        "firmware/EAX500_591.hex",
        "firmware/EAX505_591.hex",
        "firmware/EAX525_591.hex",
    ]):
        print("Some files are missing. Extracting defaults from resources.")
        extract_zip_from_resources('.')
        print('Restart the application to apply the changes.')
        # sys.exit(1)

    app_logger = applogger.AppLogger.get_logger()
    logg = applogger.LogManager()

    app = SingleInstanceApp(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow(app)
    window.show()
    info("Application started.")
    with loop:
        loop.run_forever()
