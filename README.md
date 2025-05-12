# EAX Device Test & Programming Interface

This application provides a graphical user interface for testing and programming EAX hardware devices (e.g., EAX300, EAX500 series). It interacts with an Arduino-based test fixture using the TelemetrixAIO library and allows users to execute configurable test sequences, program firmware onto target devices, and manually control I/O pins.

## Features

*   **Graphical User Interface:** Built with PySide6 (Qt6) for intuitive operation.
*   **Configurable Test Sequences:** Define test steps, including pin manipulation, delays, user prompts, and input waiting, via a `config.yaml` file.
*   **Hardware Interaction:** Controls an Arduino (via TelemetrixAIO) for digital I/O to the device under test.
*   **Device Programming:** Supports programming target EAX devices using an external programmer tool (path and arguments configurable).
*   **Device Management:** Select different EAX device models, each potentially having different test sequences or firmware.
*   **Manual Control:** A dialog to manually toggle output pins on the test fixture.
*   **Asynchronous Operations:** Utilizes `asyncio` and `qasync` to ensure a responsive UI during I/O operations and tests.
*   **Logging:** Comprehensive logging of application events and test progress.
*   **Settings Management:** Persistent application settings (COM port, programmer paths, UI preferences, etc.).
*   **Theming:** Supports dark and light themes.
*   **Single Instance:** Prevents multiple instances of the application from running simultaneously.
*   **Firmware Update:** Capability to update the firmware on the Arduino test fixture itself.
*   **Resource Bundling:** Essential configuration files and images can be bundled within the application.

## Prerequisites

*   Python 3.8+
*   An Arduino board flashed with [Telemetrix4Arduino](https://github.com/MrYsLab/Telemetrix4Arduino) (or StandardFirmata for older test fixture firmware, if supported by configuration).
*   External programmer for the target EAX devices (e.g., ASIX PRESTO or similar).

## Dependencies

The application relies on the following Python libraries:

*   `PySide6`: For the graphical user interface (Qt6 bindings).
*   `qtpy`: Abstraction layer for Qt bindings (though PySide6 is explicitly used).
*   `qasync`: To integrate `asyncio` with the Qt event loop.
*   `telemetrix-aio`: For asynchronous communication with the Arduino.
*   `PyYAML`: For loading `config.yaml`.
*   `qdarkstyle`: For dark/light theming.
*   `pyserial`: For serial port listing (dependency of Telemetrix).

You can typically install these using pip:
```bash
pip install PySide6 qtpy qasync telemetrix-aio PyYAML qdarkstyle pyserial

```

## Configuration (config.yaml)

The application uses a YAML configuration file (`config.yaml`) to define various settings, including pin mappings, test sequences, and device definitions. This file is crucial for the application's operation and should be customized according to your hardware setup and testing requirements.
The configuration file is structured into several sections:

```yaml
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃                       ┃
┣━app_name              ┃
┣━app_version           ┃
┣━firmware              ┃
┃   ┣━path              ┃
┃   ┣━default_device    ┃
┃   ┗━files             ┃
┃       ┣━device_name   ┃
┃       ┣━firmware_file ┃
┃       ┗━version       ┃
┣━pins                  ┃
┃   ┣━function          ┃
┃   ┣━io_mode           ┃
┃   ┣━pin_number        ┃
┃   ┗━pullup_enabled    ┃
┣━testing               ┃
┃   ┣━cleanup           ┃
┃   ┃   ┣━action        ┃
┃   ┃   ┣━function      ┃
┃   ┃   ┗━value         ┃
┃   ┗━sequence          ┃
┃       ┣━action        ┃
┃       ┣━params        ┃
┃       ┣━description   ┃
┃       ┣━condition     ┃
┃       ┗━delay         ┃
┣━logging               ┃
┃   ┣━log_file          ┃
┃   ┣━log_level         ┃
┃   ┣━log_format        ┃
┃   ┣━log_rotation      ┃
┃   ┣━log_retention     ┃
┃   ┗━database_file     ┃
┃                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
```

The application's behavior is heavily driven by config.yaml. This file defines:
* **Pin Mappings: Maps functional names (e.g., "battery", "low battery") to Arduino pin numbers and I/O modes.
* **Test Sequences: A list of steps for automated testing. Each step defines an action (e.g., write_pin, delay, wait_for_input, wait_for_button, message).
* **Cleanup Sequences: Steps to run after a test to reset hardware.
* **Device Definitions: Information about supported EAX devices, including firmware paths.
* **Chip Options: List of microcontroller part numbers for the programmer.
* **Logging: Configuration for logging, including log file path, log level, and log format.

A default config.yaml is expected. If not found, the application may attempt to extract a bundled version.

## Installation

* Clone this repository or download the source code.
* Install Python 3 if you haven't already.
* Install the required dependencies (see Dependencies).
* Ensure your Arduino is flashed with the appropriate Telemetrix firmware.
* Configure your external EAX device programmer and ensure its path is correctly set in the application settings or config.yaml.
* Review and customize config.yaml for your specific hardware setup and test requirements.


## Usage

Run the main application script:
```bash
python main.py
```
Use code with caution.
Bash
1. Connect to Arduino:
   - Connect the Arduino to your computer via USB.
   - Select the appropriate COM port in the application settings.
   - Click "Connect" to establish communication with the Arduino.
2. Select Device:
   - Choose the target EAX device model from the "Device" menu.
3. Program Device (Optional):
   - If you need to program firmware onto the EAX device, click the "Program" button. This uses the configured external programmer.
4. Run Test:
   - Click the "Test" button to start the automated test sequence for the selected device.
   - Follow any on-screen prompts. The main text area will display test progress and messages.
   - If the test sequence includes a wait_for_button step, the "Test" button may also act as the "Continue" button.
  
Use the "Connect" menu item or button. The application can auto-detect the COM port or use a configured one.
The USB status indicator will show the connection state.
Select Device:
Choose the target EAX device model from the "Device" menu.
Program Device (Optional):
If you need to program firmware onto the EAX device, click the "Program" button. This uses the configured external programmer.
Run Test:
Click the "Test" button to start the automated test sequence for the selected device.
Follow any on-screen prompts. The main text area will display test progress and messages.
If the test sequence includes a wait_for_button step, the "Test" button may also act as the "Continue" button.
Manual Control (Optional):
Access "Manual Control" from the menu to directly toggle output pins on the Arduino.
Settings:
Access "Modify Settings" from the menu to configure COM ports, programmer paths, UI preferences, test parameters, etc.


## Modules
* **main.py**: The main application entry point. Initializes the UI (MainWindow), handles user interactions, and orchestrates the overall application flow.
* **test_controller.py**: Manages the execution of automated test sequences. Reads steps from config.yaml, interacts with AIODevice for hardware control, and emits signals to update the UI.
* **arduino.py**: Provides the AIODevice class, an abstraction layer for communicating with the Arduino test fixture using TelemetrixAIO. Handles pin configuration, digital I/O, and input callbacks.
* **config_loader.py**: Loads and provides access to configurations from config.yaml (pin definitions, test sequences, device settings).
* **settings.py (assumed)**: Manages persistent application settings.
* **constants.py (assumed)**: Defines shared constants used throughout the application.
* **globals.py (assumed)**: Provides global instances like the logger.
* **ui/ (assumed directory)**: Contains UI files generated from Qt Designer (.ui files converted to .py).
* **util/ (assumed directory)**: Utility functions, possibly including resource management.
* **device.py (assumed)**: Defines the Device class representing the EAX device under test.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



# EAX Test Fixture Interface

This is a Python version of the EAX Test Fixture Interface. It is a GUI built on the Qt framework that allows the user to control the EAX Test Fixture. It is designed to be used with the telemetrix Arduino library. See the [firmware](#test-fixture-firmware) section for more information.

## Table of Contents

- [EAX Device Test \& Programming Interface](#eax-device-test--programming-interface)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Dependencies](#dependencies)
  - [Configuration (config.yaml)](#configuration-configyaml)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Modules](#modules)
  - [Contributing](#contributing)
  - [License](#license)
- [EAX Test Fixture Interface](#eax-test-fixture-interface)
  - [Table of Contents](#table-of-contents)
  - [Key Bindings](#key-bindings)
  - [Installation](#installation-1)
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
