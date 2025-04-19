import asyncio
from telemetrix_aio.telemetrix_aio import TelemetrixAIO
from config_loader import ConfigLoader
from settings import ApplicationSettings
from rich import print
from loguru import logger as log
from constants import *
from serial.tools import list_ports
from typing import List
from PySide6.QtCore import QObject, Signal
from enum import Enum


class PinMode(Enum):
    INPUT = 'input'
    OUTPUT = 'output'
    INPUT_PULLUP = 'input_pullup'

class Pin:
    def __init__(self, pin_number: int, mode: PinMode, function: str = None, pullup_enabled: bool = False):
        self.pin_number = pin_number
        self.mode = mode
        self.function = function
        self.pullup_enabled = pullup_enabled
        if self.mode == PinMode.OUTPUT and self.pullup_enabled:
            raise ValueError(
                "Pull-up resistors cannot be enabled for output pins.")

    async def configure(self, device: TelemetrixAIO, callback=None):
        if self.mode == PinMode.OUTPUT:
            await device.set_pin_mode_digital_output(self.pin_number)
        elif self.mode == PinMode.INPUT:
            await device.set_pin_mode_digital_input(self.pin_number, callback)
        elif self.mode == PinMode.INPUT_PULLUP:
            await device.set_pin_mode_digital_input_pullup(self.pin_number, callback)

    def __repr__(self):
        return f"Pin(pin_number={self.pin_number}, mode={self.mode}, function={self.function}, pullup_enabled={self.pullup_enabled})"


class AIODevice(QObject):
    """
    Asynchronous USB connection handler using TelemetrixAIO.
    This class no longer relies on threading.Thread; instead,
    it performs asynchronous connection and I/O with asyncio.
    """
    DEBOUNCE_TIME = 0.05
    # input_changed = Signal(list)

    def __init__(
        self,
        wait: int = 4,
        shutdown_on_exception: bool = True,
        sleep_tune: float = 1e-6,
        debug: bool = True,
    ):
        super().__init__()
        self.settings = ApplicationSettings()

        # Determine connection parameters from settings.
        if self.settings.get(KEY_AUTO_FIND):
            self.port = None
            self.arduino_instance_id = self.settings.get_int(
                KEY_ARDUINO_INSTANCE_ID)
        else:
            self.port = self.settings.get(KEY_COM_PORT)
            self.arduino_instance_id = None

        log.info(f'Port is set to {self.port}')
        self.shutdown_on_exception = shutdown_on_exception
        self.arduino_wait = wait
        self.sleep_tune = float(sleep_tune)  # Ensure a float.
        self.device_connected = False
        self.debug = debug
        self.input_pin = None
        self.callback = None
        self.pins: List[Pin] = ConfigLoader().pins
        self.inputs = []
        self.last_input_times = {}

        # Will hold the TelemetrixAIO instance.
        self.device = None

        print(
            f"[bold green]AIODevice[/bold green]\n"
            f"initialize with port: {self.port}\n"
            f"arduino_instance_id: {self.arduino_instance_id}\n"
            f"debug: {self.debug}\n"
            f"shutdown_on_exception: {self.shutdown_on_exception}\n"
            f"arduino_wait: {self.arduino_wait}\n"
            f"sleep_tune: {self.sleep_tune}\n"
            f"device_connected: {self.device_connected}\n"
        )

    async def async_connect(self, callback=None) -> None:
        """
        Asynchronously establish a connection to the Arduino via TelemetrixAIO.
        """
        try:
            # Instantiate the asynchronous Telemetrix device.
            self.device = TelemetrixAIO(
                com_port=self.port,
                arduino_instance_id=self.settings.get_int(
                    KEY_ARDUINO_INSTANCE_ID),
                arduino_wait=int(self.arduino_wait),
                shutdown_on_exception=self.shutdown_on_exception,
                sleep_tune=self.sleep_tune,
                autostart=False,
                close_loop_on_shutdown=False
            )
            # Await the connection—assuming TelemetrixAIO.connect() is an async method.
            await self.device.start_aio()

            # After connecting, load and configure pins.
            self.load_pin_configuration()
            self.device_connected = True
            await self.configure_pin_modes()

            # Notify via callback if provided.
            if callback:
                callback(self.device_connected, self.device.com_port)
        except Exception as e:
            log.exception(
                f'Exception occurred while connecting to device: {e}')
            # Notify via callback if provided.
            if callback:
                callback(False, e.args[0])
            self.device_connected = False

    async def async_disconnect(self):
        """
        Asynchronously disconnect from the Arduino device.
        """
        if self.device:
            await self.device.shutdown()
            # self.device = None
            self.device_connected = False

    async def input_callback(self, message) -> None:
        """
        Callback invoked when input changes on the Arduino.
        Expects message to be a list with at least 3 elements: [?, pin, value].
        """
        pin_number = message[1]
        value = message[2]
        print(
            self, f'Method: {self.input_callback.__name__}, Pin: {pin_number}, Value: {value}')
        if pin_number != self.input_pin:
            return

        # self.input_changed.emit([pin_number, value])
        if self.callback:
            self.callback([pin_number, value])

    def attach_callback(self, callback: callable, pin_number: int) -> None:
        """
        Attach a callback function to a specific pin.
        """
        self.callback = callback
        self.input_pin = pin_number

    def load_pin_configuration(self, filename='config.yaml') -> None:
        """
        Load pin configuration from a JSON file via the ConfigLoader.
        
        param filename: str - The name of the configuration file.
        """
        config = ConfigLoader(filename=filename)
        self.pins = config.pins

    async def configure_pin_modes(self):
        """ Configure the pin modes based on the loaded configuration. """
        for pin in self.pins:
            pin_obj = Pin(
                pin['pin_number'],
                PinMode(pin['io_mode']),
                pin.get('function') or None,
                pin.get('pullup_enabled') or False
            )

            log.debug(f'Configuring pin {pin_obj}')
            await pin_obj.configure(self.device, self.input_callback)

    # These methods delegate to the asynchronous device.

    def set_pin_mode_digital_output(self, pin_number: int):
        return self.device.set_pin_mode_digital_output(pin_number)

    def set_pin_mode_digital_input(self, pin_number: int, callback):
        return self.device.set_pin_mode_digital_input(pin_number, callback)

    def set_pin_mode_digital_input_pullup(self, pin_number: int, callback):
        return self.device.set_pin_mode_digital_input_pullup(pin_number, callback)

    async def digital_write(self, pin_number: int, value: int):
        await self.device.digital_write(pin_number, value)

    async def write_pin_by_func(self, pin_function, value) -> None:
        pin = self.get_pin_by_function(pin_function)
        if pin:
            await self.digital_write(pin, value)
        else:
            log.error(f'Pin with function {pin_function} not found.')

    def get_pin_by_function(self, function: str) -> int:
        """ Get a pin number by its function name. """
        return next(
            (pin['pin_number']
             for pin in self.pins if pin.get('function') == function), None
        )

    async def async_cleanup(self):
        """
        Asynchronously cleanup the Arduino instance.
        """
        try:
            if self.device:
                self.set_all_pins_to_value(0)
                await self.device.shutdown()
                self.device_connected = False
        except Exception as e:
            log.exception(f'Cleanup error: {e}')

    async def set_all_pins_to_value(self, value: int) -> None:
        for pin in self.pins:
            if pin.get('io_mode') == 'output':
                await self.digital_write(pin.get('pin_number'), value)

    def __str__(self) -> str:
        return f'AIODevice(port={self.port}, arduino_instance_id={self.arduino_instance_id}, device_connected={self.device_connected})'

    @staticmethod
    def get_usb_ports() -> List[str]:
        com_ports = []
        for port in list_ports.comports():
            if hasattr(port, 'pid') and hasattr(port, 'vid') and isinstance(port.pid, int) and isinstance(port.vid, int):
                com_ports.append(port.name)
        return com_ports

    @staticmethod
    def get_pin_configuration() -> List[str]:
        """
        Get the pin configuration from the settings.
        """
        config = ConfigLoader()
        return config.pins


if __name__ == "__main__":
    # Example usage
    device = AIODevice()
    asyncio.run(device.async_connect())
    print(asyncio.run(device.device._get_firmware_version()))
    print(type(device.pins))
    device.load_pin_configuration()
    asyncio.run(device.configure_pin_modes())
    asyncio.run(device.set_all_pins_to_value(0))
    print(device.get_pin_by_function('ac'))
    print(AIODevice.get_pin_configuration())
    asyncio.run(device.async_disconnect())
