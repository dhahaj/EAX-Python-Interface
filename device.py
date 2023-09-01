import os
import json
from constants import *
from loguru import logger as log
from typing import List, Dict, Any
from pathlib import Path


class Device:
    """ A class that contains the device information and maintains the current selected device. """

    def __init__(self, selected_device: str = None):
        self._selected_device = selected_device
        self.data = self.load_from_file()

    @property
    def selected_device(self) -> str:
        return self._selected_device

    @selected_device.setter
    def selected_device(self, value: str) -> None:
        self._selected_device = value

    @property
    def version(self) -> str:
        return self.version

    @property
    def firmware(self) -> str:
        for firmware in self.data.get(KEY_FIRMWARE):
            if firmware.get(KEY_FIRMWARE_BASENAME) == self.selected_device:
                return f'{self.data.get(KEY_PATH)}/{firmware.get(KEY_FIRMWARE_NAME)}'
        return None

    @firmware.setter
    def firmware(self, value: str) -> None:
        self.firmware = value

    @property
    def name(self) -> str:
        return self.selected_device

    @name.setter
    def name(self, value: str) -> None:
        self.selected_device = value

    @property
    def names(self) -> List[str]:
        return [firmware.get(KEY_FIRMWARE_BASENAME) for firmware in self.data.get(KEY_FIRMWARE)]

    @property
    def selected(self) -> bool:
        return self.selected_device is not None

    @property
    def path(self) -> str:
        return self.get_firmware()

    def get_firmware(self) -> str:
        """ Returns the path to the firmware file for the current device. """
        for firmware in self.data.get(KEY_FIRMWARE):
            if firmware.get(KEY_FIRMWARE_BASENAME) == self.selected_device:
                return f'{self.data.get(KEY_PATH)}/{firmware.get(KEY_FIRMWARE_NAME)}'
        return None

    def __str__(self) -> str:
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
    def load_from_file(self, filename: str="firmware.json") -> Dict[str, Any]:
        """Load the settings from a JSON file."""
        return json.loads(Path(filename).read_text())

    def verify_firmware(self) -> bool:
        """Verify the firmware is valid."""
        for firmware in self.data.get(KEY_FIRMWARE):
            filename = firmware.get(KEY_FIRMWARE_NAME)
            if not os.path.isfile(f'{self.data.get(KEY_PATH)}/{filename}'):
                return False
        return True
