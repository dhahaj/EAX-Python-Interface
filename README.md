# EAX Test Fixture Interface

This is a Python version of the EAX Test Fixture Interface. It is a Python module that provides a Python interface to the EAX Test Fixture. It is intended to be used by the EAX Test Fixture to control the EAX device under test (DUT) and to collect test results from the EAX DUT.

## Installation

1. Install Python 3.7 or later.
2. Install the Python packages listed in the `requirements.txt` file using the command `pip install -r requirements.txt`.
3. Run the command `python setup.py install` to install the EAX Test Fixture Interface, or use pyinstaller to create a standalone executable.

## Usage

The EAX Fixture Interface can be modified by changing the values located in the `pins.json`, `settings.json`, and `users.json` files. 

### `pins.json`

The `pins.json` file contains the pin assignments for the application. The pin assignments are stored in a JSON object with the following format:

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
    "font_style": "normal",
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

```json
{
    "users": [
        {
            "username": "dmh",
            "password": "password",
            "admin": true,
        },
        {
            "username": "user",
            "password": "password",
            "admin": false,
        }
    ]
}
```
