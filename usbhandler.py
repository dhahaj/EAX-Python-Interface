from telemetrix.telemetrix import Telemetrix
from settings import ApplicationSettings
import signal
import threading
import json
import os
from rich import print
from loguru import logger as log
from constants import *

# import serial
# noinspection PyPackageRequirementscd
from serial.serialutil import SerialException

# noinspection PyPackageRequirements
from serial.tools import list_ports
from rich import print_json


class USBDeviceHandler(Telemetrix):
    '''
    This class handles the USB connection to the Arduino board. It extends the telemetrix class. It modifies how
    the connection is handled by delaying the connection until the connect() method is called and adding a callback
    function that is called upon returning, passing a parameter indicating whether the connection was successful.
    '''

    def __init__(
        self,
        # _port=None,
        device_connected_callback=None,
        # arduino_instance_id=1,
        wait=4,
        shutdown_on_exception=True,
        sleep_tune=1e-6,
        debug=True,
        *args,
    ):
        '''
        Initialize the USBHandler class.

        :param port: The port to connect to.
        :param device_connected_callback: The callback function to call when the device is connected.
        :param arduino_instance_id: The instance ID of the Arduino board.
        '''
        self.port = None
        self.settings = ApplicationSettings()

        # determine how to connect to the arduino
        if self.settings.validate_settings():
            # only provide the id if auto find is enabled
            if self.settings.get(KEY_AUTO_FIND):
                self.port = None
                self.arduino_instance_id = self.settings.get(
                    KEY_ARDUINO_INSTANCE_ID)
            else:
                self.port = self.settings.get(KEY_COM_PORT)
                self.arduino_instance_id = None
        else:
            log.error('Settings not valid')
            # self.port = _port

        log.info(f'port is set to {self.port}')

        self.device_connected_callback = device_connected_callback
        # self.arduino_instance_id = arduino_instance_id
        self.shutdown_on_exception = shutdown_on_exception
        self.arduino_wait = wait
        self.sleep_tune = sleep_tune

        self.board = None

        self.device_connected = False
        self.debug = debug

        # Default settings
        self.pins = DEF_PIN_SETTINGS

    def connect(self, callback=None):
        '''Connect to the Arduino board.'''
        if self.debug:
            log.debug(f'Method: {self.connect.__name__}')
        if not self.device_connected and self.board is None:
            self.check_device_thread = threading.Thread(
                target=self.check_device_connection
            )
            self.check_device_thread.start()

    def check_device_connection(self):
        '''Check the connection to the Arduino board.'''
        if self.debug:
            log.info(f'Method: {self.check_device_connection.__name__}')
            # print(f'[bold red]Method[/bold red]: {self.check_device_connection.__name__},'f' Connection: {self.device_connected}')
        try:
            if not self.device_connected:
                print(self.port)
                # Create a new Telemetrix instance
                super(USBDeviceHandler, self).__init__(
                    com_port=self.port,
                    arduino_instance_id=self.arduino_instance_id,
                    arduino_wait=self.arduino_wait,
                    shutdown_on_exception=self.shutdown_on_exception,
                    sleep_tune=self.sleep_tune,
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

    def get_pin_by_function(self, function):
        '''
        Fetch a pin by its function.

        :param pins: List of pin dictionaries.
        :param function: The function to search for.
        :return: The integer pin number, or None if not found.
        '''
        if self.debug:
            log.debug(f'Method: {self.get_pin_by_function.__name__}')
            # print(f'[bold red]Method[/bold red]: {self.get_pin_by_function.__name__},'f' [bold green]Function[/bold green]: {function}')

        # Loop through the pins and find the pin with the specified function
        for pin in self.pins:
            if pin['function'] == function:
                return pin['pin_number']
        if self.debug:
            log.debug(f'Pin with function {function} not found.')
        return None  # If no pin with the function is found, return None

    def configure_pin_modes(self):
        '''
        Configures the pin modes of the Arduino board.
        '''
        if self.debug:
            log.debug(f'Method: {self.configure_pin_modes.__name__}')
            # print(f'[bold red]Method[/bold red]: {self.set_pin_modes.__name__}')

        # Loop through the pins and set the pin modes
        for pin in self.pins:
            if pin['io_mode'] == 'output':
                self.set_pin_mode_digital_output(pin['pin_number'])
            elif pin['io_mode'] == 'input':
                # See if pullup is enabled
                if pin['pullup_enabled']:
                    self.set_pin_mode_digital_input_pullup(pin['pin_number'])
                else:
                    self.set_pin_mode_digital_input(pin['pin_number'])

    def is_connected(self):
        '''Check if the Arduino board is connected.'''
        return self.device_connected

    def load_pin_configuration(self, filename='pins.json'):
        '''
        Configures the pins by loading them from a JSON file.

        :param filename: The filename to load the pins from. Defaults to pins.json.
        '''
        if self.debug:
            log.debug(f'Method: {self.load_pin_configuration.__name__}')
            # print(f'[bold red]Method[/bold red]: {self.load_pins.__name__}')

        # Check if the pins.json file exists, and create it if it doesn't
        if not os.path.exists(filename):
            log.warning('pins.json file not found. Creating a new one.')
            # print('pins.json file not found. Creating a new one.')
            # Create a pins.json file from the default pin settings
            with open(os.path.join('.', filename), 'w') as file:
                json.dump({'pins': self.pins}, file, indent=4)

        # Load the pins from the pins.json file
        with open(filename, 'r') as file:
            self.pins = json.load(file)['pins']

    def write_pin(self, pin_number, value):
        '''
        Write a value to a pin by its number.

        :param pin_number: The pin number to write to.
        :param value: The value to write to the pin.
        '''
        if self.debug:
            log.debug(
                f'Method: {self.write_pin.__name__}, Pin: {pin_number}, Value: {value}'
            )
            # print(f'[bold red]Method[/bold red]: {self.write_pin.__name__}, [bold'f' green]Pin[/bold green]: {pin_number}, [bold green]Value[/bold'f' green]: {value}')

        if pin_number is not None:  # If the pin is found
            _pin = int(pin_number)
        self.digital_write(_pin, value)

    def write_pin_by_func(self, pin_function, value):
        '''
        Write a value to a pin by its function.

        :param pin_function: The function of the pin.
        :param value: The value to write to the pin.
        '''
        if self.debug:
            log.debug(
                f'Method: {self.write_pin_by_func.__name__}, Pin: {pin_function}, Value: {value}'
            )
            # print(f'[bold red]Method[/bold red]: {self.write_pin_by_func.__name__}, [bold'f' green]Pin[/bold green]: {pin_function}, [bold green]Value[/bold'f' green]: {value}')
        if pin_function is not None:  # If the pin function is specified
            pin = self.get_pin_by_function(pin_function)
            if pin is not None:  # If the pin is found
                # self.board.digital_write(pin, value)
                self.digital_write(pin, value)
            else:
                log.error(f'Pin with function {pin_function} not found.')
                # print(f'Pin with function {pin_function} not found.')
        else:
            log.error('Pin function not specified.')
            # print('Pin function not specified.')

    def read_pin(self, pin_number):
        '''
        Read the value of a pin by its number. Not currently implemented!

        :param pin_number: The pin number to read from.
        :return: The value of the pin.
        '''
        if self.debug:
            log.debug(f'Method: {self.read_pin.__name__}, Pin: {pin_number}')
            # print(f'[bold red]Method[/bold red]: {self.read_pin.__name__}, [bold'f' green]Pin[/bold green]: {pin_number}')
        if self.is_connected() and pin_number is not None:
            if isinstance(pin_number, str):
                # pin = int(pin_number)
                pin = self.get_pin_by_function(pin_number)
            else:
                pin = pin_number
            return self.board.digital_read(pin)[0]
        else:
            if self.debug:
                if not self.is_connected():
                    print('Device not connected.')
                if pin_number is None:
                    print('Pin number not specified.')
            return None

    def set_all_pins_to_value(self, value):
        '''
        Set all pins to a value.

        :param value: The value to set the pins to.
        '''
        if self.debug:
            log.debug(f'Method: {self.set_all_pins_to_value.__name__}, Value: {value}')
            # print(f'[bold red]Method[/bold red]: {self.set_all_pins.__name__}, [bold'f' green]Value[/bold green]: {value}')

        for pin in self.pins:
            self.write_pin(pin[KEY_PIN_NUMBER], value)

    def toggle_pin(self, pin_number):
        if self.debug:
            log.debug(f'Method: {self.toggle_pin.__name__}, Pin: {pin_number}')
            # print(f'Method: {self.toggle_pin.__name__}, [bold green]Pin[/bold green]:'f' {pin_number}')

        if isinstance(pin_number, str):
            pin = self.get_pin_by_function(pin_number)
        else:
            pin = pin_number

        value = self.read_pin(pin)
        if value:
            self.write_pin(pin, 0)
        else:
            self.write_pin(pin, 1)

    def cleanup(self):
        '''Cleanup the Arduino board.'''
        if self.debug:
            log.debug(f'Method: {self.cleanup.__name__}')

        if self.is_connected():
            for pin in self.pins:
                self.digital_write(pin['pin_number'], 0)
                self.set_pin_mode_digital_input(pin['pin_number'])
        self.device_connected = False
        super(USBDeviceHandler, self).shutdown()

    def __str__(self) -> str:
        '''Return a string representation of this object'''
        return (
            f'USB Device(port={self.port},'
            f' arduino_instance_id={self.arduino_instance_id}, debug={self.debug})'
        )

    @staticmethod
    def get_ports() -> list:
        '''Get a list of available ports'''
        return list_ports.comports()

    @staticmethod
    def get_usb_ports():
        '''Get a list of available USB ports'''
        com_ports = []
        for port in USBDeviceHandler.get_ports():
            if isinstance(port.pid, int) and isinstance(port.vid, int):
                com_ports.append(port.name)
        log.debug(f'Found {len(com_ports)} usb ports: {com_ports}')
        return com_ports
