import json
import os
from PySide6.QtCore import QJsonDocument
from PySide6.QtCore import QSettings
from PySide6.QtCore import QByteArray
from typing import Any
from loguru import logger as log
from constants import *
# from imports import str_to_bool
from pathlib import Path

class ApplicationSettings():
    """The settings class, used to store settings."""

    def __init__(self, filename="settings.json"):
        QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, "./config")
        self.app_settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "Detex", "EAX Interface")
        self.filename = filename
        self.default_settings = DEFAULT_SETTINGS.copy()


    @property
    def path(self) -> str:
        return os.path.abspath(self.filename)

    def get(self, key: str, default_value=None) -> Any:
        """
        Get a setting.

        :param key: The key of the setting.
        :return: The value of the setting.
        """
        return_val = self.app_settings.value(key)
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

    def get_int(self, key: str) -> int:
        return_val = self.app_settings.value(key)
        return 0 if not return_val else int(return_val) if type(return_val) != int else return_val

    def get_bool(self, key: str) -> bool:
        """ Get a boolean setting. """
        return_val = self.app_settings.value(key)
        return False if not return_val else return_val.lower().strip(" ") in ["true", "yes", "1"]

    def setValue(self, key: str, value: Any) -> None:
        """ Set a setting. """
        self.app_settings.setValue(key, value)
        self.save_settings()

    @log.catch(
        message="Settings file is invalid, resetting to default.",
        reraise=True,
        exception=json.JSONDecodeError,
    )
    def load_settings(self) -> None:
        """ Load the settings from a JSON file. """
        # Check if the settings file exists, and create it if it doesn't
        if not self.validate_settings():
            # Convert the Python dictionary to a QJsonDocument
            json_doc = QJsonDocument.fromVariant(DEFAULT_SETTINGS)

            # Serialize the QJsonDocument to formatted string
            json_data = json_doc.toJson(QJsonDocument.JsonFormat.Indented)

            with open(os.path.join(".", self.filename), "w") as file:
                file.write(json_data.decode("utf-8"))

        # Load the settings from the settings file
        with open(self.filename, "r") as file:
            content = file.read()
            doc_from_file = QJsonDocument.fromJson(content.encode())
            s = doc_from_file.toVariant()
            self.default_settings.update(s)

    def save_settings(self) -> None:
        """Save the settings to a file."""
        self.app_settings.sync()
        # json.dumps(Path.read_text(self.filename), indent=4)
        # with open(self.filename, "w") as file:
        #     json.dump(self.default_settings, file, indent=4)
        #     file.readlines()
        #     json.loads()

    def validate_settings(self):
        """Check if the settings file exists."""
        return os.path.exists(self.filename)

    @staticmethod
    @log.catch(
        message="Settings file is invalid, resetting to default.",
        reraise=True,
        exception=json.JSONDecodeError,
    )
    def read_settings_from_file(filename="settings.json") -> dict:
        values = DEFAULT_SETTINGS.copy()
        if os.path.exists(filename):
            with open(os.path.join(".", filename), "r") as file:
                values.update(json.load(file))
        else:
            log.warning(f"Settings file {filename} does not exist.")
        return values

    def print_settings(self) -> None:
        """Print the settings."""
        self.app_settings.sync()
        for key in self.app_settings.allKeys():
            value = self.app_settings.value(key)
            if self.get_bool(KEY_DEBUG):
                log.debug(f"{key}: {value}, type={type(value)}")

    def readArray(self) -> list:
        array = []
        return array.append(self.app_settings.value(key) for key in self.app_settings.allKeys())
    
    def sync(self) -> None:
        self.app_settings.sync()


from typing import List

def read_array() -> List:
    array = []
    settings = ApplicationSettings()
    app_settings = settings.app_settings
    keys = list(DEFAULT_SETTINGS.keys())
    size = app_settings.beginReadArray("settings")
    for i in range(size):
        key = keys[i]
        app_settings.setArrayIndex(i)
        array.append(app_settings.value(key))
    app_settings.endArray()
    return array


if __name__ == "__main__":
    settings = ApplicationSettings()
    app_settings = settings.app_settings
