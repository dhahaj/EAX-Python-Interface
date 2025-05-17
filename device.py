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
        self._styles = self.config.label_styles
        self._font_size = self.config.label_font_size

    @property
    def name(self) -> str:
        """ Returns the name of the current device."""
        return self._device_name

    @property
    def styles(self) -> str:
        """Returns the styles of the current device."""
        return self._styles

    @property
    def font_size(self) -> str:
        """Returns the font size of the current device."""
        return self._font_size

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
        """Returns the path to the firmware file for the current device."""
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
    print(firmware)
    devices = []
    for name in names:
        device = next((entry for entry in firmware if entry.get(KEY_DEVICE_NAME) == name), None)
        print(device)
        if device:
            devices.append(Device(name, device.get(KEY_FIRMWARE_FILENAME), device.get(KEY_DEVICE_COLOR)))
    return devices


if __name__ == '__main__':
    devices = load_devices()
    for device in devices:
        print(device)
