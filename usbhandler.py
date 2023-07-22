from constants import *
# from applogger import AppLogger
import threading
import json
import os
import traceback

from telemetrix.telemetrix import Telemetrix


class USBHandler(Telemetrix):
    """
    This class handles the USB connection to the Arduino board. It extends the telemetrix class for this specific application.
    """

    def __init__(
        self,
        port=None,
        device_connected_callback=None,
        arduino_instance_id=1,
        debug=True,
    ):
        """
        Initialize the USBHandler class.

        :param port: The port to connect to.
        :param device_connected_callback: The callback function to call when the device is connected.
        :param arduino_instance_id: The instance ID of the Arduino board.
        """
        self.device_connected_callback = device_connected_callback
        self.arduino_instance_id = arduino_instance_id
        self.board = None
        self.port = port
        self.device_connected = False
        self.debug = debug
        # Default settings
        self.pins = DEF_PIN_SETTINGS

    def connect(self):
        """Connect to the Arduino board."""
        if not self.device_connected and self.board is None:
            self.check_device_thread = threading.Thread(
                target=self.check_device_connection,
                # shutdown_on_exception=False,
            )
            self.check_device_thread.start()
            if self.debug:
                print(f"Method: {self.connect.__name__} - Thread started")

    def check_device_connection(self):
        """Check the connection to the Arduino board."""
        try:
            if self.debug:
                print(
                    f"Method: {self.check_device_connection.__name__}, Connection: {self.device_connected}"
                )
            if not self.device_connected:
                # Create a new Telemetrix instance
                super(USBHandler, self).__init__(
                    com_port=self.port,
                    arduino_instance_id=self.arduino_instance_id,
                )
                self.load_pins()  # Load the pins from the pins.json file
                self.set_pin_modes()  # Set the pin modes

                self.device_connected = True  # Set the device connected flag

                # Call the callback function if it is specified
                if self.device_connected_callback is not None:
                    self.device_connected_callback(True)

        except Exception as e:
            print(f"Exception occurred while connecting to device: {e}")
            traceback.print_exc()
            if self.device_connected_callback is not None:
                self.device_connected_callback(False, e.args[0])
            self.device_connected = False
            # self.board = None

    def get_pin_by_function(self, function):
        """
        Fetch a pin by its function.

        :param pins: List of pin dictionaries.
        :param function: The function to search for.
        :return: The integer pin number, or None if not found.
        """
        if self.debug:
            print(f"Method: {self.get_pin_by_function.__name__}, Function: {function}")

        # Loop through the pins and find the pin with the specified function
        for pin in self.pins:
            if pin["function"] == function:
                return pin["pin_number"]
        if self.debug:
            print(f"Pin with function {function} not found.")
        return None  # If no pin with the function is found, return None

    def set_pin_modes(self):
        """
        Configures the pin modes of the Arduino board.
        """
        if self.debug:
            print(f"Method: {self.set_pin_modes.__name__}")

        # Loop through the pins and set the pin modes
        for pin in self.pins:
            if pin["io_mode"] == "output":
                self.set_pin_mode_digital_output(pin["pin_number"])
            elif pin["io_mode"] == "input":
                # See if pullup is enabled
                if pin["pullup_enabled"]:
                    self.set_pin_mode_digital_input_pullup(pin["pin_number"])
                else:
                    self.set_pin_mode_digital_input(pin["pin_number"])

    def is_connected(self):
        """Check if the Arduino board is connected."""
        return self.device_connected

    def load_pins(self, filename="pins.json"):
        """
        Configures the pins by loading them from a JSON file.

        :param filename: The filename to load the pins from. Defaults to pins.json.
        """
        if self.debug:
            print(f"Method: {self.load_pins.__name__}")

        # Check if the pins.json file exists, and create it if it doesn't
        if not os.path.exists(filename):
            print("pins.json file not found. Creating a new one.")
            # Create a pins.json file from the default pin settings
            with open(os.path.join(".", filename), "w") as file:
                json.dump({"pins": self.pins}, file, indent=4)

        # Load the pins from the pins.json file
        with open(filename, "r") as file:
            self.pins = json.load(file)["pins"]

    def write_pin(self, pin_number, value):
        """
        Write a value to a pin by its number.

        :param pin_number: The pin number to write to.
        :param value: The value to write to the pin.
        """
        if self.debug:
            print(
                f"Method: {self.write_pin.__name__}, Pin: {pin_number}, Value: {value}"
            )

        if pin_number is not None:  # If the pin is found
            _pin = int(pin_number)

        self.digital_write(_pin, value)

    def write_pin_by_func(self, pin_function, value):
        """
        Write a value to a pin by its function.

        :param pin_function: The function of the pin.
        :param value: The value to write to the pin.
        """
        if self.debug:
            print(
                f"Method: {self.write_pin_by_func.__name__}, Pin: {pin_function}, Value: {value}"
            )
        if pin_function is not None:  # If the pin function is specified
            pin = self.get_pin_by_function(pin_function)
            if pin is not None:  # If the pin is found
                # self.board.digital_write(pin, value)
                self.digital_write(pin, value)
            else:
                print(f"Pin with function {pin_function} not found.")
        else:
            print("Pin function not specified.")

    def read_pin(self, pin_number):
        """
        Read the value of a pin by its number.

        :param pin_number: The pin number to read from.
        :return: The value of the pin.
        """
        if self.debug:
            print(f"Method: {self.read_pin.__name__}, Pin: {pin_number}")
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
                    print("Device not connected.")
                if pin_number is None:
                    print("Pin number not specified.")
            return None

    def toggle_pin(self, pin_number):
        if self.debug:
            print(f"Method: {self.toggle_pin.__name__}, Pin: {pin_number}")

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
        """Cleanup the Arduino board."""
        if self.debug:
            print(f"Method: {self.cleanup.__name__}")

        if self.is_connected is not None:
            for pin in self.pins:
                self.digital_write(pin["pin_number"], 0)
                self.set_pin_mode_digital_input(pin["pin_number"])
            # self.board.shutdown()
        super(USBHandler, self).shutdown()
        self.device_connected = False

    def __str__(self) -> str:
        """Return a string representation of the Arduino object."""
        return f"USB Device(port={self.port}, arduino_instance_id={self.arduino_instance_id}, debug={self.debug})"
