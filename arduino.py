import asyncio
from telemetrix_aio.telemetrix_aio import TelemetrixAIO
import config_loader
from settings import get_instance
from constants import (
    KEY_COM_PORT,
    KEY_AUTO_FIND,
    KEY_ARDUINO_INSTANCE_ID,
    KEY_SHUTDOWN_ON_EXCEPTION,
    KEY_ARDUINO_WAIT,
    KEY_SLEEP_TUNE,
    KEY_DEBUG,
    KEY_VIRTUAL_COM_PORT,
)
from serial.tools import list_ports
from typing import List
from PySide6.QtCore import QObject, Signal
from enum import Enum
from globals import logger as log
from collections import defaultdict


class Pin:

    class Mode(Enum):
        INPUT = 'input'
        OUTPUT = 'output'
        INPUT_PULLUP = 'input_pullup'

    def __init__(self, pin_number: int, mode: Mode, function: str = None, pullup_enabled: bool = False):
        self.pin_number = pin_number
        self.mode = mode
        self.function = function
        self.pullup_enabled = pullup_enabled
        if self.mode == Pin.Mode.OUTPUT and self.pullup_enabled:
            raise ValueError("Pull-up resistors cannot be enabled for output pins.")

    async def configure(self, device: TelemetrixAIO, callback=None):
        if self.mode == Pin.Mode.OUTPUT:
            await device.set_pin_mode_digital_output(self.pin_number)
        elif self.mode == Pin.Mode.INPUT:
            await device.set_pin_mode_digital_input(self.pin_number, callback)
        elif self.mode == Pin.Mode.INPUT_PULLUP:
            await device.set_pin_mode_digital_input_pullup(self.pin_number, callback)

    def __repr__(self):
        return f"Pin(pin_number={self.pin_number}, mode={self.mode}, function={self.function}, pullup_enabled={self.pullup_enabled})"


class AIODevice(QObject):
    """
    Asynchronous USB connection handler using TelemetrixAIO.
    This class no longer relies on threading.Thread; instead,
    it performs asynchronous connection and I/O with asyncio.
    """

    DEBOUNCE_TIME = 0.5  # seconds
    connection_changed = Signal(bool, object)

    def __init__(self):
        super().__init__()

        self.settings = get_instance()

        self._device_connected = False
        self.debug = self.settings.get_bool(KEY_DEBUG, False)
        self.input_pin = None
        self.callback = None

        self.pins: List[Pin] = []

        self.inputs = []

        # Will hold the TelemetrixAIO instance.
        self.device: TelemetrixAIO = None
        self.last_input_time = 0.0

    @property
    def device_connected(self) -> bool:
        return self._device_connected

    @device_connected.setter
    def device_connected(self, value: bool) -> None:
        if self._device_connected == value:
            return
        self._device_connected = value
        self.connection_changed.emit(value, self.device.com_port if value else "Disconnected")

    async def async_connect(self, callback=None) -> None:
        """Asynchronously establish a connection to the Arduino via TelemetrixAIO."""
        try:
            # Instantiate the asynchronous Telemetrix device.
            self.device = TelemetrixAIO(
                com_port=None if self.settings.get_bool(KEY_AUTO_FIND, True) else self.settings.get(KEY_COM_PORT, None),
                arduino_instance_id=self.settings.get_int(KEY_ARDUINO_INSTANCE_ID, 1),
                arduino_wait=self.settings.get_int(KEY_ARDUINO_WAIT, 4),
                shutdown_on_exception=self.settings.get(KEY_SHUTDOWN_ON_EXCEPTION, True),
                sleep_tune=self.settings.get_float(KEY_SLEEP_TUNE, 0.000001),
                autostart=False,
                close_loop_on_shutdown=False,
            )

            # Await the connection—assuming TelemetrixAIO.connect() is an async method.
            await self.device.start_aio()
            self.device_connected = True
            asyncio.create_task(self._monitor_connection(), name="monitor_connection")

            # After connecting, load and configure pins.
            self.load_pin_configuration()
            await self.configure_pin_modes()

            # Notify via callback if provided.
            if callback:
                callback(self._device_connected, self.device.com_port)

        except Exception as e:
            log.warning(f'Exception occurred while connecting to device: {e}')
            self.device_connected = False
            self.connection_changed.emit(self._device_connected, str(e))
            if callback:
                callback(self.device_connected, str(e))

    async def async_disconnect(self):
        """Asynchronously disconnect from the Arduino device."""
        if self.device:
            await self.device.shutdown()
            self.device_connected = False

    async def input_callback(self, message) -> None:
        """
        Callback invoked when input changes on the Arduino.
        Expects message to be a list with at least 3 elements: [timestamp, pin, value].
        """
        if message[0] == 2:
            # This is a digital input change.
            input_time = message[3]
            delta = input_time - self.last_input_time
            if delta < self.DEBOUNCE_TIME:
                # If the time since the last input is less than DEBOUNCE_TIME, ignore it.
                print(f"Debouncing input: {delta:.2f} seconds")
                return  # Only process if the time since the last input is greater than DEBOUNCE_TIME.
            self.last_input_time = input_time

        pin_number = message[1]
        value = message[2]
        log.debug(f'{self}: Method: {self.input_callback.__name__}, Pin: {pin_number}, Value: {value}')
        if pin_number != self.input_pin:
            return

    def attach_callback(self, callback: callable, pin_number: int) -> None:
        """
        Attach a callback function to a specific pin.
        """
        self.callback = callback
        self.input_pin = pin_number

    def load_pin_configuration(self) -> None:
        """Load pin configuration from a YAML file via the ConfigLoader."""
        config = config_loader.get_instance()
        self.pins = config.pins

    async def configure_pin_modes(self) -> None:
        """Configure the pin modes based on the loaded configuration."""
        for pin in self.pins:
            try:
                pin_obj = Pin(pin['pin_number'], Pin.Mode(pin['io_mode']), pin.get('function'), pin.get('pullup_enabled', False))
                log.debug(f'Configuring pin {pin_obj}')
                await pin_obj.configure(self.device, self.input_callback)
            except Exception as e:
                log.error(f"Failed to configure pin {pin}: {e}")

    def set_pin_mode_digital_output(self, pin_number: int) -> None:
        return self.device.set_pin_mode_digital_output(pin_number)

    def set_pin_mode_digital_input(self, pin_number: int, callback) -> None:
        return self.device.set_pin_mode_digital_input(pin_number, callback)

    def set_pin_mode_digital_input_pullup(self, pin_number: int, callback) -> None:
        return self.device.set_pin_mode_digital_input_pullup(pin_number, callback)

    async def digital_write(self, pin_number: int, value: int) -> None:
        # log.debug(f'{self.__class__.__name__}: Method: {self.digital_write.__name__}, Pin: {pin_number}, Value: {value}')
        await self.device.digital_write(pin_number, value)

    def start_monitoring(self) -> None:
        """Start monitoring the connection."""
        # Start the connection monitoring task.
        loop = asyncio.get_running_loop()
        loop.create_task(self._monitor_connection(), name="monitor_connection")

    async def _monitor_connection(self):
        """Periodically “ping” the board; on any exception assume the port died."""
        while self._device_connected:
            await asyncio.sleep(1)
            try:
                # log.debug("Pinging device...")
                await self.device.digital_write(14, 0)
                # log.debug("Heartbeat...")
            except Exception as e:
                log.warning("Arduino connection lost")
                self.device_connected = False
                break

    async def write_pin_by_func(self, pin_function: str, value: int) -> None:
        try:
            pin = self.get_pin_by_function(pin_function)
            log.debug(f'{self.__class__}, Method: {self.write_pin_by_func.__name__}, Pin function: {pin_function}, Pin: {pin}, Value: {value}')
            if pin is None:
                raise RuntimeError(f"No pin for {pin_function}")
            await self.digital_write(pin, value)
        except Exception as e:
            log.error(f"Write failed: {e}")
            self.device_connected = False
            raise

    def get_pin_by_function(self, function: str) -> int:
        """Get a pin number by its function name."""
        return next((pin['pin_number'] for pin in self.pins if pin.get('function') == function), None)

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

    async def ensure_connected(self) -> None:
        """Connect if not already connected."""
        if not self.device_connected:
            await self.async_connect()

    # def __str__(self) -> str:
    #     return f'AIODevice(port={self.device.com_port}, arduino_instance_id={self.arduino_instance_id}, device_connected={self._device_connected})'

    @staticmethod
    def get_usb_ports() -> List[str]:
        com_ports = []
        for port in list_ports.comports():
            if hasattr(port, 'pid') and hasattr(port, 'vid') and isinstance(port.pid, int) and isinstance(port.vid, int):
                com_ports.append(port.name)
        return com_ports

    @staticmethod
    def get_pin_configuration():
        """
        Get the pin configuration from the settings.
        """
        config = config_loader.get_instance()
        return config.pins


class DummyAIODevice(AIODevice):
    """
    Mock class for AIODevice to simulate behavior without actual hardware.
    This is useful for testing purposes.
    """

    class Device:
        com_port: str = "COM3"

    connection_changed = Signal(bool, object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._device_connected = True  # Simulate a connected device
        self.device = self.Device()
        self._pin_callbacks = defaultdict(lambda: lambda msg: None)  # Default to no-op callback

    async def write_pin_by_func(self, func, val):
        print(f"MOCK WRITE: Func={func}, Val={val}")

    async def digital_write(self, pin, val):
        print(f"MOCK WRITE: Pin={pin}, Val={val}")

    def get_pin_by_function(self, func):
        return {'relay in': 7}.get(func)  # Example

    def attach_callback(self, cb, pin):
        if self.debug:
            print(f"MOCK ATTACH: Pin={pin}, CB={cb}")
        self._pin_callbacks[pin] = cb

    def detach_callback(self, pin):
        self._pin_callbacks[pin] = lambda msg: None
        print(f"MOCK DETACH: Pin={pin}")

    async def async_connect(self, callback=None):
        print("MOCK CONNECT")

    async def async_disconnect(self):
        self._device_connected = False

    async def set_pin_mode_digital_output(self, pin):
        print(f"MOCK SET OUTPUT: Pin={pin}")

    async def set_pin_mode_digital_input(self, pin, cb):
        print(f"MOCK SET INPUT: Pin={pin}, CB={cb}")
        self._pin_callbacks[pin] = cb

    async def set_pin_mode_digital_input_pullup(self, pin, cb):
        print(f"MOCK SET INPUT PULLUP: Pin={pin}, CB={cb}")
        self._pin_callbacks[pin] = cb

    def load_pin_configuration(self, filename='config.yaml'):
        print(f"MOCK LOAD CONFIG: {filename}")

    async def configure_pin_modes(self):
        print("MOCK CONFIGURE PIN MODES")

    async def set_all_pins_to_value(self, value):
        print(f"MOCK SET ALL PINS TO {value}")

    @property
    def device_connected(self) -> bool:
        return self._device_connected

    async def ensure_connected(self):
        print("MOCK ENSURE CONNECTED")
        self._device_connected = True
        self.connection_changed.emit(True, self.device.com_port)


_singleton: "AIODevice|None" = None


def get_device(**kwargs) -> "AIODevice":
    """
    Return the process-wide AIODevice.
    The first call constructs it, later calls hand bac  k the same object.
    Extra kwargs are silently ignored after the first call.
    """
    global _singleton
    if _singleton is None:
        if get_instance().get_bool(KEY_VIRTUAL_COM_PORT, False):
            # Use the DummyAIODevice for testing purposes.
            _singleton = DummyAIODevice(**kwargs)
        else:
            _singleton = AIODevice(**kwargs)
    return _singleton


async def main():
    device = AIODevice()
    device.connection_changed.connect(lambda connected, port: print(f"Connection changed: {connected}, Port: {port}"))
    await device.async_connect()
    # device.start_monitoring()
    # await device.set_pin_mode_digital_output(13)
    # device.load_pin_configuration()
    # await device.configure_pin_modes()
    print("Device running. Waiting for input changes or disconnection...")
    print("Try unplugging the Arduino now.")

    # Keep running until disconnected (monitor task handles detection)
    while device._device_connected:
        # await device.digital_write(13, 1)  # Example: Set pin 13 to HIGH
        await asyncio.sleep(1)
    print("Main loop detected disconnection.")
    print(device)


if __name__ == "__main__":
    try:
        # Use asyncio.run() for simple cases, but for GUI apps (PySide6),
        # you'll integrate with the Qt event loop (e.g., using qasync)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
