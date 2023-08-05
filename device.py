import os
import json
from constants import *
from loguru import logger as log
"""EA
EBxW
EB
EAxLBM
EBxLBM
EA_ADV
EBxW_L9SI
EA_L9SI


104010-1
104010-3
104010-4
104010-5
104010-7
104010-8
104010-9
104010-10"""

class Device:
    """ A class that contains the device information and maintains the current selected device. """
    filename = 'firmware.json'
    def __init__(self, selected_device=None):
        self.selected_device = selected_device
        # self.version = None
        self.firmware = self.get_list_by_name('binaries')
        # self.set_version()
        self.models = self.get_list_by_name('models')
        self.data = []
        self.model = None
        self.load_from_file()

    def set_model(self, model):
        self.model = model

    def get_model(self):
        return self.model

    def set_name(self, name):
        self.selected_device = name

    def get_name(self):
        return self.selected_device

    def set_version(self):
        for firmware in FIRMWARES:
            if firmware[FIRMWARE_NAME] == self.selected_device:
                self.version = firmware[FIRMWARE_VERSION]
                break

    def get_firmware(self):
        """ Returns the firmware file name for the current device. """
        for firmware in self.data:
            if firmware['basename'] == self.selected_device:
                filename = firmware['filename']
                return f'firmware/{filename}'
        return None

    def get_names(self):
        """ Returns a list of all the device names. """
        return [firmware['basename'] for firmware in self.data]

    def __str__(self):
        return f'{self.selected_device}_{self.version}.hex'

    def __repr__(self):
        return f"{self.selected_device}_{self.version}.hex"

    def __eq__(self, other):
        if not isinstance(other, Device):  # suggestion 1
            return False
        return (
            self.selected_device == other.selected_device
            and self.version == other.version
        )

    @log.catch(
        message='Firmware json file is invalid, resetting to default.',
        reraise=True,
        exception=json.JSONDecodeError,
    )
    def load_from_file(self, filename='firmware.json'):
        """Load the settings from a JSON file."""
        with open(filename, 'r') as file:
            self.data = json.load(file)

    def get_list_by_name(self, name):
        """Return a list of firmware dictionaries by name."""
        with open(self.filename, 'r') as file:
            return json.load(file)[name]

    def verify_firmware(self):
        """Verify the firmware is valid."""
        for firmware in self.firmware:
            filename = firmware['filename']
            if not os.path.isfile(f'firmware/{filename}'):
                return False
        return True

    def get_model_names(self):
        """Return a list of model names."""
        return [model['name'] for model in self.models]