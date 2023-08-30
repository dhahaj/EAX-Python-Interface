"""
Constants used for the EAX300/500 Test Fixture.

Author: Daniel Hahaj 2023-08-01

This file contains many variables that are used throughout the application. Certian
values can be adjusted here to make the application more modular. 
"""
import enum
from typing import List
from os import PathLike

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


class Files(enum.Enum):
    Settings: str = "settings.json"
    Users: str = "users.db"
    Pins: str = "pins.json"
    Firmware: str = "firmware.json"
    Logs: str = "logs.db"

    @classmethod
    def all_files(cls) -> List[str]:
        return [f.value for f in cls]
    
    def __str__(self) -> str:
        return self.value
    


# Default testing speed in ms. This is adjustable inside the application.
DEFAULT_TESTING_SPEED: int = 2000


"""
Pin numbers for the Arduino board.
"""
PIN_LOW_BATTERY: int       = 2
PIN_TESTING_INDICATOR: int = 4
PIN_BATTERY: int           = 12
PIN_INDICATOR: int         = 13

CHIP_OPTIONS = ["PIC16F627", "PIC16F627A", "PIC16F628", "PIC16F628A"]


"""
Keys for the settings file.
"""
KEY_DEBUG: str                      = "debug"
KEY_COM_PORT: str                   = "serial_port"
KEY_PROGRAMMER_SERIAL_NUMBER: str   = "programmer_serial_number"
KEY_CHIP_PART: str                  = "chip_part"
KEY_LAST_USER: str                  = "last_user"
KEY_TESTING_SPEED: str              = "testing_speed"
KEY_AUTO_TEST: str                  = "auto_test"
KEY_FONT_FAMILY: str                = "font_family"
KEY_FONT_SIZE: str                  = "font_size"
KEY_FONT_WEIGHT: str                = "font_weight"
KEY_AUTO_LOGIN: str                 = "skip_login"
KEY_AUTO_CONNECT: str               = "auto_connect"
KEY_ARDUINO_INSTANCE_ID: str        = "arduino_instance_id"
KEY_FIRMWARE_FOLDER: str            = "firmware_folder"
KEY_LOGOFF_DELAY: str               = "auto_logoff_delay"
KEY_BACKGROUND_COLOR: str           = "bg_color"
KEY_FOREGROUND_COLOR: str           = "fg_color"
KEY_ARDUINO_WAIT: str               = "arduino_wait"
KEY_SHUTDOWN_ON_EXCEPTION: str      = "shutdown_on_exception"
KEY_AUTO_FIND: str                  = "auto_find"
KEY_SLEEP_TUNE: str                 = "sleep_tune"
KEY_FULLSCREEN: str                 = "full_screen"
KEY_TOUCHSCREEN_ENABLED: str        = "touchscreen_enabled"
KEY_FRAMELESS: str                  = "frameless"
KEY_DARK_THEME: str                 = "dark_mode"

class Key(enum.Enum):
    debug: str = "debug"
    com_port: str = "serial_port"
    programmer_serial_number: str = "programmer_serial_number"
    chip_part: str = "chip_part"
    last_user: str = "last_user"
    testing_speed: str = "testing_speed"
    auto_test: str = "auto_test"
    font_family: str = "font_family"
    font_size: str = "font_size"
    font_weight: str = "font_weight"
    auto_login: str = "skip_login"
    auto_connect: str = "auto_connect"
    arduino_instance_id: str = "arduino_instance_id"
    firmware_folder: str = "firmware_folder"
    logoff_delay: str = "auto_logoff_delay"
    background_color: str = "bg_color"
    foreground_color: str = "fg_color"
    arduino_wait: str = "arduino_wait"
    shutdown_on_exception: str = "shutdown_on_exception"
    auto_find: str = "auto_find"
    sleep_tune: str = "sleep_tune"
    fullscreen: str = "full_screen"
    touchscreen_enabled: str = "touchscreen_enabled"
    frameless: str = "frameless"
    dark_theme: str = "dark_mode"
    
    pin_number: str     = "pin_number"
    pin_function: str   = "function"
    io_mode: str        = "io_mode"
    pullup_enabled: str = "pullup_enabled"

    firmware: str = "firmware"
    firmware_name: str = "filename"
    firmware_basename: str = "basename"
    firmware_version: str = "version"
    path: str = "path"

    username: str = "username"
    password: str = "password"
    admin: str    = "admin"

    @property
    def value(self) -> str:
        return super(Key, self).value

    @property
    def name(self) -> str:
        return super(Key, self).name
    
    @classmethod
    def all_files(cls) -> List[str]:
        return [f.value for f in cls]
    
    def __str__(self) -> str:
        return self.value


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
    KEY_TOUCHSCREEN_ENABLED: False,
    KEY_FRAMELESS: False,
}


INPUT: str  = "INPUT"
OUTPUT: str = "OUTPUT"

DEF_PIN_SETTINGS = [
    {
        Key.pin_number: PIN_LOW_BATTERY,
        Key.pin_function: "LOW BATTERY",
        Key.io_mode: OUTPUT,
        Key.pullup_enabled: False,
    },
    {
        Key.pin_number: PIN_TESTING_INDICATOR,
        Key.pin_function: "TESTING INDICATOR",
        Key.io_mode: OUTPUT,
        Key.pullup_enabled: False,
    },
    {
        Key.pin_number: PIN_BATTERY,
        Key.pin_function: "BATTERY",
        Key.io_mode: OUTPUT,
        Key.pullup_enabled: False,
    },
    {
        Key.pin_number: PIN_INDICATOR,
        Key.pin_function: "INDICATOR",
        Key.io_mode: OUTPUT,
        Key.pullup_enabled: False,
    },
]

"""
Default users for the application.
"""
DEFAULT_USERS = [
    {
        Key.username: "dmh",
        Key.password: "$2b$12$ccVAflXRZEz4U5spRCyHv.Z5lAWu8P6cLbRSmlpKBck1SlzR3yV7O",
        Key.admin: True,
    },
    {
        Key.username: "sm",
        Key.password: "$2b$12$S35v7teOYbxZvWmdkqCzu.fqejX4Lzpe2uTaZMolhh7fXpHwmdOVG",
        Key.admin: True,
    },
    {
        Key.username: "admin",
        Key.password: "$2b$12$.RWCdkSOLyGzXzFtqlY//Ow4GRMD2j4CcRGOCfa.fG/OP2P6B5UGW",
        Key.admin: True,
    },
    {
        Key.username: "user",
        Key.password: "$2b$12$GxFOW/zBSQmdSq3Y9lIxE.pLPOFCIl9dQd0rmgu.Ofg3nSJke8Hpm",
        Key.admin: False,
    },
]

"""
Keys for the firmware dictionary.
"""
FIRMWARE_NAME: str = "name"
FIRMWARE_VERSION: str = "version"
KEY_FIRMWARE: str = "firmware"
KEY_FIRMWARE_NAME: str = "filename"
KEY_FIRMWARE_BASENAME: str = "basename"
KEY_FIRMWARE_VERSION: str = "version"
KEY_PATH: str = "path"

"""
Firmware names and versions for the application.

This is used for locating the firmware binaries. The hex files are
stored in a folder named "firmware" in the same folder as the application.

[{
    "filename": "EAX300_591.hex",
    "basename": "EAX300",
    "version": "591"
},
{
    "filename": "EAX300_591.hex",
    "basename": "EAX300",
    "version": "591"
}]
"""

FIRMWARES = {
    "firmware":
    [
        {
            Key.firmware_name: "EAX300_591.hex",
            Key.firmware_basename: "EAX300",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX500_591.hex",
            Key.firmware_basename: "EAX500",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX503_591.hex",
            Key.firmware_basename: "EAX503",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX504_591.hex",
            Key.firmware_basename: "EAX504",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX505_591.hex",
            Key.firmware_basename: "EAX505",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX510_591.hex",
            Key.firmware_basename: "EAX510",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX513_591.hex",
            Key.firmware_basename: "EAX513",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX514_591.hex",
            Key.firmware_basename: "EAX514",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX515_591.hex",
            Key.firmware_basename: "EAX515",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX520_591.hex",
            Key.firmware_basename: "EAX520",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX523_591.hex",
            Key.firmware_basename: "EAX523",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX524_591.hex",
            Key.firmware_basename: "EAX524",
            Key.firmware_version: "591"
        },
        {
            Key.firmware_name: "EAX525_591.hex",
            Key.firmware_basename: "EAX525",
            Key.firmware_version: "591"
        },
    ],
    "path": "firmware"
}


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
