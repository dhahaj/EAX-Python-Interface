import config_loader
from constants import *
from typing import List, Dict, Any


class Device:
    """ A class representing a device. """
    _device_name: str = None
    _firmware: str = None
    _label_color: str = None
    config: config_loader.ConfigLoader | None = None

    def __init__(self, device_name: str = None, firmware: str = None, label_color: str = None) -> None:
        """ Initializes the device with the given name and firmware. """
        self._device_name = device_name
        self._firmware = firmware
        self._label_color = label_color
        self.config = config_loader.get_instance()

    @property
    def name(self) -> str:
        """ Returns the name of the current device."""
        return self._device_name

    @name.setter
    def name(self, value: str) -> None:
        """ Sets the name of the current device."""
        self._device_name = value

    @property
    def firmware(self) -> str:
        """ Returns the path to the firmware file for the current device."""
        return self.get_firmware()

    # @firmware.setter
    # def firmware(self, value: str) -> None:
    #     self._firmware = value

    @property
    def label_color(self) -> str:
        """ Returns the color of the current device."""
        return self._label_color

    # @label_color.setter
    # def label_color(self, value: str) -> None:
    #     """ Sets the color of the current device."""
    #     self._label_color = value

    @property
    def is_selected(self) -> bool:
        """ Returns True if a device is selected, False otherwise."""
        return self._device_name is not None
    
    @property
    def firmware_path(self) -> str:
        """ Returns the path to the firmware file for the current device."""
        return self.get_firmware()

    def get_firmware(self) -> str:
        """ Returns the path to the firmware file for the current device. """
        if self._device_name is None:
            return None
        return f'{self.config.firmware_path}/{self._firmware}'
    
    def __str__(self) -> str:
        """ Returns a string representation of the device. """
        return f'{self._device_name if self._device_name else "No device selected."}, {self._firmware if self._firmware else "No firmware selected."}, {self._label_color if self._label_color else "No color selected."}'



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