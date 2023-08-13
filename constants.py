"""
Constants used for the EAX300/500 Test Fixture.

Author: Daniel Hahaj 2023-08-01

This file contains many variables that are used throughout the application. Certian
values can be adjusted here to make the application more modular. 
"""


ICON_USB_IMAGE = '<html><head/><body><p><img width="50" height="050" src=":/resources/icons/images/icons/usb3.png"/></p></body></html>'

ICON_USB_RED = '<html><head/><body><p><img width="52" height="52" src=":/resources/icons/images/icons/disconnected2.png"/></p></body></html>'
ICON_USB_GREEN = '<html><head/><body><p><img width="52" height="52" src=":/resources/icons/images/icons/connected2.png"/></p></body></html>'
ICON_USB_YELLOW = '<html><head/><body><p><img width="52" height="52" src=":/resources/icons/images/icons/connecting.png"/></p></body></html>'

ICON_USB_BACKGROUND_GRN = "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(85, 170, 0, 206), stop:0.284091 rgba(85, 170, 0, 80), stop:0.5 rgba(85, 170, 0, 80), stop:0.991525 rgba(255, 255, 255, 0));"
ICON_USB_BACKGROUND_YLW = "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 0, 206), stop:0.284091 rgba(255, 255, 0, 80), stop:0.5 rgba(255, 255, 0, 80), stop:0.991525 rgba(255, 255, 255, 0));"

ORANGE = "color: rgb(229, 153, 0);"
GREEN = "color: green;"
YELLOW = "color: rgb(200, 195, 0);"
RED = "color: red;"
DEVICE_LABEL = "color: rgb(255, 0, 0); font-weight: bold;"

RADIO_OFF_ICON = ":/resources/icons/images/icons/radio-off-button.png"
RADIO_ON_ICON = ":/resources/icons/images/icons/radio-on-button.png"

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

CHIP_PARTS = ["PIC16F627", "PIC16F627A", "PIC16F628", "PIC16F628A"]


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
KEY_ARDUINO_WAIT = "arduino_wait"
KEY_SHUTDOWN_ON_EXCEPTION = "shutdown_on_exception"
KEY_AUTO_FIND = "auto_find"
KEY_SLEEP_TUNE = "sleep_tune"
KEY_FULLSCREEN = "full_screen"

KEY_DARK_THEME = "dark_mode"
"""
Default settings for the application.
"""
DEFAULT_SETTINGS = {
    KEY_COM_PORT: "COM30",
    KEY_PROGRAMMER_SERIAL_NUMBER: "1E660",
    KEY_CHIP_PART: "PIC16F628A",
    KEY_LAST_USER: "dmh",
    KEY_TESTING_SPEED: 2100,
    KEY_AUTO_TEST: True,
    KEY_FONT_FAMILY: "Consolas",
    KEY_FONT_SIZE: 14,
    KEY_FONT_WEIGHT: "normal",
    KEY_AUTO_LOGIN: False,
    KEY_AUTO_CONNECT: True,
    KEY_ARDUINO_INSTANCE_ID: 1,
    KEY_DEBUG: False,
    KEY_FIRMWARE_FOLDER: "firmware",
    KEY_LOGOFF_DELAY: 15,
    KEY_BACKGROUND_COLOR: "#000000",
    KEY_FOREGROUND_COLOR: "#ff5500",
    KEY_ARDUINO_WAIT: 4,
    KEY_SHUTDOWN_ON_EXCEPTION: True,
    KEY_AUTO_FIND: True,
    KEY_SLEEP_TUNE: 0.000001,
    KEY_FULLSCREEN: False,
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
    {
        KEY_USERNAME: "dmh",
        KEY_PASSWORD: "$2b$12$ccVAflXRZEz4U5spRCyHv.Z5lAWu8P6cLbRSmlpKBck1SlzR3yV7O",
        KEY_ADMIN: True,
    },
    {
        KEY_USERNAME: "sm",
        KEY_PASSWORD: "$2b$12$S35v7teOYbxZvWmdkqCzu.fqejX4Lzpe2uTaZMolhh7fXpHwmdOVG",
        KEY_ADMIN: True,
    },
    {
        KEY_USERNAME: "admin",
        KEY_PASSWORD: "$2b$12$.RWCdkSOLyGzXzFtqlY//Ow4GRMD2j4CcRGOCfa.fG/OP2P6B5UGW",
        KEY_ADMIN: True,
    },
    {
        KEY_USERNAME: "user",
        KEY_PASSWORD: "$2b$12$GxFOW/zBSQmdSq3Y9lIxE.pLPOFCIl9dQd0rmgu.Ofg3nSJke8Hpm",
        KEY_ADMIN: False,
    },
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
 - An assembled 102605/102605-1 PWA
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
