from math import ceil
from psutil import Popen
from config_loader import ConfigLoader
import config_loader
from imports import *
from rich import print


class LoginDialog(QDialog, Ui_LoginDialog):
    """
    Login dialog. This dialog allows the user to login to the application.

    :param last_user: The last user that logged in.
    """

    def __init__(self, last_user=None):
        super().__init__()
        self.setupUi(self)

        self.setStyleSheet(get_stylesheet())

        self.app_settings = QSettings("Detex Corp", "Login Dialog")
        self.restoreGeometry(self.app_settings.value("geometry", QByteArray()))

        for username in db.get_users():
            self.comboBox.addItem(username)
        self.comboBox.setCurrentText(last_user)

        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)

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
            return
        elif key == Qt.Key_F2:
            screen = QtGui.QGuiApplication.primaryScreen()
            QtCore.QCoreApplication.processEvents()
            pixmap = screen.grabWindow(self.winId())
            img = pixmap.toImage()
            t = time.time()
            img.save(f"screenshot-{t}.png")
            QtCore.QCoreApplication.processEvents()
            return
        super().keyPressEvent(event)


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

        self.app_settings = QSettings("Detex Corp", "Log View")
        self.restoreGeometry(self.app_settings.value("geometry", QByteArray()))
        self.setStyleSheet(get_stylesheet())

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
        self.app_settings.setValue("geometry", self.saveGeometry())
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
        self.app_settings = QSettings("Detex Corp", "Help Dialog")
        self.restoreGeometry(self.app_settings.value("geometry", QByteArray()))
        # self.toolBox.currentChanged.connect(self.on_tab_clicked)
        self.label.installEventFilter(self)
        self.label_2.installEventFilter(self)
        self.label_3.installEventFilter(self)
        self.setStyleSheet(get_stylesheet())

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
        self.app_settings.setValue("geometry", self.saveGeometry())
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
    button_pressed: bool = False
    connecting: bool = False
    log_view: LogView = None
    help_dialog: HelpDialog = None
    loginDialog: LoginDialog = None
    arduino: USBDevice = None
    _drag_pos: int = None
    eax_device = Device()

    def __init__(self, app) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/resources/icons/images/icons/code.ico"))
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Settings
        self.settings: ApplicationSettings = settings
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.saved.connect(self.on_settings_closed)
        # Restore the window geometry and state
        self.app_settings = QSettings("Detex Corp", "EAX Interface")
        self.restoreGeometry(self.app_settings.value("geometry", QByteArray()))
        self.restoreState(self.app_settings.value("windowState", QByteArray()))

        print(f"Settings: {self.app_settings.allKeys()}")

        if self.app_settings.value(KEY_FULLSCREEN, type=bool):
            self.showFullScreen()
        else:
            self.showNormal()
        self.actionFullscreen.setChecked(
            self.app_settings.value(KEY_FULLSCREEN, type=bool)
        )
        self.actionFullscreen.triggered.connect(self.toggleFullScreen)

        if self.settings.get_bool(KEY_FRAMELESS):
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # Process for updating the firmware
        self.update_process = QProcess(self)
        self.update_process.finished.connect(self.on_finished)
        self.update_process.errorOccurred.connect(self.on_error)
        self.update_process.readyReadStandardError.connect(
            self.read_standard_output)
        self.update_process.readyReadStandardOutput.connect(
            self.read_standard_output)
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
        print(self.settings.get(KEY_FONT_FAMILY))
        # Setup the text area
        self.text_edit.setFont(
            QFont(
                self.settings.get(KEY_FONT_FAMILY),
                self.settings.get_int(KEY_FONT_SIZE),
            )
        )
        self.text_edit.setStyleSheet(
            f"color:{self.settings.get(KEY_FOREGROUND_COLOR)};"
            f"background-color:{self.settings.get(KEY_BACKGROUND_COLOR)};"
        )

        # Connect the menu items
        self.actionExplore_Directory.triggered.connect(browse_directory)
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
        self.actionScreenshot.triggered.connect(take_screenshot)
        self.actionLogout.triggered.connect(self.perform_login)
        self.program_button.clicked.connect(self.program)
        self.test_button.clicked.connect(self.execute_test)

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

        if not self.eax_device.verify_firmware():
            self.insert_text("Missing firmware!")
            log.critical("Missing firmware!")
            app_logger.critical("Missing firmware!")

        # Set the theme
        self.set_theme(get_theme())

        print(logg.check_integrity())
        logg.backup_database()
        db.backup_database()
        clean_backups("backups", 5)

        # If auto login and auto connect are enabled, try to connect to the USB device
        if self.settings.get(KEY_AUTO_LOGIN) and self.settings.get(KEY_AUTO_CONNECT):
            QTimer.singleShot(2000, self.connect_device)

        self.timeout_timer = QTimer()
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.timeout.connect(self.on_timeout)

    @property
    def state(self) -> State:
        # print(f"Getting state: {self._state}")
        return self._state

    @state.setter
    def state(self, value: State) -> None:
        log.debug(f"Setting state to {value}")
        self._state = value

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.geometry().topLeft()
            event.accept()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()
        else:
            super().mouseMoveEvent(event)

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
        anchor = self.text_edit.anchorAt(
            self.text_edit.mapFromGlobal(QCursor.pos()))
        if anchor:
            debug(current_position)
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
            style = qdarkstyle.load_stylesheet(palette=DarkPalette)
            self.actionDark_Theme.setChecked(True)
        else:
            style = qdarkstyle.load_stylesheet(palette=LightPalette)
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
        self.set_icon(self.actionAdd_User, 'follow')
        self.set_icon(self.actionRemove_User, 'remove-user')
        self.set_icon(self.actionHelp, 'help')
        self.set_icon(self.actionStatisitics, 'bar-chart')
        self.set_icon(self.actionLogout, 'logout')

    def toggle_theme(self) -> None:
        log.info("Toggle theme")
        if self.settings.get_bool(KEY_DARK_THEME):
            self.app_settings.setValue(KEY_DARK_THEME, False)
            self.set_theme('light')
            self.actionDark_Theme.setChecked(False)
        else:
            self.app_settings.setValue(KEY_DARK_THEME, True)
            self.set_theme('dark')
            self.actionDark_Theme.setChecked(True)

    def set_icon(self, widget: QObject, icon_name: str, ext='png') -> None:
        if get_theme() == 'dark':
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
        elif key == Qt.Key.Key_Q and event.modifiers() & ControlModifier:
            sys.exit(0)
        elif key == Qt.Key.Key_F2:
            take_screenshot()
        elif key == Qt.Key.Key_F3:
            self.control_manually()
        elif key == Qt.Key.Key_F4:
            self.actionConnect.trigger()
        elif key == Qt.Key.Key_E and event.modifiers() & ControlModifier:
            logg.export_logs()
        elif key == Qt.Key.Key_R and event.modifiers() & ControlModifier:
            is_frameless = self.windowFlags() & Qt.FramelessWindowHint
            # Toggle between frameless and regular states
            if is_frameless:
                self.setWindowFlags(self.windowFlags() & ~
                                    Qt.FramelessWindowHint)
                self.settings.setValue(KEY_FRAMELESS, False)
            else:
                self.setWindowFlags(self.windowFlags() |
                                    Qt.FramelessWindowHint)
                self.settings.setValue(KEY_FRAMELESS, True)
            QTimer.singleShot(10, self.show)
        elif key == Qt.Key.Key_1 and event.modifiers() & ControlModifier:
            log.warning(f"State: {self.state}")
        elif (
            key == Qt.Key.Key_2 and
            event.modifiers() & ControlModifier
        ):
            log.warning(f"Device: {self.eax_device.name}")
        elif key == Qt.Key.Key_A and event.modifiers() & ControlModifier:
            print(vars(self))
            print(vars(self.settings))
            print(vars(app_logger))
            print(vars(self.arduino))
            print(vars(db))
            print(vars(logg))


    def on_device_changed(self, device: str) -> None:
        """ Called when the device is changed. """
        log.info(f"Device changed: {device}")
        self.device_label.setText(f"Device: {device}")
        self.eax_device.name = device

        # Set the color of the device label
        if self.eax_device.name == "EAX300":
            self.device_label.setStyleSheet(YELLOW)
        elif self.eax_device.name == "EAX500":
            self.device_label.setStyleSheet(GREEN)
        else:
            self.device_label.setStyleSheet(ORANGE)

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
            self.device_label.setStyleSheet(DEVICE_LABEL)
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
            self.settings.setValue(KEY_FONT_FAMILY, QFontInfo(font).family())
            self.app_settings.setValue(
                KEY_FONT_FAMILY, QFontInfo(font).family())
            self.settings.setValue(KEY_FONT_SIZE, font.pointSize())
            self.app_settings.setValue(KEY_FONT_SIZE, font.pointSize())

    def get_chip_part(self) -> None:
        self.settings.load_settings()
        current_chip = self.settings.get(KEY_CHIP_PART)
        current_selection = CHIP_OPTIONS.index(current_chip)
        item, okPressed = QInputDialog.getItem(
            self, "Get item", "Chip Select:", CHIP_OPTIONS, current_selection, False
        )
        if okPressed and item:
            self.settings_dialog.comboBox_chip.setCurrentText(
                item
            )  # update the combo box
            self.settings.setValue(KEY_CHIP_PART, item)
            self.app_settings.setValue(KEY_CHIP_PART, item)
            log.debug(f"saved chip settings: {item}")

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        # Handle mouse clicks on the scroll area
        # if watched.objectName() == "qt_scrollarea_viewport":
        #     if event.type() == QEvent.MouseButtonPress:
        #         if event.button() == Qt.LeftButton:
        #             log.info("Left mouse button clicked!")
        #             if self.settings.get_bool(KEY_TOUCHSCREEN_ENABLED):
        #                 self.test_button.click()
        #                 return True  # event was handled

        # Reset the inactivity timer if a mouse movement or key press event is detected
        if event.type() in (QEvent.MouseMove, QEvent.KeyPress):
            self.inactivityTimer.start(
                self.settings.get_int(KEY_LOGOFF_DELAY, 10) * 60 * 1000
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

        # if not self.settings.get_bool(KEY_AUTO_LOGIN):
        #     self.perform_login()  # show the login dialog

        icon = QIcon()
        icon.addFile(RADIO_OFF_ICON, QSize(), QIcon.Normal, QIcon.On)
        # Uncheck all menu actions
        [action.setIcon(icon) for action in self.menuDevice.actions()]
        self.device_label.setText("")  # clear the device label
        self.eax_device.name = None  # reset the device
        [self.perform_login() if not self.settings.get_bool(KEY_AUTO_LOGIN) else self._pass()]

    def add_user(self) -> None:
        if self.settings.get_bool(KEY_AUTO_LOGIN):
            if not self.authenticate():
                return
        self.add = UserAdditionDialog()
        self.add.show()

    def remove_user(self) -> None:
        # force the user to login if auto login is enabled
        if self.settings.get(KEY_AUTO_LOGIN):
            if not self.authenticate():
                return
        self.remove = UserRemovalDialog()
        self.remove.show()

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

    def connect_device(self) -> None:
        if self.state == State.CONNECTING:
            return

        if not self.arduino:
            self.arduino = USBDevice(
                device_connected_callback=self.notify_device_connected,
                wait=self.settings.get(KEY_ARDUINO_WAIT),
                shutdown_on_exception=self.settings.get(
                    KEY_SHUTDOWN_ON_EXCEPTION),
                sleep_tune=self.settings.get(KEY_SLEEP_TUNE),
                debug=self.settings.get(KEY_DEBUG),
            )

        if not self.arduino.connected:
            self.connecting = True
            self.state = State.CONNECTING
            self.label_usb_icon.setText(ICON_USB_YELLOW)
            self.usb_label.setStyleSheet(YELLOW)
            self.usb_label.setText("Connecting...")
            self.arduino.connect(self.notify_device_connected)
            self.arduino.attach_callback(self.input_callback, 7)

    def notify_device_connected(self, connected: bool, message: str=None) -> None:
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
            self.connect_menu.triggered.disconnect(
                self.connect_device
            )
            self.connect_menu.triggered.connect(
                self.disconnect_device
            )
            atexit.register(self.arduino.cleanup)
            self.state = State.CONNECTED

            # Save this port to the settings
            self.settings.setValue(KEY_COM_PORT, self.arduino.serial_port.port)
            self.app_settings.setValue(
                KEY_COM_PORT, self.arduino.serial_port.port)

            log_info(f"USB: connected to {self.arduino.serial_port.port}")
            log.success(f"USB: connected to {self.arduino.serial_port.port}")

        else:  # device is not connected
            error(f"USB: connection failed. Error: {message}")
            if message is not None and str.__contains__(
                message, "Incorrect Arduino ID"
            ):
                self.insert_text(f"Connection Failed. {message}")
            self.label_usb_icon.setText(ICON_USB_RED)
            self.actionConnect.setText("Connect")
            self.usb_label.setStyleSheet(RED)
            self.usb_label.setText("USB: connection failed")
            self.arduino = None
            self.state = State.IDLE

    def disconnect_device(self) -> None:
        if self.arduino:
            atexit.unregister(self.arduino.cleanup)
            self.arduino.set_all_pins_to_value(0)
            self.actionConnect.setText("Connect")
            self.actionConnect.triggered.connect(self.connect_device)
            self.actionConnect.triggered.disconnect(self.disconnect_device)
            self.connect_menu.triggered.connect(self.connect_device)
            self.connect_menu.triggered.disconnect(self.disconnect_device)
            self.label_usb_icon.setText(ICON_USB_RED)
            self.usb_label.setStyleSheet(RED)
            self.usb_label.setText("USB: disconnected")
            debug("USB: disconnected.")
            self.arduino.cleanup()
            self.arduino = None
            self.state = State.IDLE

    def control_manually(self) -> None:
        self.manual = ManualWidget(self.arduino)
        self.manual.show()

    def execute_test(self) -> None:
        """Start testing the device."""

        if self.state == State.WAITING_FOR_BUTTON:
            self.button_pressed = True
            return
        elif self.state == State.IDLE:
            warning(self, f"USB device not connected.")
            return
        elif self.state != State.CONNECTED:
            warning(self, f"Cannot run test.")
            return

        self.state = State.TESTING

        info(f"Testing started for {self.eax_device._selected_device}")

        dispatch = {
            "digital_write": self.arduino.digital_write,
            "insert_text": self.insert_text,
            "load_instructions": self.load_file_text,
            "wait_for_button": self.wait_for_button,
            "wait_for_input": self.wait_for_input,
            "set_indicator": self.arduino.set_indicator,
            "indicator_on": self.arduino.indicator_on,
            "indicator_off": self.arduino.indicator_off,
            "set_test_indicator": self.arduino.set_test_indicator,
            "test_indicator_on": self.arduino.test_indicator_on,
            "test_indicator_off": self.arduino.test_indicator_off,
            "set_battery": self.arduino.set_battery,
            "battery_on": self.arduino.battery_on,
            "battery_off": self.arduino.battery_off,
            "set_low_battery": self.arduino.set_low_battery,
            "low_battery_on": self.arduino.low_battery_on,
            "low_battery_off": self.arduino.low_battery_off,
            "set_remote": self.arduino.set_remote,
            "set_pad": self.arduino.set_pad,
            "set_relay1": self.arduino.set_relay1,
            "set_relay2": self.arduino.set_relay2,
            "set_all_pins_to_value": self.arduino.set_all_pins_to_value,
        }

        self.test_queue = []

        speed = self.settings.get_int(KEY_TESTING_SPEED)
        
        config = ConfigLoader()
        
        # Load the test instructions from the config file
        for instruction in config.get_testing_config():
            command_name = instruction["command"]
            params = instruction["params"]
            delay = instruction["delay"]

            if not delay:
                delay = speed

            command_function = dispatch.get(command_name)
            if command_function:
                self.test_queue.append((delay, command_function, *params))
                print(f"Added {command_name} to queue")
            else:
                error(f"Invalid command: {command_name}")

        self.text_edit.setMarkdown(
            f"# Starting test for {self.eax_device._selected_device}... "
        )

        # self.test_queue.append((1, self.arduino.test_indicator_on))

        # self.test_queue.append(
        #     (
        #         1,
        #         self.insert_text,
        #         "\n • Battery power on → Siren chirps and both LEDs flash  \n",
        #     )
        # )

        # self.test_queue.append((1, self.arduino.battery_on))

        # self.test_queue.append(
        #     (
        #         speed,
        #         self.insert_text,
        #         "\n • Starting low battery test → LEDs flash alternating \n",
        #     )
        # )

        # self.test_queue.append((1, self.arduino.low_battery_on))

        # self.test_queue.append(
        #     (
        #         speed,
        #         self.insert_text,
        #         "\n • Low battery test off → LEDs turn off.\n",
        #     )
        # )

        # self.test_queue.append((1, self.arduino.low_battery_off))

        # self.test_queue.append(
        #     (
        #         500,
        #         self.insert_text,
        #         (
        #             " • Perform the following:\n"
        #             " \t1. Press the key switch → The siren sounds\n"
        #             " \t2. Press the cylinder switch → The LEDs turn on\n"
        #         ),
        #     )
        # )

        # self.test_queue.append(
        #     (
        #         200,
        #         self.insert_text,
        #         "\n\nPress the Continue button to finish testing...",
        #     )
        # )

        # self.test_queue.append((1, self.wait_for_button))

        # self.test_queue.append((1, self.arduino.battery_off))

        # self.test_queue.append((10, self.load_file_text, "instructions.md"))

        # self.test_queue.append((1, self.arduino.test_indicator_off))

        # Start processing the queue
        self.process_queue()
        self.state = State.TESTING

    def process_queue(self) -> None:
        """Process the test queue."""
        if self.state == State.WAITING_FOR_BUTTON:
            # Waiting for the button to be pressed
            return
        elif self.state == State.WAITING_FOR_INPUT:
            # Waiting for an input
            return
        if self.test_queue:
            # Loop through the queue and execute the tasks
            delay, task, *args = self.test_queue.pop(0)
            QTimer.singleShot(
                delay, lambda: self.perform_task(task, args)
            )
            debug(
                f"Processing queue. {len(self.test_queue)} items left."
                f"Current state: {self.state}"
                f"Current queue item: Task:{task} Params:{args} Delay:{delay}ms"
            )
        else:
            # test is complete
            self.state = State.CONNECTED

    def wait_for_button(self, timeout: int = 20000) -> None:
        """Waiting for the test button to be pressed."""
        if self.state == State.TESTING:
            self.state = State.WAITING_FOR_BUTTON
            self.timeout_timer.start(timeout)
            
        if not self.button_pressed:
            # loop until the button is pressed
            QTimer.singleShot(100, self.wait_for_button)
            self.set_icon(self.test_button, 'forward-button')
        else:
            # button was pressed
            self.timeout_timer.stop()
            self.set_icon(self.test_button, 'test-button')
            self.button_pressed = False
            self.state = State.TESTING
            self.process_queue()

    def wait_for_input(self, pin: int, value: int, timeout: int) -> bool:
        """Wait for a pin input."""
        self.state = State.WAITING_FOR_INPUT
        self.arduino.attach_callback(self.input_callback, pin)
        self.timeout_timer.start(timeout)

    def input_callback(self, msg: str) -> None:
        pin = msg[0]
        value = msg[1]
        log.debug(f"Pin: {pin} Value: {value}")
        if self.state == State.WAITING_FOR_INPUT:
            self.timeout_timer.stop()
            self.state = State.TESTING
            self.process_queue()
        
    def on_timeout(self) -> None:
        """Called when the timeout timer times out."""
        if self.state == State.WAITING_FOR_BUTTON or self.state == State.WAITING_FOR_INPUT:
            self.state = State.TESTING
            self.button_pressed = True
            debug("Timeout.")
            self.insert_text("Timeout.")
            self.process_queue()

    def modify_settings(self) -> None:
        # if auto login is enabled, force the user to login
        if self.settings.get(KEY_AUTO_LOGIN):
            if self.authenticate():
                self.settings_dialog.show()
        else:
            self.settings_dialog.show()

    def authenticate(self) -> bool:
        """Authenticate via the login dialog."""
        self.loginDialog = LoginDialog(self.settings.get(KEY_LAST_USER))
        if self.loginDialog.exec() == QDialog.Accepted:
            success, username = self.loginDialog.ok()
            if success:
                self.settings.setValue(KEY_LAST_USER, username)
                self.app_settings.setValue(KEY_LAST_USER, username)
            else:
                critical(
                    self.loginDialog,
                    title="Invalid credentials",
                    message="The username or password you entered is incorrect. Please try again.",
                )
            return success
        else:
            return False
    
    # @Slot(Tuple[int, QObject])
    def on_settings_closed(self, result: Tuple) -> None:
        return_val, settings = result
        log.info(f"Settings dialog closed. Result: {return_val}")
        self.text_edit.setStyleSheet(
            f"color: {self.settings.get(KEY_FOREGROUND_COLOR)};"
            f"background-color: {self.settings.get(KEY_BACKGROUND_COLOR)};"
        )
        if self.settings.get(KEY_AUTO_LOGIN):
            self.actionLogout.setEnabled(False)
        else:
            self.actionLogout.setEnabled(True)
        if self.settings.get(KEY_FULLSCREEN):
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

            self.settings.load_settings()  # reload the settings
            chip = self.settings.get("chip_part")
            serial = self.settings.get("programmer_serial_number")

            command = [
                "C:\\Program Files (x86)\\ASIX\\UP\\up.exe",
                f"/part {chip}",
                f"/s {serial}",
                f"/p {self.eax_device.firmware_path}",
                "/q1",
            ]

            self.state = State.PROGRAMMING

            info(
                f"Programming {self.eax_device._selected_device}, args: {command}")

            self.program_thread = ProgrammingThread(command)
            self.program_thread.resultReady.connect(self.process_result)
            self.program_thread.start()

    def process_result(self, returncode=0) -> None:
        # This function gets called when the command finishes.
        # Do whatever you need to do with the return code here.
        if returncode == 0:
            self.insert_text("Programming successful.")
            log_info(
                f"Programming {self.eax_device._selected_device} successful")
            logg.success(
                f"Programming {self.eax_device._selected_device} successful")
            if self.settings.get(KEY_AUTO_TEST):
                # self.state = State.TESTING
                self.execute_test()
                return
        elif returncode == 2:
            error(
                f"Programming {self.eax_device._selected_device} failed. Error code: {returncode} (Check Programmer Serial Number?)")
        elif returncode == 7:
            error(
                f"Programming {self.eax_device._selected_device} failed. Error code: {returncode} (Check chip part number)")
        else:
            error(
                f"Programming {self.eax_device._selected_device} failed. Error code: {returncode}")

        if self.arduino:
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
        self.save_worker.progress_changed.connect(
            self.progress_bar.update_progress)
        self.save_worker.started.connect(self.progress_bar.show)
        self.save_worker.finished.connect(self.on_save_finished)
        self.save_worker.start()

    def on_save_finished(self) -> None:
        log.info("Save finished.")
        self.progress_bar.close()

    def perform_login(self) -> None:
        """Show the login dialog."""
        success, username = False, None
        # Block until the user is logged in
        while not success and self.window().isVisible():
            self.loginDialog = LoginDialog(self.settings.get(KEY_LAST_USER))
            if self.loginDialog.exec() == QDialog.Accepted:
                success, username = self.loginDialog.ok()
                if not success:
                    critical(
                        self.loginDialog,
                        "The username or password you entered is incorrect. Please try again.",
                        "Invalid credentials",
                    )
            else:
                self.close()
        if success:
            if self.settings.get_bool(KEY_AUTO_CONNECT):
                # Auto Connect
                QTimer.singleShot(1000, self.connect_device)
            log.success(f"Logged in as: {username}")
            logg.success(f"Logged in as: {username}")
            app_logger.info(f"Logged in as: {username}")

            # Block if the user is not an admin
            self.actionModify_Settings.setEnabled(db.is_admin(username))
            self.actionAdd_User.setEnabled(db.is_admin(username))
            self.actionRemove_User.setEnabled(db.is_admin(username))
            self.actionUpdate_Firmware.setEnabled(db.is_admin(username))
            # save the last user to the settings
            self.settings.setValue(KEY_LAST_USER, username)
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
            logg.info("Application closed.")
            app_logger.info("Application closed.")
            self.app_settings.setValue("geometry", self.saveGeometry())
            self.app_settings.setValue("windowState", self.saveState())
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

        # force the user to login if auto login is enabled
        if self.settings.get(KEY_AUTO_LOGIN):
            if not self.authenticate():
                return

        self.state = State.UPDATING

        self.device_label.setText("Firmware Update...")
        info("Updating firmware...")
        self.disconnected = False
        if self.arduino:
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

    def on_error(self, error: QProcess.ProcessError) -> None:
        log.error("An error occurred: ", error)
        log.error("System reported: ", self.update_process.errorString())
        app_logger.error("Firmware update failed: ", error)
        logg.critical("Firmware update failed: ", error)

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
            log.error("Process did not terminate in time.")


class ManualWidget(QWidget, Ui_ManualControlDialog):
    """
    Manual control dialog. This dialog allows the user to manually control the
    pins of the USB device.

    :param usb_handler: The USB connection handler.
    """

    def __init__(self, usb_handler: USBDevice = None):
        super().__init__()
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        if get_theme() == "dark":
            self.setStyleSheet(qdarkstyle.load_stylesheet(palette=DarkPalette))
        else:
            self.setStyleSheet(
                qdarkstyle.load_stylesheet(palette=LightPalette))

        self.usb_device = usb_handler

        if self.usb_device is None or not self.usb_device.connected:
            warning(self, f"USB device not connected.")
            self.close()
            return
        self.usb_device.attach_callback(self.callback)
        self.battery_button.clicked.connect(self.toggle_battery)
        self.low_battery_button.clicked.connect(self.toggle_low_battery)
        self.test_indicator_button.clicked.connect(
            self.toggle_testing_indicator)
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
            if self.usb_device.connected:
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
    saved = Signal(Any)

    def __init__(self, parent: MainWindow = None):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setupUi(self)
        self.app_settings = QSettings("Detex Corp", "EAX Interface")
        self.settings: ApplicationSettings = parent.settings
        self._parent = parent

        self.background_color: QColor = None
        self.foreground_color: QColor = None
        self.qfont: QFont = None

        self.pushButton_background_color.clicked.connect(
            self.pick_background_color)
        self.pushButton_foreground_color.clicked.connect(self.pick_color)
        self.pushButton_change_font.clicked.connect(self.change_font)

        self.pushButton_save.clicked.connect(self.save_changes)
        self.pushButton_default.clicked.connect(self.reset_to_default)

        self.apply_changes()

        # Set the theme
        self.setStyleSheet(get_stylesheet())

    def apply_changes(self) -> None:
        config = ConfigLoader()
        
        self.lineEdit_serial.setText(
            self.app_settings.value(KEY_PROGRAMMER_SERIAL_NUMBER, config.get_default_setting(KEY_PROGRAMMER_SERIAL_NUMBER))
        )
        
        chip_options = config.chip_options
        for chip_part in chip_options:
            self.comboBox_chip.addItem(chip_part)

        self.comboBox_chip.setCurrentText(
            self.app_settings.value(KEY_CHIP_PART, config.get_default_setting(KEY_CHIP_PART))
        )

        value = self.settings.get_int(KEY_TESTING_SPEED, config.get_default_setting(KEY_TESTING_SPEED))
        self.dial.setValue(value)

        self.comboBox_com_port.setCurrentText(
            self.app_settings.value(KEY_COM_PORT, config.get_default_setting(KEY_COM_PORT))
        )

        for port in USBDevice.get_usb_ports():
            self.comboBox_com_port.addItem(port)
        
        self.spinBox_autologoff_delay.setValue(
            self.settings.get_int(KEY_LOGOFF_DELAY, config.get_default_setting(KEY_LOGOFF_DELAY))
        )

        self.spinBox_arduino_id.setValue(
            self.settings.get_int(KEY_ARDUINO_INSTANCE_ID, config.get_default_setting(KEY_ARDUINO_INSTANCE_ID))
        )

        self.checkBox_test.setChecked(
            self.settings.get_bool(KEY_AUTO_TEST, config.get_default_setting(KEY_AUTO_TEST))
        )

        self.checkBox_connect.setChecked(
            self.settings.get_bool(KEY_AUTO_CONNECT, config.get_default_setting(KEY_AUTO_CONNECT))
        )

        self.checkBox_debug.setChecked(self.settings.get_bool(KEY_DEBUG, config.get_default_setting(KEY_DEBUG)))

        self.checkBox_logon.setChecked(
            self.settings.get_bool(KEY_AUTO_LOGIN, config.get_default_setting(KEY_AUTO_LOGIN))
        )

        self.checkBox_auto_find.setChecked(
            self.settings.get_bool(KEY_AUTO_FIND, config.get_default_setting(KEY_AUTO_FIND))
        )

        self.checkBox_shutdown_on_exception.setChecked(
            self.settings.get_bool(KEY_SHUTDOWN_ON_EXCEPTION, config.get_default_setting(KEY_SHUTDOWN_ON_EXCEPTION))
        )

        self.lineEdit_serial_sleep_tune.setText(
            str(self.app_settings.value(KEY_SLEEP_TUNE, config.get_default_setting(KEY_SLEEP_TUNE)))
        )

        self.spinBox_wait_time.setValue(
            self.settings.get_int(KEY_ARDUINO_WAIT, config.get_default_setting(KEY_ARDUINO_WAIT))
        )

        self.checkBox_fullscreen.setChecked(
            self.settings.get_bool(KEY_FULLSCREEN, config.get_default_setting(KEY_FULLSCREEN))
        )

        self.checkBox_touchscreen.setChecked(
            self.settings.get_bool(KEY_TOUCHSCREEN_ENABLED, config.get_default_setting(KEY_TOUCHSCREEN_ENABLED))
        )
        
        self.checkBox_frameless.setChecked(
            self.settings.get_bool(KEY_FRAMELESS, config.get_default_setting(KEY_FRAMELESS))
        )


    def reset_to_default(self) -> None:
        config = ConfigLoader()
        default_settings = config.settings

        self.comboBox_com_port.setCurrentText(default_settings[KEY_COM_PORT])
        self.lineEdit_serial.setText(default_settings[KEY_PROGRAMMER_SERIAL_NUMBER])
        self.comboBox_chip.setCurrentText(default_settings[KEY_CHIP_PART])
        self.dial.setValue(default_settings[KEY_TESTING_SPEED])
        self.checkBox_test.setChecked(default_settings[KEY_AUTO_TEST])
        self.checkBox_logon.setChecked(default_settings[KEY_AUTO_LOGIN])
        self.checkBox_connect.setChecked(default_settings[KEY_AUTO_CONNECT])
        self.spinBox_arduino_id.setValue(default_settings[KEY_ARDUINO_INSTANCE_ID])
        self.checkBox_debug.setChecked(default_settings[KEY_DEBUG])
        self.spinBox_autologoff_delay.setValue(default_settings[KEY_LOGOFF_DELAY])
        self.spinBox_wait_time.setValue(default_settings[KEY_ARDUINO_WAIT])
        self.checkBox_shutdown_on_exception.setChecked(default_settings[KEY_SHUTDOWN_ON_EXCEPTION])
        self.checkBox_auto_find.setChecked(default_settings[KEY_AUTO_FIND])
        self.lineEdit_serial_sleep_tune.setText(str(default_settings[KEY_SLEEP_TUNE]))
        self.checkBox_fullscreen.setChecked(default_settings[KEY_FULLSCREEN])
        self.checkBox_touchscreen.setChecked(default_settings[KEY_TOUCHSCREEN_ENABLED])
        self.checkBox_frameless.setChecked(default_settings[KEY_FRAMELESS])

        # defaults = [DEFAULT_SETTINGS[key] for key in DEFAULT_SETTINGS.keys()]
        # self.comboBox_com_port.setCurrentIndex(0)
        # self.lineEdit_serial.setText(defaults[1])
        # self.comboBox_chip.setCurrentIndex(CHIP_OPTIONS.index(defaults[2]))
        # self.dial.setValue(int(defaults[4]))
        # self.checkBox_test.setChecked(defaults[5])
        # self.checkBox_logon.setChecked(defaults[9])
        # self.checkBox_connect.setChecked(defaults[10])
        # self.spinBox_arduino_id.setValue(defaults[11])
        # self.checkBox_debug.setChecked(defaults[12])
        # self.spinBox_autologoff_delay.setValue(defaults[14])
        # self.spinBox_wait_time.setValue(defaults[17])
        # self.checkBox_shutdown_on_exception.setChecked(defaults[18])
        # self.checkBox_auto_find.setChecked(defaults[19])
        # self.lineEdit_serial_sleep_tune.setText(str(defaults[20]))
        # self.checkBox_fullscreen.setChecked(defaults[21])
        # self.checkBox_touchscreen.setChecked(defaults[22])
        # self.checkBox_frameless.setChecked(defaults[23])

    def save_changes(self) -> None:
        if self.background_color:
            self.settings.setValue(KEY_BACKGROUND_COLOR,
                              self.background_color.name())
        if self.foreground_color:
            self.app_settings.setValue(KEY_FOREGROUND_COLOR,
                              self.foreground_color.name())
        if self.qfont:
            self.settings.setValue(KEY_FONT_FAMILY, QFontInfo(self.qfont).family())
            self.settings.setValue(KEY_FONT_SIZE, QFontInfo(self.qfont).pointSize())
            self.settings.setValue(KEY_FONT_WEIGHT, QFontInfo(self.qfont).weight())
        self.settings.setValue(
            KEY_COM_PORT, self.comboBox_com_port.currentText())
        self.settings.setValue(
            KEY_CHIP_PART, self.comboBox_chip.currentText())
        self.settings.setValue(
            KEY_PROGRAMMER_SERIAL_NUMBER, self.lineEdit_serial.text()
        )
        self.settings.setValue(
            KEY_AUTO_TEST, self.checkBox_test.isChecked())
        self.settings.setValue(
            KEY_AUTO_CONNECT, self.checkBox_connect.isChecked())
        self.settings.setValue(KEY_DEBUG, self.checkBox_debug.isChecked())
        self.settings.setValue(
            KEY_AUTO_LOGIN, self.checkBox_logon.isChecked())
        self.settings.setValue(
            KEY_ARDUINO_INSTANCE_ID, self.spinBox_arduino_id.value()
        )
        self.settings.setValue(KEY_TESTING_SPEED, self.dial.value())
        self.settings.setValue(
            KEY_LOGOFF_DELAY, self.spinBox_autologoff_delay.value()
        )
        self.settings.setValue(
            KEY_AUTO_FIND, self.checkBox_auto_find.isChecked())
        self.settings.setValue(
            KEY_SHUTDOWN_ON_EXCEPTION, self.checkBox_shutdown_on_exception.isChecked()
        )
        self.settings.setValue(
            KEY_SLEEP_TUNE, float(self.lineEdit_serial_sleep_tune.text())
        )
        self.settings.setValue(
            KEY_ARDUINO_WAIT, self.spinBox_wait_time.value())
        self.settings.setValue(
            KEY_FULLSCREEN, self.checkBox_fullscreen.isChecked())
        self.settings.setValue(
            KEY_TOUCHSCREEN_ENABLED, self.checkBox_touchscreen.isChecked())
        self.settings.setValue(KEY_TOUCHSCREEN_ENABLED,
                          self.checkBox_touchscreen.isChecked())
        self.settings.setValue(KEY_FRAMELESS, self.checkBox_frameless.isChecked())
        self.saved.emit((0, self))
        self.close()

    def pick_color(self, *args) -> None:
        print(args)
        self.foreground_color = self.choose_color(
            self.settings.get(KEY_FOREGROUND_COLOR, "#ffffff"))
        log.debug(f"User selected color: {self.foreground_color.name()}")

    def pick_background_color(self, *args) -> None:
        print(args)
        self.background_color = self.choose_color(
            self.settings.get(KEY_BACKGROUND_COLOR, "#000000"))
        log.debug(f"User selected color: {self.background_color.name()}")

    def choose_color(self, color_name: str) -> QColor:
        new_color = QColorDialog.getColor(color_name)
        if new_color.isValid():
            return new_color
        else:
            return QColor(color_name)

    def change_font(self) -> None:
        ok, font = get_font([
            self.settings.get(KEY_FONT_FAMILY, self._parent.font().family()),
            self.settings.get_int(KEY_FONT_SIZE, self._parent.font().pointSize()),
            self.settings.get_int(KEY_FONT_WEIGHT, self._parent.font().weight())
        ])
        if ok:
            print(font)
            self.qfont = font

    def closeEvent(self, event) -> None:
        # self.settings.load_settings()
        self.saved.emit((0, self))
        self.destroy()
        event.accept()

    def keyPressEvent(self, event) -> None:
        key = event.key()

        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_F2:
            take_screenshot()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.activateWindow()
        self.setFocus()


class UserAdditionDialog(QDialog, Ui_AddUserDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.setStyleSheet(get_stylesheet())

        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

        self.users = db.get_users()

    def save(self) -> None:
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        admin = self.checkBox.isChecked()
        if not db.insert_user(username=username, password=password, is_admin=admin):
            warning(self, "Error adding user.")
        self.close()


class UserRemovalDialog(QDialog, Ui_RemoveUserDialog):
    def __init__(self, title="Remove User"):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.setWindowTitle(title)

        if get_theme() == "dark":
            self.setStyleSheet(qdarkstyle.load_stylesheet(palette=DarkPalette))
        else:
            self.setStyleSheet(
                qdarkstyle.load_stylesheet(palette=LightPalette))

        self.us = db.get_users()
        for username in self.us:
            self.comboBox.addItem(username)

        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

    def save(self):
        selected_username = self.comboBox.currentText()
        if selected_username == "dmh":
            critical(
                self,
                f"Cannot remove user: {selected_username}",
            )
            self.close()
            return
        db.remove_user(selected_username)


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

    def run(self):
        logg.clear_all_logs()
        for entry in self.data:
            log_entry = f"{entry['timestamp']} - logger - {entry['level']} - {entry['message']}"
            log.info(log_entry)
            logg.insert_log(entry['timestamp'], "logger",
                            entry['level'], entry['message'])
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
        self.setStyleSheet(get_stylesheet())

    def update_progress(self, value: int) -> None:
        self.progressBar.setValue(value)
        if value == 100:
            self.close()


class ProgrammingThread(QThread):
    resultReady = Signal(int)

    def __init__(self, command: List[str]):
        super(ProgrammingThread, self).__init__()
        self.command = command

    def run(self) -> None:
        debug(f"Running command: {self.command}")
        debug(" ".join(self.command))
        process = subprocess.run(self.command, shell=True)
        self.resultReady.emit(process.returncode)
        super(ProgrammingThread, self).exec()


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


if __name__ == "__main__":
    with log.catch(
        message="Encountered exception from main.",
        reraise=True,
        exception=BaseException,
    ):
        app = SingleInstanceApp(sys.argv)
        debug("Checking for running instances")
        if app.is_running:
            log.critical(
                "Another instance of the application is already running.")
            critical(
                None,
                "Another instance of the application is already running.",
            )
            sys.exit(1)
        
        # Validate the config file
        (valid, missing_keys) = config_loader.validate_config('config.yaml')
        if not valid:
            critical(None, f"Missing the following keys in config file:\n  {', '.join(missing_keys)}")
            sys.exit(1)
            
        window = MainWindow(app)
        window.show()
        info("Application started.")
        app.exec()
