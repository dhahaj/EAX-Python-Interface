import asyncio
from telemetrix_aio.telemetrix_aio import TelemetrixAIO
from config_loader import ConfigLoader
from settings import ApplicationSettings
from rich import print
# from loguru import logger as log
from constants import KEY_COM_PORT, KEY_AUTO_FIND, KEY_ARDUINO_INSTANCE_ID
from serial.tools import list_ports
from typing import List
from PySide6.QtCore import QObject, Signal
from enum import Enum
import imports

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
    connection_changed = Signal(bool, object)

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
            self.arduino_instance_id = self.settings.get_int(KEY_ARDUINO_INSTANCE_ID)
        else:
            self.port = self.settings.get(KEY_COM_PORT)
            self.arduino_instance_id = None
        self.log = imports.log
        self.log.info(f'Port is set to {self.port}')
        self.shutdown_on_exception = shutdown_on_exception
        self.arduino_wait = wait
        self.sleep_tune = float(sleep_tune)  # Ensure a float.
        self._device_connected = False
        self.debug = debug
        self.input_pin = None
        self.callback = None

        self.pins: List[Pin] = []

        self.inputs = []
        self.last_input_times = {}
        self._connect_callback = None

        # Will hold the TelemetrixAIO instance.
        self.device: TelemetrixAIO = None

        print(
            f"[bold green]AIODevice[/bold green]\n"
            f"initialize with port: {self.port}\n"
            f"arduino_instance_id: {self.arduino_instance_id}\n"
            f"debug: {self.debug}\n"
            f"shutdown_on_exception: {self.shutdown_on_exception}\n"
            f"arduino_wait: {self.arduino_wait}\n"
            f"sleep_tune: {self.sleep_tune}\n"
            f"device_connected: {self._device_connected}\n"
        )

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
        """ Asynchronously establish a connection to the Arduino via TelemetrixAIO. """
        try:
            # Instantiate the asynchronous Telemetrix device.
            self.device = TelemetrixAIO(
                com_port=self.port,
                arduino_instance_id=self.settings.get_int(KEY_ARDUINO_INSTANCE_ID),
                arduino_wait=int(self.arduino_wait),
                shutdown_on_exception=False,
                sleep_tune=self.sleep_tune,
                autostart=False,
                close_loop_on_shutdown=False
            )

            self._connect_callback = callback
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

            # self.connection_changed.emit(self._device_connected, self.device.com_port)

        except Exception as e:
            self.log.info(f'Exception occurred while connecting to device: {e}')
            # Notify via callback if provided.
            self.device_connected = False
            if callback:
                callback(self.device_connected, str(e))
            # self.connection_changed.emit(self._device_connected, str(e))

    async def async_disconnect(self):
        """ Asynchronously disconnect from the Arduino device. """
        if self.device:
            await self.device.shutdown()
            self.device_connected = False
            # self.device = None

    async def input_callback(self, message) -> None:
        """
        Callback invoked when input changes on the Arduino.
        Expects message to be a list with at least 3 elements: [?, pin, value].
        """
        pin_number = message[1]
        value = message[2]
        print(self, f'Method: {self.input_callback.__name__}, Pin: {pin_number}, Value: {value}')
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

    async def configure_pin_modes(self) -> None:
        """ Configure the pin modes based on the loaded configuration. """
        for pin in self.pins:
            pin_obj = Pin(
                pin['pin_number'],
                PinMode(pin['io_mode']),
                pin.get('function') or None,
                pin.get('pullup_enabled') or False
            )

            self.log.debug(f'Configuring pin {pin_obj}')
            await pin_obj.configure(self.device, self.input_callback)

    def set_pin_mode_digital_output(self, pin_number: int) -> None:
        return self.device.set_pin_mode_digital_output(pin_number)

    def set_pin_mode_digital_input(self, pin_number: int, callback) -> None:
        return self.device.set_pin_mode_digital_input(pin_number, callback)

    def set_pin_mode_digital_input_pullup(self, pin_number: int, callback) -> None:
        return self.device.set_pin_mode_digital_input_pullup(pin_number, callback)

    async def digital_write(self, pin_number: int, value: int) -> None:
        await self.device.digital_write(pin_number, value)

    def start_monitoring(self) -> None:
        """ Start monitoring the connection. """
        # Start the connection monitoring task.
        loop = asyncio.get_running_loop()
        loop.create_task(self._monitor_connection(), name="monitor_connection")

    async def _monitor_connection(self):
        """Periodically “ping” the board; on any exception assume the port died."""
        while self._device_connected:
            await asyncio.sleep(1)
            try:
                # log.debug("Pinging device...")
                await self.digital_write(14, 0)
                # log.debug("Heartbeat...")
            except Exception as e:
                self.log.info("Arduino connection lost")
                self.device_connected = False
                if self._connect_callback:
                    self._connect_callback(False, "Connection lost")
                break
        # self.connection_changed.emit(self._device_connected, 'Connection lost')

    async def write_pin_by_func(self, pin_function: str, value: int) -> None:
        try:
            pin = self.get_pin_by_function(pin_function)
            if pin is None:
                raise RuntimeError(f"No pin for {pin_function}")
            await self.device.digital_write(pin, value)
        except Exception as e:
            self.log.error(f"Write failed: {e}")
            self.device_connected = False
            if self._connect_callback:
                self._connect_callback(False, str(e))
            raise

    def get_pin_by_function(self, function: str) -> int:
        """ Get a pin number by its function name. """
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
            self.log.exception(f'Cleanup error: {e}')

    async def set_all_pins_to_value(self, value: int) -> None:
        for pin in self.pins:
            if pin.get('io_mode') == 'output':
                await self.digital_write(pin.get('pin_number'), value)

    def __str__(self) -> str:
        return f'AIODevice(port={self.port}, arduino_instance_id={self.arduino_instance_id}, device_connected={self._device_connected})'

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
        config = ConfigLoader()
        return config.pins


async def main():
    device = AIODevice()
    device.connection_changed.connect(lambda connected, port: print(f"Connection changed: {connected}, Port: {port}"))
    await device.async_connect()
    # device.start_monitoring()
    # await device.set_pin_mode_digital_output(13)
    device.load_pin_configuration()
    await device.configure_pin_modes()
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
