"""
Constants used for the EAX300/500 Test Fixture.

Author: Daniel Hahaj 2021-09-30

This file contains many variables that are used throughout the application. Certian
values can be adjusted here to make the application more modular. 
"""

SETTINGS_FILE = "settings.json"
USERS_FILE = "users.db"
PINS_FILE = "pins.json"

FILES = [SETTINGS_FILE, USERS_FILE, PINS_FILE]

# Default testing speed in ms. This is adjustable inside the application.
DEFAULT_TESTING_SPEED = 2000

APPLICATION_THEME = "dark"

"""
Pin numbers for the Arduino board.
"""
PIN_LOW_BATTERY = 2
PIN_TESTING_INDICATOR = 4
PIN_BATTERY = 12
PIN_INDICATOR = 13

CHIP_PARTS = ["PIC16F627","PIC16F627A","PIC16F628","PIC16F628A"]


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
KEY_COM_PORT = "serial_port"
KEY_PROGRAMMER_SERIAL_NUMBER = "programmer_serial_number"
KEY_CHIP_PART = "chip_part"
KEY_LAST_USER = "last_user"
KEY_TESTING_SPEED = "testing_speed"
KEY_AUTO_TEST = "auto_test"
KEY_FONT_FAMILY = "font_family"
KEY_FONT_SIZE = "font_size"
KEY_FONT_WEIGHT = "font_weight"
KEY_AUTO_LOGIN = "skip_login"
KEY_AUTO_CONNECT = "auto_connect"
KEY_ARDUINO_INSTANCE_ID = "arduino_instance_id"
KEY_FIRMWARE_FOLDER = "firmware_folder"
KEY_LOGOFF_DELAY = "auto_logoff_delay"
KEY_BACKGROUND_COLOR = "bg_color"
KEY_FOREGROUND_COLOR = "fg_color"


"""
Default settings for the application.
"""
DEFAULT_SETTINGS = {            
    KEY_COM_PORT: "COM30",               
    KEY_PROGRAMMER_SERIAL_NUMBER: "1E660",
    KEY_CHIP_PART: "PIC16F627A",        
    KEY_LAST_USER: "dmh",
    KEY_TESTING_SPEED: 1.0,             
    KEY_AUTO_TEST: True,
    KEY_FONT_FAMILY: "Consolas",
    KEY_FONT_SIZE: 14,
    KEY_FONT_WEIGHT: "normal",
    KEY_AUTO_LOGIN: False,
    KEY_AUTO_CONNECT: False,
    KEY_ARDUINO_INSTANCE_ID: 1,
    KEY_DEBUG: False,
    KEY_FIRMWARE_FOLDER: "firmware",
    KEY_LOGOFF_DELAY: 10,
    KEY_BACKGROUND_COLOR: "#000000",
    KEY_FOREGROUND_COLOR: "#ffffff"
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
    {KEY_USERNAME: "dmh", KEY_PASSWORD: "$2b$12$ccVAflXRZEz4U5spRCyHv.Z5lAWu8P6cLbRSmlpKBck1SlzR3yV7O", KEY_ADMIN: True},
    {KEY_USERNAME: "sm", KEY_PASSWORD: "$2b$12$S35v7teOYbxZvWmdkqCzu.fqejX4Lzpe2uTaZMolhh7fXpHwmdOVG", KEY_ADMIN: True},
    {KEY_USERNAME: "admin", KEY_PASSWORD: "$2b$12$.RWCdkSOLyGzXzFtqlY//Ow4GRMD2j4CcRGOCfa.fG/OP2P6B5UGW", KEY_ADMIN: True},
    {KEY_USERNAME: "user", KEY_PASSWORD: "$2b$12$GxFOW/zBSQmdSq3Y9lIxE.pLPOFCIl9dQd0rmgu.Ofg3nSJke8Hpm", KEY_ADMIN: False},
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

INSTRUCTIONS = """# EAX-500 Testing Software

## Equipment Needed:

 - EAX-500 Test Fixture
 - An assembled 102618 PWA
 - A magnet for checking the reed switches

## Setup instructions:

- Head unit is connected and secured to the test fixture.
- Place battery connector in the proper position before clamping down the board.
- PWA is clamped down on the head unit.
- Test base is powered and power LED is ON.
- All USB cables from the tester are connected to the tablet.
- Flip both slide switches to the OFF position.
- Press the connect button to establish a connection with the fixture

## Usage instructions:

- Select the appropriate device from the Device drop down menu. *(e.g. EAX500, EAX505, etc.)*
- Press the *Program* button to program the board. 
- If auto test is enabled and programming was successful, testing will begin automatically.
- If auto test is disabled, press the *Test* button to begin testing. 
  
```info

```
"""