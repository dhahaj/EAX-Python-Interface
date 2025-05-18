import config_loader
from constants import KEY_DEVICE_NAME, KEY_FIRMWARE_FILENAME, KEY_DEVICE_COLOR
from typing import List, Dict, Any


class Device:
    """A class representing a device."""

    _device_name: str = None
    _firmware: str = None
    _label_color: str = None
    config: config_loader.ConfigLoader | None = None

    def __init__(self, device_name: str = None, firmware: str = None, label_color: str = None) -> None:
        """Initializes the device with the given name and firmware."""
        self._device_name = device_name
        self._firmware = firmware
        self._label_color = label_color
        self.config = config_loader.get_instance()
        self._styles = self.config.label_styles
        self._font_size = self.config.label_font_size

    @property
    def name(self) -> str:
        """Returns the name of the current device."""
        return self._device_name

    @property
    def styles(self) -> str:
        """Returns the styles of the current device."""
        return self._styles + f"color:{self._label_color};"

    @property
    def font_size(self) -> str:
        """Returns the font size of the current device."""
        return self._font_size

    @property
    def firmware(self) -> str:
        """Returns the path to the firmware file for the current device."""
        return self.get_firmware_path()

    @property
    def label_color(self) -> str:
        """Returns the color of the current device."""
        return self._label_color

    @property
    def firmware_path(self) -> str:
        """Returns the path to the firmware file for the current device."""
        return self.get_firmware_path()

    def get_firmware_path(self) -> str:
        """Returns the path to the firmware file for the current device."""
        if not self._device_name:
            return None
        return f'{self.config.firmware_path}/{self._firmware}'

    def __str__(self) -> str:
        """Returns a string representation of the device."""
        return (
            f'{self._device_name if self._device_name else "Device not selected."}'
            f'{self._firmware if self._firmware else "Firmware not selected."}',
            f'{self._label_color if self._label_color else "No label color defined."}',
        )


def load_devices() -> List[Device]:
    """Load the devices from the config file."""
    config = config_loader.get_instance()
    names = config.device_names
    firmware = config.get_firmware()
    device_list = []
    for name in names:
        device = next((entry for entry in firmware if entry.get(KEY_DEVICE_NAME) == name), None)
        if device:
            device_list.append(
                Device(name, device.get(KEY_FIRMWARE_FILENAME), device.get(KEY_DEVICE_COLOR))
            )
    return device_list


if __name__ == '__main__':
    devices = load_devices()
    for device in devices:
        print(device)
