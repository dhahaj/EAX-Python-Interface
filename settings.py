import json
import os
from constants import *

class Settings:
    """Settings class for the GUI."""

    def __init__(self, filename="settings.json"):
        """
        Initialize the settings class.

        :param filename: The name of the settings file.
        """
        self.filename = filename

        # Default settings
        self.settings = DEFAULT_SETTINGS

        # Load settings from file
        self.load()

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
        self.save()

    def load(self):
        """
        Load the settings from a JSON file.
        """
        try:
            # Check if the settings file exists, and create it if it doesn't
            if not os.path.exists(self.filename):
                with open(os.path.join(".", self.filename), "w") as file:
                    json.dump(self.settings, file, indent=4)
            
            # Load the settings from the settings file
            with open(self.filename, "r") as file:
                self.settings.update(json.load(file))
        except json.JSONDecodeError:
            print("Failed to decode JSON from settings file.")
            # self.settings = DEFAULT_SETTINGS
            self.save()

    def save(self):
        """Save the settings to a JSON file."""
        with open(self.filename, "w") as file:
            json.dump(self.settings, file, indent=4)
        self.load() # Reload the settings

    def get_path(self):
        """
        Get the path of the settings file.

        :return: The path of the settings file.
        """
        return os.path.abspath(self.filename)
    
    def validate(self):
        """ Check if the settings file exists."""
        return os.path.exists(self.filename)
    