import asyncio
from telemetrix_aio.telemetrix_aio import TelemetrixAIO
from config_loader import ConfigLoader
from settings import ApplicationSettings
from rich import print
from loguru import logger as log
from constants import KEY_COM_PORT, KEY_AUTO_FIND, KEY_ARDUINO_INSTANCE_ID
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
        self._connect_callback = None
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
                close_loop_on_shutdown=True
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

            self.connection_changed.emit(self.device_connected, self.device.com_port)

            # Start monitoring the connection in a separate task.
            asyncio.create_task(self._monitor_connection())
        except Exception as e:
            log.exception(
                f'Exception occurred while connecting to device: {e}')
            # Notify via callback if provided.
            self.device_connected = False
            if callback:
                callback(False, e.args[0])
            self.connection_changed.emit(self.device_connected, str(e))

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

    def set_pin_mode_digital_output(self, pin_number: int):
        return self.device.set_pin_mode_digital_output(pin_number)

    def set_pin_mode_digital_input(self, pin_number: int, callback):
        return self.device.set_pin_mode_digital_input(pin_number, callback)

    def set_pin_mode_digital_input_pullup(self, pin_number: int, callback):
        return self.device.set_pin_mode_digital_input_pullup(pin_number, callback)

    async def digital_write(self, pin_number: int, value: int):
        await self.device.digital_write(pin_number, value)

    async def _monitor_connection(self):
        """Periodically “ping” the board; on any exception assume the port died."""
        while self.device_connected:
            await asyncio.sleep(1)
            try:
                # you can pick any benign operation; a zero‐write is cheapest
                await self.device._get_firmware_version()
            except Exception as e:
                log.exception("Arduino connection lost")
                self.device_connected = False
                if self._connect_callback:
                    self._connect_callback(False, "Connection lost")
                self.connection_changed.emit(self.device_connected, 'Connection lost')
                break


    async def write_pin_by_func(self, pin_function, value):
        try:
            pin = self.get_pin_by_function(pin_function)
            if pin is None:
                raise RuntimeError(f"No pin for {pin_function}")
            await self.device.digital_write(pin, value)
        except Exception as e:
            log.error(f"Write failed: {e}")
            self.device_connected = False
            if self._connect_callback:
                self._connect_callback(False, str(e))
            raise

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


async def main():
    device = AIODevice()
    await device.async_connect()
    print(await device.device._get_firmware_version())
    print(type(device.pins))
    device.load_pin_configuration()
    await device.configure_pin_modes()
    await device.set_all_pins_to_value(0)
    print(device.get_pin_by_function('ac'))
    print(AIODevice.get_pin_configuration())

    print("Device running. Waiting for input changes or disconnection...")
    print("Try unplugging the Arduino now.")

    # Keep running until disconnected (monitor task handles detection)
    while device.device_connected:
        await asyncio.sleep(1)
    print("Main loop detected disconnection.")

if __name__ == "__main__":
    try:
        # Use asyncio.run() for simple cases, but for GUI apps (PySide6),
        # you'll integrate with the Qt event loop (e.g., using qasync)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        log.exception(f"An unexpected error occurred: {e}")
