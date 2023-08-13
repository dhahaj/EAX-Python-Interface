import json
import os

from PySide6.QtCore import QJsonDocument
from PySide6.QtCore import QSettings
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
        # self.app_settings.setDefaultFormat(QSettings.IniFormat)

        # Default settings
        self.default_settings = DEFAULT_SETTINGS.copy()

        # Load settings from file
        self.load_settings()

    def get(self, key, default_value=None):
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

    def get_bool(self, key) -> bool:
        return_val = self.app_settings.value(key)
        if return_val is None:
            return False
        elif type(return_val) == str:
            return return_val.lower().strip(" ") in ["true", "yes", "1"]
        else:
            return bool(return_val)

    def set(self, key, value):
        """
        Set a setting.

        :param key: The key of the setting.
        :param value: The value of the setting.
        """
        self.app_settings.setValue(key, value)
        self.default_settings[key] = value
        self.save_settings()

    @log.catch(
        message="Settings file is invalid, resetting to default.",
        reraise=True,
        exception=json.JSONDecodeError,
    )
    def load_settings(self):
        """
        Load the settings from a JSON file.
        """
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

    def save_settings(self):
        """Save the settings to a JSON file."""
        with open(self.filename, "w") as file:
            json.dump(self.default_settings, file, indent=4)
        self.load_settings()  # Reload the settings

    def get_settings_path(self):
        return os.path.abspath(self.filename)

    def validate_settings(self):
        """Check if the settings file exists."""
        return os.path.exists(self.filename)

    @staticmethod
    @log.catch(
        message="Settings file is invalid, resetting to default.",
        reraise=True,
        exception=json.JSONDecodeError,
    )
    def read_settings_from_file(filename="settings.json"):
        values = DEFAULT_SETTINGS.copy()
        if os.path.exists(filename):
            with open(os.path.join(".", filename), "r") as file:
                values.update(json.load(file))
        else:
            log.warning(f"Settings file {filename} does not exist.")
        return values


def signal(obj):
    print(obj)


def export_qsettings_to_json(settings, filename):
    data = {}
    for key in settings.allKeys():
        value = settings.value(key)
        if isinstance(value, QByteArray):
            value = "QByteArray:" + value.data().decode("ISO-8859-1")
        data[key] = value

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def import_from_json_to_qsettings(filename, settings):
    with open(filename, "r") as file:
        data = json.load(file)

    for key, value in data.items():
        if isinstance(value, str) and value.startswith("QByteArray:"):
            byte_value = value[len("QByteArray:") :].encode("ISO-8859-1")
            value = QByteArray(byte_value)
        settings.setValue(key, value)


def read_array():
    array = []
    settings = ApplicationSettings()
    app_settings = settings.app_settings
    keys = list(DEFAULT_SETTINGS.keys())
    size = app_settings.beginReadArray("settings")
    for i in range(size):
        key = keys[i]
        app_settings.setArrayIndex(i)
        array.append(app_settings.value(key))
        # print(app_settings.value(key))
    app_settings.endArray()
    return array


from PySide6.QtCore import QByteArray

if __name__ == "__main__":
    settings = ApplicationSettings()
    app_settings = settings.app_settings
    keys = []
    values = []
    dict_ = {}
    for key in settings.app_settings.allKeys():
        value = settings.app_settings.value(key)
        # print(key, settings.app_settings.value(key))
        keys.append(key)
        values.append(value)

        if type(value) != QByteArray:
            # dict_.update({key: settings.app_settings.value(key).data().decode()})
            dict_.update({key: value})
        elif type(value) == str:
            dict_.update({key: value.data().decode("ISO-8859-1")})
        else:
            dict_.update({key: value.data().decode("ISO-8859-1")})

    # with open("temp.json", "w") as file:
    #     json.dump(dict_, file, indent=4)
    # print(dict_)
    # with open("temp.json", "w") as file:
    #     data_string = settings.app_settings.value(key).data().decode('ISO-8859-1')
    #     json.dump({key: data_string}, file, indent=4)
    with open("temp.json", "r") as file:
        # loaded_data = json.load(file)
        content = json.loads(file.read())

    for key, value in content.items():
        if key == "geometry" or key == "windowState":
            b = QByteArray(value.encode("ISO-8859-1"))
            # b = bytearray(value, 'ISO-8859-1')
            print(f"{key}: {b}")
        else:
            print(f"{key}: {value}")

    # export_qsettings_to_json(app_settings, "temp2.json")
    # a = read_array()
    # print(a)

    # import_from_json_to_qsettings("temp2.json", app_settings)s

    # recent_files = DEFAULT_SETTINGS
    # app_settings.beginWriteArray("settings")
    # for i, key in enumerate(recent_files):
    #     name = recent_files.get(key)
    #     print(key)
    #     app_settings.setArrayIndex(i)
    #     app_settings.setValue(key, name)
    # app_settings.endArray()
    # app_settings.sync()
    # app_settings.beginGroup("MainWindow")
    # app_settings.setValue("size", "1024x768")
    # app_settings.setValue("fullscreen", False)
    # app_settings.endGroup()
