# EAX Test Fixture Interface

This is a Python version of the EAX Test Fixture Interface. It is a GUI built on the Qt framework that allows the user to control the EAX Test Fixture. It is designed to be used with the telemetrix Arduino library. See the [firmware](#test-fixture-firmware) section for more information.

## Table of Contents

- [EAX Test Fixture Interface](#eax-test-fixture-interface)
  - [Table of Contents](#table-of-contents)
  - [Key Bindings](#key-bindings)
  - [Installation](#installation)
  - [Test Fixture Firmware](#test-fixture-firmware)
  - [Configuration File](#configuration-file)
    - [Firmware Configuration](#firmware-configuration)
    - [Pin Configuration](#pin-configuration)
    - [Default Settings Configuration](#default-settings-configuration)
    - [Testing Configuration](#testing-configuration)
  - [Test Commands](#test-commands)
  - [Misc Files](#misc-files)
    - [Log Database](#log-database)


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

## Configuration File

The `config.yaml` file contains the configuration for the application. The table below describes the configuration options.

| Key | Description |
| --- | --- |
|`app_name` | The name of the application. |
| `app_version` | The version of the application. |
| `firmware` | The EAX firmware configuration. |
|`testing` | The testing configuration. (Not currently implemented) |
|`settings` | The default settings configuration. |
|`pins` | The pin configuration. |

### Firmware Configuration

The firmware configuration defined in `config.yaml` is used to configure the filenames, versions, and paths of the firmware. The firmware configuration is stored in a YAML object with the following format:

```yaml
...

firmware:
  path: ./firmware
  default_device: EAX500
  files:
    - basename: EAX300
      filename: EAX300_59.hex
      version: '59'
    - basename: EAX500
      filename: EAX500_591.hex
      version: '591'
    - basename: EAX503
      filename: EAX503_591.hex
      version: '591'
...
```

| Key | Description |
| --- | --- |
| `path` | The relative path to the firmware files. |
| `default_file` | The default firmware file. |
| `files` | A list of the firmware files. |
| `filename` | The filename of the firmware. |
| `basename` | The basename of the firmware. |
| `version` | The firmware version. |

### Pin Configuration

The `pins` key in the `config.yaml` file contains the pin configuration. The pin configuration is stored in a YAML object with the following format:

```yaml
pins:
  - function: low battery
    io_mode: output
    pin_number: 2
    pullup_enabled: false
  - function: test mode
    io_mode: output
    pin_number: 3
    pullup_enabled: false
  - function: battery
    io_mode: output
    pin_number: 4
    pullup_enabled: false
...
```

| Key | Description |
| --- | --- |
| `pin_number` | The pin number. |
| `io_mode` | The I/O mode of the pin. Can be `input`, `output`, or `input_pullup`. |
| `function` | Describes the function of the pin. |
| `pullup_enabled` | Whether the internal pullup resistor is enabled. |

### Default Settings Configuration

The `settings` key in the `config.yaml` file contains the default settings configuration. The settings configuration is stored in a YAML object with the following format:

```yaml
settings:
    serial_port: COM30
    programmer_serial_number: 1E660
    chip_part: PIC16F628A
    last_user: dmh
    testing_speed: 2100
    auto_test: true
    font_family: Consolas
    font_size: 14
    font_weight: normal
    skip_login: false
    auto_connect: true
    arduino_instance_id: 1
    debug: true
    firmware_folder: firmware
    auto_logoff_delay: 15
    bg_color: "#000000"
    fg_color: "#ff5500"
    arduino_wait: 4
    shutdown_on_exception: true
    auto_find: true
    sleep_tune: 1e-06
    full_screen: false
    touchscreen_enabled: false
    frameless: false
```

| Key | Description |
| --- | --- |
| `serial_port` | The default serial port. |
| `programmer_serial_number` | The default programmer serial number. |
| `chip_part` | The default chip part. |
| `last_user` | The last user to login. |
| `testing_speed` | The default testing speed. |
| `auto_test` | Whether to automatically run the test after programming. |
| `font_family` | The default font family. |
| `font_size` | The default font size. |
| `font_weight` | The default font weight. |
| `skip_login` | Whether to skip the login screen. |
| `auto_connect` | Whether to automatically connect to the Arduino. |
| `arduino_instance_id` | The default Arduino instance ID. |
| `debug` | Whether to enable debug mode. |
| `firmware_folder` | The default firmware folder. |
| `auto_logoff_delay` | The default auto logoff delay. |
| `bg_color` | The default background color. |
| `fg_color` | The default foreground color. |
| `arduino_wait` | The default Arduino wait time. |
| `shutdown_on_exception` | Whether to shutdown on exception. |
| `auto_find` | Whether to automatically find the Arduino. |
| `sleep_tune` | The default sleep tune. |
| `full_screen` | Whether to start in full screen mode. |
| `touchscreen_enabled` | Whether to enable touchscreen mode. |
| `frameless` | Whether to start in frameless mode. |


### Testing Configuration

The `testing` key in the `config.yaml` file defines how the test is run. Currently this is not implemented. The testing configuration is stored in a YAML object with the following format:

```yaml
testing:
    - description: Test Indicator On
        command: digital_write
        params: [13, 1]
        delay: 1
    - description: Show Text
        command: insert_text
        params: ["\n • Battery power on → Siren chirps and both LEDs flash  \n"]
        delay: 1
...
```

| Key | Description |
| --- | --- |
| `description` | Description of the command. Used for logging purposes. |
| `command` | The command to be executed. The available commands can be found in the [Test Commands](#test-commands) section. |
| `params` | The parameters to pass to the command. |
| `delay` | The delay in seconds after the command is run. Setting this to null uses the default testing speed. |

## Test Commands

The following commands are available for use in the testing configuration:

| Command | Description | Params | Example |
| ------- | ----------- | ------ | ------- |
| `digital_write` | Sets the value of a pin. | `pin_number`, `pin_value` | `digital_write`, [13, 1] |
| `insert_text` | Displays text on the screen. | `text` | `insert_text`, ["\n Text to display."] |
| `load_instructions` | Clears the screen and displays the instructions. | `filename` (optional) | `load_instructions`, ["instructions.txt"] |
| `wait_for_button` | Waits for a button to be pressed. | `timeout` (optional) | `wait_for_button`, 5 |
| `wait_for_input` | Waits for a pin to be set. | `pin_number`, `pin_value`, `timeout` (optional) | `wait_for_input`, [13, 1] |
| `set_indicator` | Sets the value of the indicator. | `indicator_value` | `set_indicator`, 1 |
| `indicator_on` | Turns on the indicator. | None | `indicator_on` |
| `indicator_off` | Turns off the indicator. | None | `indicator_off` |
| `set_test_indicator` | Sets the value of the test indicator. | `indicator_value` | `set_test_indicator`, 1 |
| `test_indicator_on` | Turns on the test indicator. | None | `test_indicator_on` |
| `test_indicator_off` | Turns off the test indicator. | None | `test_indicator_off` |
| `set_battery` | Sets the value of the battery. | `battery_value` | `set_battery`, 1 |
| `battery_on` | Turns on the battery output. | None | `battery_on` |
| `battery_off` | Turns off the battery output. | None | `battery_off` |
| `set_low_battery` | Sets the value of the low battery. | `low_battery_value`| `set_low_battery`, 1 |
| `low_battery_on` | Turns on the low battery output. | None | `low_battery_on` |
| `low_battery_off` | Turns off the low battery output. | None | `low_battery_off` |
| `set_remote` | Sets the value of the remote. | `remote_value` | `set_remote`, 1 |
| `set_pad` | Sets the value of the pad. | `pad_value` | `set_pad`, 1 |
| `set_relay1` | Sets the value of relay 1. | `relay1_value` | `set_relay1`, 1 |
| `set_relay2` | Sets the value of relay 2. | `relay2_value` | `set_relay2`, 1 |
| `set_all_pins_to_value` | Sets all pins to a value. | `pin_value` | `set_all_pins_to_value`, 1 |

## Misc Files

### Log Database

The `logs.db` file is a SQLite database is used to store log data. This database uses the following schema:

```sql
CREATE TABLE logs (id INTEGER PRIMARY KEY,
                   timestamp TEXT NOT NULL,
                   level TEXT NOT NULL,
                   logger TEXT NOT NULL,
                   message TEXT NOT NULL)
```
