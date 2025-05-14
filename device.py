import config_loader
from constants import *
from typing import List, Dict, Any


class Device:
    """ A class that contains the device information and maintains the current selected device. """
    config: config_loader.ConfigLoader | None = None

    def __init__(self, device_name: str = None, firmware: str = None, color: str = None) -> None:
        """ Initializes the device with the given name and firmware. """
        self._name = device_name
        self._firmware = firmware
        self._color = color
        self.config = config_loader.get_instance()

    @property
    def name(self) -> str:
        """ Returns the name of the current device."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """ Sets the name of the current device."""
        self._name = value

    @property
    def firmware(self) -> str:
        """ Returns the path to the firmware file for the current device."""
        return self.get_firmware()

    @firmware.setter
    def firmware(self, value: str) -> None:
        self._firmware = value

    @property
    def color(self) -> str:
        """ Returns the color of the current device."""
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        """ Sets the color of the current device."""
        self._color = value

    @property
    def is_selected(self) -> bool:
        """ Returns True if a device is selected, False otherwise."""
        return self._name is not None
    
    @property
    def firmware_path(self) -> str:
        """ Returns the path to the firmware file for the current device."""
        return self.get_firmware()

    def get_firmware(self) -> str:
        """ Returns the path to the firmware file for the current device. """
        if self._name is None:
            return None
        return f'{self.config.firmware_path}/{self._firmware}'
    
    def __str__(self) -> str:
        """ Returns a string representation of the device. """
        return f'{self._name if self._name else "No device selected."}, {self._firmware if self._firmware else "No firmware selected."}, {self._color if self._color else "No color selected."}'



def load_devices() -> List[Device]:
    """Load the devices from the config file."""
    config = config_loader.get_instance()
    names = config.device_names
    firmware = config.get_firmware()
    devices = []
    for name in names:
        device = next((d for d in firmware if d.get(KEY_DEVICE_NAME) == name), None)
        if device:
            devices.append(Device(name, device.get(KEY_DEVICE_FIRMWARE_FILE), device.get(KEY_DEVICE_COLOR)))
    return devices



if __name__ == '__main__':
    devices = load_devices()
    for device in devices:  
        print(device)