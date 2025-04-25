import os
from PySide6.QtCore import QSettings
from typing import Any
import constants
from applogger import AppLogger, logger as log
import imports 

class ApplicationSettings():
    """The settings class, used to store settings."""

    def __init__(self, filename: str = "settings.ini"):
        self.app_settings: QSettings = QSettings(filename, QSettings.Format.IniFormat)
        self.filename = filename
        self.default_settings = constants.DEFAULT_SETTINGS.copy()
        self.log = log

    @property
    def path(self) -> str:
        return os.path.abspath(self.filename)

    def get(self, key: str, default_value=None) -> Any:
        """
        Get a setting.

        :param key: The key of the setting.
        :return: The value of the setting.
        """
        return_val = self.app_settings.value(key, default_value)
        if not return_val:
            return None
        elif type(return_val) == str:
            if return_val.lower().strip(" ") in ["true", "yes"]:
                return True
            elif return_val.lower().strip(" ") in ["false", "no"]:
                return False
        return return_val

    def get_str(self, key: str) -> str:
        return_val = self.app_settings.value(key)
        return "" if not return_val else str(return_val) if type(return_val) != str else return_val

    def get_int(self, key: str, default_value: int = None) -> int:
        return_val = self.app_settings.value(key, default_value)
        return 0 if not return_val else int(return_val) if type(return_val) != int else return_val

    def get_float(self, key: str, default_value: float = None) -> float:
        return_val = self.app_settings.value(key, default_value)
        print(f"get_float: {key} = {return_val}, type={type(return_val)}")
        return 0.0 if not return_val else float(return_val) if type(return_val) != float else return_val

    def get_bool(self, key: str, default_value: bool = False) -> bool:
        """ Get a boolean setting. """
        return_val = self.app_settings.value(key, default_value)
        if type(return_val) == str:
            return return_val.lower().strip(" ") in ["true", "yes", "1"]
        return return_val
        # return False if not return_val else return_val.lower().strip(" ") in ["true", "yes", "1"]

    def setValue(self, key: str, value: Any) -> None:
        """ Set a setting. """
        self.app_settings.setValue(key, value)
        self.save_settings()

    def save_settings(self) -> None:
        """Save the settings to a file."""
        self.app_settings.sync()

    def validate_settings(self):
        """Check if the settings file exists."""
        return os.path.exists(self.filename)

    def print_settings(self) -> None:
        """Print the settings."""
        for key in self.app_settings.allKeys():
            value = self.app_settings.value(key)
            self.log.debug(f"{key}: {value}, type={type(value)}")

    def readArray(self) -> list:
        array = []
        return array.append(self.app_settings.value(key) for key in self.app_settings.allKeys())

    def sync(self) -> None:
        self.app_settings.sync()

    def copy_to_settings(self, settings: QSettings) -> None:
        """Copy settings to another QSettings object."""
        for key in self.app_settings.allKeys():
            value = self.app_settings.value(key)
            settings.setValue(key, value)

    def copy_from_settings(self, settings: QSettings) -> None:
        """Copy settings from another QSettings object."""
        for key in settings.allKeys():
            value = settings.value(key)
            self.app_settings.setValue(key, value)

    def __str__(self) -> str:
        """Return a string representation of the settings."""
        settings_str = ""
        for key in self.app_settings.allKeys():
            value = self.app_settings.value(key)
            settings_str += f"{key}: {value}\n"
        return settings_str

from typing import List

def read_array() -> List:
    array = []
    settings = ApplicationSettings()
    app_settings = settings.app_settings
    keys = list(constants.DEFAULT_SETTINGS.keys())
    size = app_settings.beginReadArray("settings")
    for i in range(size):
        key = keys[i]
        app_settings.setArrayIndex(i)
        array.append(app_settings.value(key))
    app_settings.endArray()
    return array


if __name__ == "__main__":
    settings = ApplicationSettings()
    settings.print_settings()

