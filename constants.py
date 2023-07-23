"""
Constants used for the EAX300/500 Test Fixture.

Author: Daniel Hahaj 2021-09-30

This file contains many variables that are used throughout the application. Certian
values can be adjusted here to make the application more modular. 
"""

# Default testing speed in ms. This is adjustable inside the application.
DEFAULT_TESTING_SPEED = 2000

APPLICATION_THEME = "light"

"""
Pin numbers for the Arduino board.
"""
PIN_LOW_BATTERY = 2
PIN_TESTING_INDICATOR = 4
PIN_BATTERY = 12
PIN_INDICATOR = 13

"""
States for the application.
"""
ST_LOGGED_IN = "Logged In"
ST_LOGGED_OUT = "Logged Out"
ST_LOGGING_IN = "Logging In"
ST_LOGGING_OUT = "Logging Out"
ST_TESTING = "Testing"
ST_TESTING_COMPLETE = "Testing Complete"
ST_TESTING_FAILED = "Testing Failed"
ST_PROGRAMMING = "Programming"
ST_EXITING = "Exiting"
ST_INIT = "Initializing"

"""
Keys for the settings file.
"""
KEY_DEBUG = "debug"
KEY_SERIAL_PORT = "serial_port"
KEY_PROGRAMMER_SERIAL_NUMBER = "programmer_serial_number"
KEY_CHIP_PART = "chip_part"
KEY_LAST_USER = "last_user"
KEY_TESTING_SPEED = "testing_speed"
KEY_AUTO_TEST = "auto_test"
KEY_FONT_FAMILY = "font_family"
KEY_FONT_SIZE = "font_size"
KEY_FONT_WEIGHT = "font_style"
KEY_FONT_COLOR = "font_color"
KEY_SKIP_LOGIN = "skip_login"
KEY_AUTO_CONNECT = "auto_connect"
KEY_ARDUINO_INSTANCE_ID = "arduino_instance_id"
KEY_FIRMWARE_FOLDER = "firmware_folder"

"""
Default settings for the application.
"""
DEFAULT_SETTINGS = {
    KEY_SERIAL_PORT: "COM30",
    KEY_PROGRAMMER_SERIAL_NUMBER: "1E660",
    KEY_CHIP_PART: "PIC16F627A",
    KEY_LAST_USER: "dmh",
    KEY_TESTING_SPEED: 1.0,
    KEY_AUTO_TEST: True,
    KEY_FONT_FAMILY: "Consolas",
    KEY_FONT_SIZE: 14,
    KEY_FONT_WEIGHT: "normal",
    KEY_FONT_COLOR: "#000000",
    KEY_SKIP_LOGIN: False,
    KEY_AUTO_CONNECT: False,
    KEY_ARDUINO_INSTANCE_ID: 1,
    KEY_DEBUG: False,
    KEY_FIRMWARE_FOLDER: "firmware",
}

"""
Keys for the pin dictionary.
"""
KEY_PIN_NUMBER = "pin_number"
KEY_PIN_FUNCTION = "function"
KEY_IO_MODE = "io_mode"
KEY_PULLUP_ENABLED = "pullup_enabled"

"""
IO modes values.
"""
INPUT = "INPUT"
OUTPUT = "OUTPUT"

DEF_PIN_SETTINGS = [
    {
        KEY_PIN_NUMBER: PIN_LOW_BATTERY,
        KEY_PIN_FUNCTION: "LOW BATTERY",
        KEY_IO_MODE: OUTPUT,
        KEY_PULLUP_ENABLED: False,
    },
    {
        KEY_PIN_NUMBER: PIN_TESTING_INDICATOR,
        KEY_PIN_FUNCTION: "TESTING INDICATOR",
        KEY_IO_MODE: OUTPUT,
        KEY_PULLUP_ENABLED: False,
    },
    {
        KEY_PIN_NUMBER: PIN_BATTERY,
        KEY_PIN_FUNCTION: "BATTERY",
        KEY_IO_MODE: OUTPUT,
        KEY_PULLUP_ENABLED: False,
    },
    {
        KEY_PIN_NUMBER: PIN_INDICATOR,
        KEY_PIN_FUNCTION: "INDICATOR",
        KEY_IO_MODE: OUTPUT,
        KEY_PULLUP_ENABLED: False,
    },
]

"""
Keys for the user dictionary.
"""
KEY_USERNAME = "username"
KEY_PASSWORD = "password"
KEY_ADMIN = "admin"

"""
Default users for the application.
"""
DEFAULT_USERS = [
    {KEY_USERNAME: "dmh", KEY_PASSWORD: "d853", KEY_ADMIN: True},
    {KEY_USERNAME: "sm", KEY_PASSWORD: "1234", KEY_ADMIN: True},
    {KEY_USERNAME: "admin", KEY_PASSWORD: "password", KEY_ADMIN: True},
    {KEY_USERNAME: "user", KEY_PASSWORD: "password", KEY_ADMIN: False},
]

"""
Keys for the firmware dictionary.
"""
FIRMWARE_NAME = "name"
FIRMWARE_VERSION = "version"

"""
Firmware names and versions for the application.

This is used for locating the firmware binaries. The hex files are
stored in a folder named "firmware" in the same folder as the application.
"""
FIRMWARES = [
    {FIRMWARE_NAME: "EAX300", FIRMWARE_VERSION: "59"},
    {FIRMWARE_NAME: "EAX500", FIRMWARE_VERSION: "591"},
    {FIRMWARE_NAME: "EAX503", FIRMWARE_VERSION: "591"},
    {FIRMWARE_NAME: "EAX504", FIRMWARE_VERSION: "591"},
    {FIRMWARE_NAME: "EAX505", FIRMWARE_VERSION: "591"},
    {FIRMWARE_NAME: "EAX510", FIRMWARE_VERSION: "591"},
    {FIRMWARE_NAME: "EAX513", FIRMWARE_VERSION: "591"},
    {FIRMWARE_NAME: "EAX514", FIRMWARE_VERSION: "591"},
    {FIRMWARE_NAME: "EAX515", FIRMWARE_VERSION: "591"},
    {FIRMWARE_NAME: "EAX520", FIRMWARE_VERSION: "591"},
    {FIRMWARE_NAME: "EAX523", FIRMWARE_VERSION: "591"},
    {FIRMWARE_NAME: "EAX524", FIRMWARE_VERSION: "591"},
    {FIRMWARE_NAME: "EAX525", FIRMWARE_VERSION: "591"},
]

