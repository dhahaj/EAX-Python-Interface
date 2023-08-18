import json
import os
from PySide6.QtCore import QJsonDocument
from PySide6.QtCore import QSettings
from PySide6.QtCore import QByteArray
from typing import Any
from loguru import logger as log

from constants import *


class ApplicationSettings:
    """The settings class, used to store settings."""

    def __init__(self, filename="settings.json"):
        """
        Initialize the settings class.

        :param filename: The name of the settings file.
        """
        self.filename = filename
        self.app_settings = QSettings("Detex Corp", "EAX Interface")

        # Default settings
        self.default_settings = DEFAULT_SETTINGS.copy()

        # Load settings from file
        self.load_settings()

    @property
    def path(self) -> str:
        return os.path.abspath(self.filename)

    def get(self, key: str, default_value=None) -> Any:
        """
        Get a setting.

        :param key: The key of the setting.
        :return: The value of the setting.
        """
        # return self.default_settings.get(key)
        return_val = self.app_settings.value(key)
        if return_val is None:
            return_val = self.default_settings.get(key, default_value)
        elif type(return_val) == str:
            if return_val == "true":
                return_val = True
            elif return_val == "false":
                return_val = False
        return return_val

    def get_str(self, key: str) -> str:
        return_val = self.app_settings.value(key)
        return "" if not return_val else str(return_val) if type(return_val) != str else return_val

    def get_int(self, key: str) -> int:
        return_val = self.app_settings.value(key)
        return 0 if not return_val else int(return_val) if type(return_val) != int else return_val

    def get_bool(self, key) -> bool:
        """ Get a boolean setting. """
        return_val = self.app_settings.value(key)
        return False if not return_val else return_val.lower().strip(" ") in ["true", "yes", "1"]

    def set(self, key: str, value: Any) -> None:
        """ Set a setting. """
        self.app_settings.setValue(key, value)
        self.default_settings[key] = value
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
                # json.dump(DEFAULT_SETTINGS, file, indent=4)
                file.write(json_data.decode("utf-8"))

        # Load the settings from the settings file
        with open(self.filename, "r") as file:
            content = file.read()
            # self.settings.update(json.loads(content))
            doc_from_file = QJsonDocument.fromJson(content.encode())
            s = doc_from_file.toVariant()
            self.default_settings.update(s)

    def save_settings(self) -> None:
        """Save the settings to a JSON file."""
        with open(self.filename, "w") as file:
            json.dump(self.default_settings, file, indent=4)

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


def signal(obj):
    print(obj)


def export_qsettings_to_json(settings, filename) -> None:
    data = {}
    for key in settings.allKeys():
        value = settings.value(key)
        if isinstance(value, QByteArray):
            value = "QByteArray:" + value.data().decode("ISO-8859-1")
        data[key] = value

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def import_from_json_to_qsettings(filename, settings) -> None:
    with open(filename, "r") as file:
        data = json.load(file)

    for key, value in data.items():
        if isinstance(value, str) and value.startswith("QByteArray:"):
            byte_value = value[len("QByteArray:"):].encode("ISO-8859-1")
            value = QByteArray(byte_value)
        settings.setValue(key, value)


def read_array() -> list:
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
