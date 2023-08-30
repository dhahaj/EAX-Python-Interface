from telemetrix.telemetrix import Telemetrix
from settings import ApplicationSettings
import threading
import json
import os
from rich import print
from loguru import logger as log
from constants import *
from time import time
from serial.tools.list_ports_common import ListPortInfo
from serial.tools import list_ports
from rich import print_json
from typing import List
from pprint import pprint as pp

def debug(self, msg):
    if self.debug:
        log.debug(msg)


class USBDevice(Telemetrix):
    """
    This class handles the USB connection to the Arduino board. It extends the telemetrix class. It modifies how
    the connection is handled by delaying the connection until the connect() method is called and adding a callback
    function that is called upon returning, passing a parameter indicating whether the connection was successful.
    """
    DEBOUNCE_TIME = 0.05

    def __init__(
        self,
        device_connected_callback=None,
        wait: int=4,
        shutdown_on_exception: bool=True,
        sleep_tune: float=1e-6,
        debug: bool=True,
    ):
        """Initialize the USBHandler class.

        :param port: The port to connect to.
        :param device_connected_callback: The callback function to call when the device is connected.
        :param arduino_instance_id: The instance ID of the Arduino board.
        """
        self.port: str = None
        self.settings = ApplicationSettings()

        # determine how to connect to the arduino
        if self.settings.get(KEY_AUTO_FIND):
            # If auto find is enabled, only specify the arduino ID
            self.port = None
            self.arduino_instance_id: int = self.settings.get_int(KEY_ARDUINO_INSTANCE_ID)
        else:
            # otherwise, only specify the port
            self.port = self.settings.get(KEY_COM_PORT)
            self.arduino_instance_id = None

        log.info(f'port is set to {self.port}')

        self.device_connected_callback = device_connected_callback
        self.shutdown_on_exception: bool = shutdown_on_exception
        self.arduino_wait: int = wait
        self.sleep_tune: float = sleep_tune

        self.board: Telemetrix = None

        self.device_connected = False
        self.debug: bool = debug

        self.pins: dict = {}
        self.inputs: List = []
        self.last_input_times: dict = {}
        self.callback = None
        print(vars(self))
        print(type(vars(self)))

        print(
            f"[bold green]USBDeviceHandler[/bold green]\n"
            f"initialized with port: {self.port}\n"
            f"arduino_instance_id: {self.arduino_instance_id}\n"
            f"debug: {self.debug}\n"
            f"shutdown_on_exception: {self.shutdown_on_exception}\n"
            f"arduino_wait: {self.arduino_wait}\n"
            f"sleep_tune: {self.sleep_tune}\n"
            f"device_connected: {self.device_connected}\n"
        )

    def input_callback(self, message: str) -> None:
        pin_number = message[0]
        value = message[2]
        current_time = time()

        # Debouncing: If the pin has not been read recently, process the value
        if pin_number not in self.last_input_times or current_time - self.last_input_times[pin_number] > self.DEBOUNCE_TIME:
            log.info(f'Pin {pin_number} changed to {value}')
            # Store the current time for this pin
            self.last_input_times[pin_number] = current_time
            # You can now handle the change in value as needed
            # if self.callback is not None:
            #     self.callback([pin_number, value])

    def attach_callback(self, callback):
        self.callback = callback

    def connect(self, callback=None):
        """
        Connect to the Arduino board.

        :param callback: The callback function to call when the device is connected.
        """
        debug(self, f'Method: {self.connect.__name__}')
        if not self.device_connected:
            self.check_device_thread = threading.Thread(
                target=self.check_device_connection
            )
            self.check_device_thread.start()

    def check_device_connection(self):
        """Check the connection to the Arduino board."""
        debug(self, f'Method: {self.check_device_connection.__name__}')
        try:
            if not self.device_connected:
                # Create a new Telemetrix instance
                super(USBDevice, self).__init__(
                    com_port=self.port,
                    arduino_instance_id=self.settings.get_int(KEY_ARDUINO_INSTANCE_ID),
                    arduino_wait=int(self.arduino_wait),
                    shutdown_on_exception=bool(self.shutdown_on_exception),
                    sleep_tune=float(self.sleep_tune),
                )
                self.load_pin_configuration()  # Load the pins from the pins.json file
                self.configure_pin_modes()  # Set the pin modes

                self.device_connected = True  # Set the device connected flag

                # Call the callback function if it is specified
                if self.device_connected_callback is not None:
                    self.device_connected_callback(True, self.com_port)
        except Exception as e:
            log.exception(
                f'Exception occurred while connecting to device: {e}')
            if self.device_connected_callback is not None:
                self.device_connected_callback(False, e.args[0])
            self.device_connected = False

    def get_pin_by_function(self, function: str) -> int:
        """
        Fetch a pin by its function.

        :param pins: List of pin dictionaries.
        :param function: The function to search for.
        :return: The integer pin number, or None if not found.
        """
        debug(self, f'Method: {self.get_pin_by_function.__name__}')

        # Loop through the pins and find the pin with the specified function
        for pin in self.pins:
            if pin['function'] == function:
                return pin['pin_number']
        debug(self, f'Pin with function {function} not found.')
        return None  # If no pin with the function is found, return None

    def battery_on(self):
        self.write_pin_by_func('battery', 1)

    def battery_off(self):
        self.write_pin_by_func('battery', 0)

    def low_battery_on(self):
        self.write_pin_by_func('low battery', 1)

    def low_battery_off(self):
        self.write_pin_by_func('low battery', 0)

    def indicator_on(self):
        self.write_pin_by_func('indicator', 1)

    def indicator_off(self):
        self.write_pin_by_func('indicator', 0)
        
    def test_indicator_on(self):
        self.write_pin_by_func('test indicator', 1)

    def test_indicator_off(self):
        self.write_pin_by_func('test indicator', 0)

    def configure_pin_modes(self):
        """Configures the pin modes of the Arduino board."""
        debug(self, f'Method: {self.configure_pin_modes.__name__}')
        # Loop through the pins and set the pin modes
        for pin in self.pins:
            if pin['io_mode'] == 'output':
                self.set_pin_mode_digital_output(pin['pin_number'])
            elif pin['io_mode'] == 'input':
                pin_number = pin['pin_number']  # Extract pin number
                self.inputs.append(pin)
                self.last_input_times[pin_number] = 0
                if pin['pullup_enabled']:
                    self.set_pin_mode_digital_input_pullup(
                        pin['pin_number'], self.input_callback)
                else:
                    self.set_pin_mode_digital_input(
                        pin['pin_number'], self.input_callback)

    @property
    def connected(self) -> bool:
        return self.device_connected
    
    @connected.setter
    def connected(self, value: bool) -> None:
        self.device_connected = value        

    def load_pin_configuration(self, filename='pins.json') -> None:
        """
        Configures the pins by loading them from a JSON file.

        :param filename: The filename to load the pins from. Defaults to pins.json.
        """
        debug(self, f'Loading pin configuration from {filename}')

        # Check if the pins.json file exists, and create it if it doesn't
        if not os.path.exists(filename):
            log.warning('pins.json file not found. Creating a new one.')
            # Create a pins.json file from the default pin settings
            with open(os.path.join('.', filename), 'w') as file:
                json.dump({'pins': self.pins}, file, indent=4)

        # Load the pins from the pins.json file
        with open(filename, 'r') as file:
            self.pins = json.load(file)['pins']

        self.enable_digital_reporting(13)

    def write_pin(self, pin_number: int, value: int) -> None:
        """
        Write a value to a pin by its number.

        :param pin_number: The pin number to write to.
        :param value: The value to write to the pin.
        """
        debug(self, 
            f'Method: {self.write_pin.__name__}, Pin: {pin_number}, Value: {value}')

        if pin_number:  # If the pin is found
            _pin = int(pin_number)
        self.digital_write(_pin, value)

    def write_pin_by_func(self, pin_function, value) -> None:
        """
        Write a value to a pin by its function.

        :param pin_function: The function of the pin.
        :param value: The value to write to the pin.
        """
        debug(self, f'Method: {self.write_pin_by_func.__name__}, Pin: {pin_function}, Value: {value}')
        if pin_function:
            pin = self.get_pin_by_function(pin_function)
            if pin:  # If the pin is found
                self.digital_write(pin, value)
            else:
                log.error(f'Pin with function {pin_function} not found.')
        else:
            log.error('Pin function not specified.')

    def read_pin(self, pin_number) -> int:
        """
        Read the value of a pin by its number. Not currently implemented!

        :param pin_number: The pin number to read from.
        :return: The value of the pin.
        """
        debug(self, f'Method: {self.read_pin.__name__}, Pin: {pin_number}')
        if pin_number and self.connected:
            pin = self.get_pin_by_function(pin_number) if isinstance(pin_number, str) else pin_number
            return self.board.digital_read(pin)[0]
        else:
            if self.debug:
                if not self.connected:
                    log.warning('Device not connected.')
                if not pin_number:
                    log.warning('Pin number not specified.')
        return None

    def set_all_pins_to_value(self, value: int) -> None:
        """
        Set all pins to a value.

        :param value: The value to set the pins to.
        """
        debug(self, f'Method: {self.set_all_pins_to_value.__name__}, Value: {value}')
        for pin in self.pins:
            if pin[Key.io_mode] == 'output':
                self.write_pin(pin[Key.pin_number], value)

    def toggle_pin(self, pin_number) -> None:
        debug(self, f'Method: {self.toggle_pin.__name__}, Pin: {pin_number}')

        pin = self.get_pin_by_function(pin_number) if isinstance(pin_number, str) else pin_number
        if self.read_pin(pin):
            self.write_pin(pin, 0)
        else:
            self.write_pin(pin, 1)

    def cleanup(self) -> None:
        """Cleanup the Arduino instance."""
        debug(self, f'Method: {self.cleanup.__name__}')
        self.set_all_pins_to_value(0)
        self.device_connected = False
        super(USBDevice, self).shutdown()

    def __str__(self) -> str:
        """Return a string representation of this object"""
        return (
            f'USB Device(port={self.port},'
            f' arduino_instance_id={self.arduino_instance_id}, debug={self.debug})'
        )

    @staticmethod
    def get_configuration(filename: str) -> List[dict]:
        pins = []
        if os.path.exists(filename):
            # Load the pins from the pins.json file
            with open(filename, 'r') as file:
                pins = json.load(file)['pins']
        return pins


    @staticmethod
    def get_ports() -> List[ListPortInfo]:
        """Get a list of available ports"""
        return list_ports.comports()

    @staticmethod
    def get_usb_ports() -> List[str]:
        """Get a list of available USB ports"""
        com_ports = []
        for port in list_ports.comports():
            if isinstance(port.pid, int) and isinstance(port.vid, int):
                com_ports.append(port.name)
        return com_ports


def get_device():
    """Get the USB device handler"""
    return USBDevice()


def get_usb_ports():
    return USBDevice.get_usb_ports()


def configuration(filename='pins.json') -> List[dict]:
    pins: dict = None
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            pins = json.load(file)['pins']
    return pins


def get_pin_by_function(function, pins: List[dict]=None) -> int:
    """
    Fetch a pin by its function.

    :param pins: List of pin dictionaries.
    :param function: The function to search for.
    :return: The integer pin number, or None if not found.
    """
    if pins is None:
        pins = configuration()
    # Loop through the pins and find the pin with the specified function
    for pin in pins:
        if pin['function'] == function:
            return pin['pin_number']
    return None  # If no pin with the function is found, return None
