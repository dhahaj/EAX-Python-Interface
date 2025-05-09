import os
import config_loader
from constants import *
from typing import List, Dict, Any


class Device:
    """ A class that contains the device information and maintains the current selected device. """
    config: config_loader.ConfigLoader | None = None

    def __init__(self, selected_device: str = None):
        self._selected_device = selected_device
        self.data: List[Dict[str, Any]] = None
        self._path: str = None
        self.config = config_loader.get_instance()
        self.load_from_config()

    @property
    def selected_device(self) -> str:
        """ Returns the name of the current device."""
        return self._selected_device

    @property
    def name(self) -> str:
        """ Returns the name of the current device."""
        return self.selected_device

    @name.setter
    def name(self, value: str) -> None:
        """ Sets the name of the current device."""
        self.selected_device = value

    @selected_device.setter
    def selected_device(self, value: str) -> None:
        self._selected_device = value

    @property
    def firmware(self) -> str:
        """ Returns the path to the firmware file for the current device."""
        return self.get_firmware()

    @firmware.setter
    def firmware(self, value: str) -> None:
        self.firmware = value

    @property
    def names(self) -> List[str]:
        """ Returns a list of all the device names."""
        return self.config.devices

    @property
    def is_selected(self) -> bool:
        """ Returns True if a device is selected, False otherwise."""
        return self.selected_device is not None

    @property
    def firmware_path(self) -> str:
        """ Returns the path to the firmware file for the current device."""
        return self.get_firmware()

    def get_firmware(self) -> str:
        """ Returns the path to the firmware file for the current device. """
        for firmware in self.data:
            if firmware.get(KEY_FIRMWARE_DEVICE_NAME) == self.selected_device:
                name = firmware.get(KEY_FIRMWARE_NAME)
                return f'{self._path}/{name}'
        return None

    def load_from_config(self) -> None:
        """Load the settings from a file."""
        self.data = self.config.get_firmware()
        self._path = self.config.firmware_path

    def verify_firmware(self) -> bool:
        """Verify the firmware is valid."""
        return_val = True
        for firmware in self.data:
            filename = firmware.get(KEY_FIRMWARE_NAME)
            if not os.path.isfile(f'{self._path}/{filename}'):
                print(f"Firmware file {filename} not found in {self._path}.")
                return_val = False
        return return_val
    
    def __str__(self) -> str:
        """ Returns a string representation of the device. """
        return self.selected_device if self.selected_device else "No device selected."


if __name__ == '__main__':
    dev = Device()
    print(dev)
    for d in dev.names:
        dev.name = d
        print(dev.name)
        print(dev.firmware)
        print(dev.firmware_path)
        print(dev.is_selected)
        print(dev.verify_firmware())
    dev.name = None
    print(dev.verify_firmware())