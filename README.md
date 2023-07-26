# EAX Test Fixture Interface

This is a Python version of the EAX Test Fixture Interface. It is a GUI built on the Qt framework that allows the user to control the EAX Test Fixture. It is designed to be used with the telemetrix Arduino library. See the [firmware](#firmware) section for more information.

## Installation

1. Install Python 3.7 or later.
2. Install the Python packages listed in the `requirements.txt` file using the command `pip install -r requirements.txt`.
3. Run the command `python setup.py install` to install the EAX Test Fixture Interface, or use `pyinstaller` to create a standalone executable.

## Firmware

This application uses the telemetrix Arduino library to communicate with the fixture. It can be compilled and uploaded via the Arduino IDE. This installation of the firmware can be automated using the [Install.ps1](https://github.com/dhahaj/EAX-Python-Interface/blob/main/Install.ps1) script. This script will download the `arduino-cli` tool, install the required libraries, compile the firmware, and upload it to the Arduino. It prompts for the COM port of the Arduino before uploading the firmware. Modify the file [Telemetrix4Arduino.ino](https://github.com/dhahaj/EAX-Python-Interface/blob/main/sketches/Telemetrix4Arduino/Telemetrix4Arduino.ino) to make modifications to the firmware, such as changing the `arduino_instance_id`. See [The Telemetrix Project](https://mryslab.github.io/telemetrix/) for more information.

## Usage

The EAX Fixture Interface can be modified by changing the values located in the [pins.json](https://github.com/dhahaj/EAX-Python-Interface/blob/main/pins.json), [settings.json](https://github.com/dhahaj/EAX-Python-Interface/blob/main/settings.json), and [users.json](https://github.com/dhahaj/EAX-Python-Interface/blob/main/users.json) files.

### `pins.json`

The [pins.json](https://github.com/dhahaj/EAX-Python-Interface/blob/main/pins.json) file contains the pin assignments for the application. The pin assignments are stored in a JSON object with the following format:

```json
{
    "pins": [
        {
            "pin_number": 2,
            "io_mode": "input",
            "function": "battery",
            "pullup_enabled": false,
        },
    ]
}
```

### `settings.json`

The [settings.json](https://github.com/dhahaj/EAX-Python-Interface/blob/main/settings.json) file contains the runtime settings for the application. The settings are pretty self-explanatory. The `arduino_instance_id` is a value that is set in the firmware and is used where they may be multiple connected devices.

```json
{
    "serial_port": "COM8",
    "programmer_serial_number": "1E660",
    "chip_part": "PIC16F628A",
    "last_user": "dmh",
    "testing_speed": 0.5,
    "auto_test": true,
    "font_family": "Arial",
    "font_size": 14,
    "font_weight": "normal",
    "font_color": "#000000",
    "skip_login": true,
    "auto_connect": false,
    "arduino_instance_id": 1,
    "debug": true,
    "firmware_folder": "",
    "firmware_location": "./firmware"
}

```

### `users.json`

The [users.json](https://github.com/dhahaj/EAX-Python-Interface/blob/main/users.json) file contains the user login information for the application. The `admin` field is currently not used. The `password` field is the SHA256 hash of the user's password.

```json
{
    "users": [
        {
            "username": "user",
            "password": "password",
            "admin": false,
        }
    ]
}
```
