"""
    This file contains all the imports used in the project,
    global variables used throughout the project and some 
    utility functions used throughout the project.
"""
from qtpy import (
    QtCore,
    QtGui,
    QtWidgets,
)
from qtpy.QtGui import (
    QFont,
    QFontInfo,
    QColor,
    QPalette,
    QIcon,
    QPixmap,
    QMovie,
    QCursor,
    QAction,
    QKeyEvent,
    QShowEvent,
)
from qtpy.QtCore import (
    QCoreApplication,
    QMetaObject,
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
    QObject,
    QThread,
    Signal,
    QJsonDocument,
    QPropertyAnimation,
    QRect,
    QFileInfo,
    QDir,
    QFile,
    QDateTime,
    QTime,
    QRunnable,
    Slot,
)
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QColorDialog,
    QWidget,
    QFontDialog,
    QInputDialog,
    QLineEdit,
    QTableWidgetItem,
    QDialog,
    QMenu,
    QSplashScreen,
    QComboBox,
    QProgressBar,
    QLabel,
    QFileDialog,
    QStatusBar,
    QLCDNumber
)
from ui import (
    Ui_MainWindow,
    Ui_AddUserDialog,
    Ui_RemoveUserDialog,
    Ui_HelpDialog,
    Ui_LogView,
    Ui_Settings,
    Ui_LoginDialog,
    Ui_ManualControlDialog,
    Ui_ProgressBar,
    Ui_StatusBarWidget
)
import qdarkstyle
from qdarkstyle import DarkPalette, LightPalette
from device import Device
from settings import ApplicationSettings
# from applogger import AppLogger, Log, LogManager
from constants import *
# from loguru import logger as log
from applogger import AppLogger
import subprocess
import sys
import os
import atexit
import time
from typing import List, Dict, Tuple, Union, Optional, Any, overload
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum
import send2trash

"""
Set the QT_API environment variable to "pyside6" to use PySide6
"""
os.environ["QT_API"] = 'pyside6'



"""
Global variables
"""
# app_logger: AppLogger | None = None
# settings = ApplicationSettings()
# logg: LogManager | None = None
log: AppLogger = AppLogger()


"""
Utility functions
"""
@overload
def get_font(attr: QFont) -> Tuple[bool, QFont]: ...


@overload
def get_font(attr: List) -> Tuple[bool, QFont]: ...


def get_font(attr: Union[QFont, List]) -> Tuple[bool, QFont]:
    """ Returns the font from the given attribute. """
    if isinstance(attr, QFont):
        font = attr
    elif isinstance(attr, list):
        font = QFont(attr[0], attr[1], attr[2])
    else:
        return (False, None)

    return QFontDialog.getFont(font)


def clean_backups(directory: str, days: int = 7) -> None:
    """
    Removes files from the given directory (and its subdirectories) that are
    older than the specified number of days by moving them to the trash.

    Args:
        directory (str): The directory to clean.
        days (int, optional): The number of days to keep files. Defaults to 7.
    """
    cutoff = datetime.now() - timedelta(days=days)

    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            filepath = os.path.join(dirpath, file)

            # Get modified time and compare with cutoff
            file_modified_time = datetime.fromtimestamp(
                os.path.getmtime(filepath))

            if file_modified_time < cutoff:
                # Send to trash
                try:
                    send2trash.send2trash(filepath)
                    log.info(f"Moved to trash: {filepath}")
                except Exception as e:
                    log.critical(f"Failed to move to trash: {filepath}. Error: {e}")


def take_screenshot() -> None:
    """ Takes a screenshot of the current window. """
    obj = QApplication.activeWindow()

    screen = QtGui.QGuiApplication.primaryScreen()
    QtCore.QCoreApplication.processEvents()
    pixmap = screen.grabWindow(obj.winId())
    img = pixmap.toImage()
    QtCore.QCoreApplication.processEvents()
    fileName, _ = QFileDialog.getSaveFileName(
        obj,
        "Save Screenshot",
        "screenshot.png",
        "All Files (*);;Image Files (*.png)",
        "Image Files (*.png)",
        QFileDialog.Options()
    )
    if fileName:
        # Save the data to the specified filename
        img.save(fileName)
        path = os.path.abspath(fileName)
        subprocess.Popen(['explorer', '/select,', path], shell=False)
        subprocess.run(['cmd', '/C', f'"{fileName}"'], shell=False)
        print(path, fileName)



def get_theme(settings: ApplicationSettings) -> str:
    """ Returns the current theme. """
    return 'dark' if str_to_bool(settings.app_settings.value(KEY_DARK_THEME)) else 'light'


def get_stylesheet(settings: ApplicationSettings) -> str:
    """ Returns the stylesheet for the current theme. """
    palette = DarkPalette if get_theme(settings) == 'dark' else LightPalette
    return qdarkstyle.load_stylesheet(palette)


def debug(msg: str) -> None:
    """ Logs a debug message. """
    if log: log.debug(msg)
    # if app_logger: app_logger.debug(msg)


def error(msg: str) -> None:
    """ Logs an error message. """
    if log: log.error(msg)
    # if app_logger: app_logger.error(msg)
    # if logg: logg.log('ERROR', msg)


def log_info(msg: str) -> None:
    """ Logs an info message. """
    if log: log.log('INFO', msg)
    # if app_logger: app_logger.info(msg)
    # if logg: logg.log('INFO', msg)


def info(msg: str) -> None:
    """ Logs an info message. """
    if log: log.info(msg)
    # if app_logger: app_logger.info(msg)
    # if logg: logg.log('INFO', msg)



def str_to_bool(s: str) -> bool:
    """ Converts a string to a boolean value. """
    if s is None:
        return False
    return s.lower().strip(' ') in ['true', 'yes', '1'] if type(s) == str else bool(s)



@overload
def warning(message: str) -> QtWidgets.QMessageBox.StandardButton: ...

@overload
def warning(parent: QWidget, message: str, title: str = "Error") -> QtWidgets.QMessageBox.StandardButton: ...


def warning(attr: Union[str, QWidget], message: str, title: str = "Error") -> QtWidgets.QMessageBox.StandardButton:
    """ Displays a warning message box. """
    if isinstance(attr, str):
        return QMessageBox.warning(None, title, message, QMessageBox.StandardButton.Ok)
    return QMessageBox.warning(attr, title, message, QMessageBox.StandardButton.Ok)


@overload
def critical(message: str) -> QtWidgets.QMessageBox.StandardButton: ...

@overload
def critical(parent: QWidget, message: str, title: str = "Error") -> QtWidgets.QMessageBox.StandardButton: ...


def critical(attr: Union[str, QWidget], message: str, title: str = "Error") -> QtWidgets.QMessageBox.StandardButton:
    """ Displays a critical message box. """
    if isinstance(attr, str):
        return QMessageBox.critical(None, title, attr, QMessageBox.StandardButton.Ok)
    return QMessageBox.critical(attr, title, message, QMessageBox.StandardButton.Ok)
