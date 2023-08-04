import json
import os
from constants import *
from loguru import logger as log

class ApplicationSettings:
    """ The settings class, used to store settings. """

    def __init__(self, filename="settings.json"):
        """
        Initialize the settings class.

        :param filename: The name of the settings file.
        """
        self.filename = filename

        # Default settings
        self.settings = DEFAULT_SETTINGS.copy()

        # Load settings from file
        self.load_settings()

    def get(self, key):
        """
        Get a setting.

        :param key: The key of the setting.
        :return: The value of the setting.
        """
        return self.settings.get(key)

    def set(self, key, value):
        """
        Set a setting.

        :param key: The key of the setting.
        :param value: The value of the setting.
        """
        self.settings[key] = value
        self.save_settings()

    @log.catch(message="Settings file is invalid, resetting to default.", reraise=True, exception=json.JSONDecodeError)
    def load_settings(self):
        """
        Load the settings from a JSON file.
        """

        # Check if the settings file exists, and create it if it doesn't
        if not self.validate_settings():
            with open(os.path.join(".", self.filename), "w") as file:
                json.dump(DEFAULT_SETTINGS, file, indent=4)

        # Load the settings from the settings file
        with open(self.filename, "r") as file:
            self.settings.update(json.load(file))

        # Check if the settings file is valid
        # if not self.validate():
        #     log.error("Settings file is invalid, resetting to default.")
        #     self.settings = DEFAULT_SETTINGS
        # self.save()    

        # try:
        #     # Check if the settings file exists, and create it if it doesn't
        #     if not os.path.exists(self.filename):
        #         with open(os.path.join(".", self.filename), "w") as file:
        #             json.dump(self.settings, file, indent=4)

        #     # Load the settings from the settings file
        #     with open(self.filename, "r") as file:
        #         self.settings.update(json.load(file))
        # except json.JSONDecodeError:
        #     # self.settings = DEFAULT_SETTINGS
        #     self.save()

    def save_settings(self):
        """ Save the settings to a JSON file. """
        with open(self.filename, "w") as file:
            json.dump(self.settings, file, indent=4)
        self.load_settings()  # Reload the settings

    def get_settings_path(self):
        """
        Get the path of the settings file.

        :return: The path of the settings file.
        """
        return os.path.abspath(self.filename)

    def validate_settings(self):
        """Check if the settings file exists."""
        return os.path.exists(self.filename)

    @staticmethod
    @log.catch(message="Settings file is invalid, resetting to default.", reraise=True, exception=json.JSONDecodeError)
    def read_settings_from_file(filename="settings.json"):
        values = DEFAULT_SETTINGS.copy()
        if os.path.exists(filename):
            with open(os.path.join(".", filename), "r") as file:
                values.update(json.load(file))
        else:
            log.warning(f"Settings file {filename} does not exist.")
        return values