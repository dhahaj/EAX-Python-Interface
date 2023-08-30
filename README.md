# EAX Test Fixture Interface

This is a Python version of the EAX Test Fixture Interface. It is a GUI built on the Qt framework that allows the user to control the EAX Test Fixture. It is designed to be used with the telemetrix Arduino library. See the [firmware](#test-fixture-firmware) section for more information.

## Table of Contents

- [EAX Test Fixture Interface](#eax-test-fixture-interface)
  - [Table of Contents](#table-of-contents)
  - [Key Bindings](#key-bindings)
  - [Installation](#installation)
  - [Test Fixture Firmware](#test-fixture-firmware)
  - [Misc Files](#misc-files)
    - [Log Database](#log-database)
    - [Pin Definitions](#pin-definitions)
    - [Firmware Definitions](#firmware-definitions)
    - [Log Database](#log-database-1)
    - [User Database](#user-database)

## Key Bindings

| Key | Function |
| --- | --- |
| `Esc` | Close Window |
| `Ctrl+Q` | Exit |
| `Ctrl+L` | Login |
| `F12` | Show Stats |
| `F11` | Toggle Fullscreen |
| `F10` | Show Logs |
| `F6` | Toggle Dark Mode |
| `F4` | Open Settings |
| `F3` | Open Manual Control |
| `F2` | Take Screenshot |
| `F1` | Open Help |
| `P` | Program |
| `T` | Run Test |
| `?` | Open About |

## Installation

1. Install Python >= 3.7.
2. The programming software called `up.exe` provided for by the [Asix corporation](https://www.asix.net/) is required for programming.
3. Install the required Python package dependencies listed in `requirements.txt` using the command `pip install -r requirements.txt`.
4. A standalone executable can be created using `pyinstaller`. Install `pyinstaller` using the command `pip install pyinstaller`. (Optional)

## Test Fixture Firmware

This application uses the `Telemetrix4Arduino` Arduino library to communicate with the test fixture. It can be compilled and uploaded via the Arduino IDE or the `arduino-cli` tool. The installation of the firmware can be automated using the [Install.ps1](Scripts/Install.ps1) script. This script will download the `arduino-cli` tool, install the required libraries, compile the firmware, and upload it to the Arduino. It prompts for the COM port of the Arduino before uploading the firmware. Modify the file [Telemetrix4Arduino.ino](https://github.com/dhahaj/EAX-Python-Interface/blob/main/sketches/Telemetrix4Arduino/Telemetrix4Arduino.ino) to make modifications to the firmware, such as changing the `arduino_instance_id`. See [The Telemetrix Project](https://mryslab.github.io/telemetrix/) for more information.

## Misc Files

### Log Database

Logging is handled by the `loguru` Python package and the data is stored in the `logs.db` file using the `sqlite3` Python package. The `logs.db` file is a SQLite database is used to store log data. Log data can be viewed by clicking on the `Logs` menu item located in the `Help` menu. The database uses the following schema:

```sql
CREATE TABLE logs (id INTEGER PRIMARY KEY,
                   timestamp TEXT NOT NULL,
                   level TEXT NOT NULL,
                   logger TEXT NOT NULL,
                   message TEXT NOT NULL)
```

### Pin Definitions

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

### Firmware Definitions

The `firmware.json` file contains information about the names, versions, and locations of the firmware. The firmware information is stored in a JSON object with the following format:

```json
{
    "firmware": [
        {
            "filename": "EAX300_591.hex",
            "basename": "EAX300",
            "version": "591",
        },
        {
            "filename": "EAX500_591.hex",
            "basename": "EAX500",
            "version": "591",
        }
    ],
    "path": "./firmware",
}
```

### Log Database

The `logs.db` file is a SQLite database is used to store log data. This database uses the following schema:

```sql
CREATE TABLE logs (id INTEGER PRIMARY KEY,
                   timestamp TEXT NOT NULL,
                   level TEXT NOT NULL,
                   logger TEXT NOT NULL,
                   message TEXT NOT NULL)
```

### User Database

The `users.db` file is a SQLite database is used to store user data. This database uses the following schema:

```sql
CREATE TABLE users (id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    admin BOOLEAN NOT NULL DEFAULT 0)
```
