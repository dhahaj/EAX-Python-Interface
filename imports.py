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
)
from qtpy.QtWidgets import (
    QApplication,
    QMessageBox,
    QWidget,
    QFontDialog,
    QFileDialog,
)
# from ui import (
#     Ui_MainWindow,
#     Ui_AddUserDialog,
#     Ui_RemoveUserDialog,
#     Ui_HelpDialog,
#     Ui_LogView,
#     Ui_Settings,
#     Ui_LoginDialog,
#     Ui_ManualControlDialog,
#     Ui_ProgressBar,
#     Ui_StatusBarWidget
# )
import qdarkstyle
from qdarkstyle import DarkPalette, LightPalette
from settings import ApplicationSettings
from constants import *
import subprocess
import os
from typing import List, Tuple, Union, overload
# from globals import logger as log

"""
Set the QT_API environment variable to "pyside6" to use PySide6
"""
os.environ["QT_API"] = 'pyside6'


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
