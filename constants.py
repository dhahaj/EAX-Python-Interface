"""
Constants used for the EAX300/500 Test Fixture.

Author: Daniel Hahaj 2023-08-01

This file contains many variables that are used throughout the application. Certian
values can be adjusted here to make the application more modular.
"""

import enum
from typing import List
from os import PathLike

APP_NAME: str = "EAX Interface"
APP_VERSION: str = "2.1.0"
COMPANY_NAME: str = "Detex Corp"

ICON_WINDOW = ':/images/icons/code.ico'

ICON_USB_IMAGE = '<html><head/><body><p><img width="50" height="050" src=":/resources/icons/images/icons/usb3.png"/></p></body></html>'

ICON_USB_RED = '<html><head/><body><p><img width="52" height="52" src=":/images/icons/disconnected"/></p></body></html>'
ICON_USB_GREEN = '<html><head/><body><p><img width="52" height="52" src=":/images/icons/connected"/></p></body></html>'
ICON_USB_YELLOW = '<html><head/><body><p><img width="52" height="52" src=":/images/icons/connecting"/></p></body></html>'

ICON_USB_BACKGROUND_GRN = "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(85, 170, 0, 206), stop:0.284091 rgba(85, 170, 0, 80), stop:0.5 rgba(85, 170, 0, 80), stop:0.991525 rgba(255, 255, 255, 0));"
ICON_USB_BACKGROUND_YLW = "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 0, 206), stop:0.284091 rgba(255, 255, 0, 80), stop:0.5 rgba(255, 255, 0, 80), stop:0.991525 rgba(255, 255, 255, 0));"

ORANGE = "color: rgb(229, 153, 0); background-color: rgba(0, 0, 0, 0);"
GREEN = "color: green; background-color: rgba(0, 0, 0, 0);"
YELLOW = "color: rgb(200, 195, 0); background-color: rgba(0, 0, 0, 0);"
RED = "color: red; background-color: rgba(0, 0, 0, 0);"
DEVICE_LABEL = "color: rgb(255, 0, 0); font-weight: bold; background-color: rgba(0, 0, 0, 0);"


class State(enum.Enum):
    """The state of the application."""

    IDLE = enum.auto()
    PROGRAMMING = enum.auto()
    TESTING = enum.auto()
    WAITING_FOR_BUTTON = enum.auto()
    CONNECTING = enum.auto()
    CONNECTED = enum.auto()
    UPDATING = enum.auto()
    WAITING_FOR_INPUT = enum.auto()


CHIP_OPTIONS = ["PIC16F627", "PIC16F627A", "PIC16F628", "PIC16F628A"]

KEY_TEST_COUNT = "testing/total_count"


"""
Keys for the settings file.
"""
KEY_DEBUG: str = "debug"
KEY_COM_PORT: str = "serial_port"
KEY_PROGRAMMER_SERIAL_NUMBER: str = "programmer_serial_number"
KEY_CHIP_PART: str = "chip_part"
KEY_CHIP_OPTIONS: str = "chip_options"
KEY_TESTING_SPEED: str = "testing_speed"
KEY_AUTO_TEST: str = "auto_test"
KEY_FONT: str = "mainwindow/font"
KEY_FONT_FAMILY: str = "font_family"
KEY_FONT_SIZE: str = "font_size"
KEY_FONT_WEIGHT: str = "font_weight"
KEY_AUTO_CONNECT: str = "auto_connect"
KEY_ARDUINO_INSTANCE_ID: str = "arduino_instance_id"
KEY_FIRMWARE_FOLDER: str = "firmware_folder"
KEY_INACTIVITY_TIMEOUT: str = "inactivity_timeout"
KEY_BACKGROUND_COLOR: str = "bg_color"
KEY_FOREGROUND_COLOR: str = "fg_color"
KEY_ARDUINO_WAIT: str = "arduino_wait"
KEY_SHUTDOWN_ON_EXCEPTION: str = "shutdown_on_exception"
KEY_AUTO_FIND: str = "auto_find"
KEY_SLEEP_TUNE: str = "sleep_tune"
KEY_FULLSCREEN: str = "full_screen"
KEY_FRAMELESS: str = "frameless"
KEY_DARK_THEME: str = "dark_mode"
KEY_COUNTER_ENABLED: str = "counter_enabled"
KEY_TEST_COUNT: str = "test_count"
KEY_BUTTON_TIMEOUT: str = "button_timeout"
KEY_VIRTUAL_COM_PORT: str = "virtual_com_port"
KEY_PROGRAMMING_CONFIG: str = "programmer_config"

"""
Default settings for the application.
"""
DEFAULT_SETTINGS = {
    KEY_COM_PORT: "COM30",
    KEY_PROGRAMMER_SERIAL_NUMBER: "1E660",
    KEY_CHIP_PART: "PIC16F628A",
    KEY_TESTING_SPEED: 2100,
    KEY_AUTO_TEST: True,
    KEY_FONT: "Calibri,16,-1,5,400,0,0,0,0,0,0,0,0,0,0,1,Regular",
    KEY_FONT_FAMILY: "Consolas",
    KEY_FONT_SIZE: 14,
    KEY_FONT_WEIGHT: "normal",
    KEY_AUTO_CONNECT: True,
    KEY_ARDUINO_INSTANCE_ID: 1,
    KEY_DEBUG: False,
    KEY_FIRMWARE_FOLDER: "firmware",
    KEY_INACTIVITY_TIMEOUT: 15,
    KEY_BACKGROUND_COLOR: "#000000",
    KEY_FOREGROUND_COLOR: "#ea0065",
    KEY_ARDUINO_WAIT: 2,
    KEY_SHUTDOWN_ON_EXCEPTION: True,
    KEY_AUTO_FIND: True,
    KEY_SLEEP_TUNE: 0.000001,
    KEY_FULLSCREEN: False,
    KEY_FRAMELESS: False,
    KEY_COUNTER_ENABLED: True,
    KEY_TEST_COUNT: 0,
    KEY_BUTTON_TIMEOUT: 15,
    KEY_VIRTUAL_COM_PORT: False,
}


"""
Keys for the firmware dictionary.
"""
KEY_DEVICE_NAME: str = "device_name"
KEY_DEVICE_COLOR: str = "color"
KEY_FIRMWARE_FILENAME: str = "firmware_name"

INSTRUCTIONS = """<p><img src=":/resources/detex" width="300" style="float:right;"/></p>

# EAX-500 Testing Software  

 *[Click Here for help.](https://)*

## Equipment Needed

- EAX-500 Test Fixture
- An assembled 102605 PWA
- A magnet for checking the reed switches

## Setup instructions

- Head unit is connected and secured to the test fixture.
- Place battery connector in the proper position before clamping down the board.
- PWA is clamped down on the head unit.
- Test base is powered and power LED is ON.
- All USB cables from the tester are connected to the tablet.
- Flip both slide switches to the OFF position.
- Press the connect button to establish a connection with the fixture

## Usage instructions

- Select the appropriate device from the Device drop down menu. *(e.g. EAX500, EAX505, etc.)*
- Press the *Program* button to program the board. 
- If auto test is enabled and programming was successful, testing will begin automatically.
- If auto test is disabled, press the *Test* button or press anywhere on the screen to begin testing.

```info

```
"""
