# EAX Device Test & Programming Interface

This application provides a graphical user interface for testing and programming EAX hardware devices (e.g., EAX300, EAX500 series). It interacts with an Arduino-based test fixture using the TelemetrixAIO library and allows users to execute configurable test sequences, program firmware onto target devices, and manually control I/O pins.

## Table of Contents

- [EAX Device Test \& Programming Interface](#eax-device-test--programming-interface)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Dependencies](#dependencies)
  - [Configuration (config.yaml)](#configuration-configyaml)
    - [Device Configuration](#device-configuration)
    - [Testing Configuration](#testing-configuration)
    - [Pin Configuration](#pin-configuration)
  - [Installation](#installation)
  - [Modules](#modules)
  - [Contributing](#contributing)
  - [License](#license)


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

Install all the dependencies using pip:
```bash
pip install -r requirements.txt

```

## Configuration (config.yaml)

The application uses a YAML configuration file (`config.yaml`) to define various runtime settings. This file is expected to be in the same directory as the main executable, and if not found, the application will attempt to extract a bundled version with default settings. The structure of the `config.yaml` file is as follows:

```yaml
┏━app_name             
┣━app_version          
┃
┣━devices
┃   ┣━firmware_path            
┃   ┣━label_styles
┃   ┣━label_size   
┃   ┗━firmware_files           
┃       ┣━device_name  
┃       ┣━firmware_name
┃       ┗━color     
┃
┣━pins                 
┃   ┗━<function>
┃       ┗━<mode, number, pullup>
┃
┣━testing              
┃   ┣━cleanup          
┃   ┃   ┗━<action, function, value>       
┃   ┗━sequence         
┃       ┗━<action, params...>       
┃
┣━window
┃   ┗━usb_label
┃       ┣━connected_style
┃       ┣━connected_text
┃       ┣━connecting_style
┃       ┣━disconnected_style
┃       ┣━disconnected_text
┃       ┗━text  
┃
┣━logging              
┃   ┣━log_file         
┃   ┣━log_level        
┃   ┣━log_format       
┃   ┣━log_rotation     
┃   ┣━log_retention    
┃   ┗━database_file    
┃
┣━chip_options
┃   ┗━<chip_part_numbers>
┃
┗━programmer_config
    ┣━executable
    ┣━programmer
    ┗━arguments[...]
```

### Device Configuration
The `devices` key in the `config.yaml` file contains the device configuration. The device configuration is stored in a YAML object with the following format:

```yaml
devices:
  firmware_path: <path_to_firmware_folder>
  label_styles: <style>
  label_size: <size>
  firmware_files:
    - device_name: <device_name>
      firmware_name: <firmware_name>
      color: <color>
```

| Key | Description |
| --- | ----------- |
| `firmware_path` | The path to the firmware files. |
| `label_styles` | The styles for the labels (connected, disconnected, connecting). |
| `label_size` | The size of the labels. |
| `firmware_files` | A list of firmware files for different devices. Each entry contains the device name, firmware name, and color. |


### Testing Configuration

The `testing` key in `config.yaml` file defines how the test is run. The testing configuration is stored in a YAML object with the following format:

```yaml
testing:
  sequence:
    - action: message
      text: "Testing Battery function"

    - action: write_pin
      function: low battery
      value: 1

    - action: delay
      duration_ms: 1000

  cleanup:
    - action: write_pin
      function: test_indicator
      value: 0
    - action: write_pin
      function: low battery
      value: 0
```


The `sequence` key in the `config.yaml` file contains a sequence of actions to be performed during the testing process. The possible options for an action are:

| Action |  Parameters | Description |
| --- | --- | --- |
| `message` | `text` | Display a message. |
|  --- | `if_has (optional)` | Optional condition to check if the action should be executed.
| `delay`  | `duration_ms (optional)` | Delay in milliseconds. Defaults to testing speed. |
|  --- | `if_has (optional)` | Optional condition to check if the action should be executed. |
| `write_pin` | `function` | Write a value to the pin with the specified function. |
|  --- | `value` | The value to write to the pin. |
|  --- | `if_has (optional)` | Optional condition to check if the action should be executed. |
| `wait_for_input` | `function` | Wait for input on the pin with the specified function. |
|  --- | `if_has (optional)` | Optional condition to check if the action should be executed. |
| --- | `timeout_key` | The key used in the settings to set the timeout. |
| --- | `message_on_pass` | The message to display on pass. |
| --- | `message_on_fail` | The message to display on fail. |
| --- | `expected_value` | The expected value. (0 or 1) |
| --- | `fail_on_timeout` | Whether to fail on timeout. |
| `wait_for_button` | `timeout_key` | The key used in the settings to set the button timeout. |
| --- | `message_on_fail` | The message to display on fail. |
| --- | `fail_on_timeout` | Whether to fail on timeout. |


### Pin Configuration
The `pins` key in the `config.yaml` file contains the pin configuration. The pin configuration is stored in a YAML object with the following format:

```yaml
pins:
  - function: <function_name>
    io_mode: <input|output|input_pullup>
    pin_number: <pin_number>
    pullup_enabled: <true|false>
```

| Key | Description |
| --- | ----------- |
| `function` | The functional name of the pin (e.g., "battery", "low battery"). |
| `io_mode` | The I/O mode of the pin (e.g., "input", "output", "input_pullup"). |
| `pin_number` | The Arduino pin number associated with the function. |
| `pullup_enabled` | Whether the internal pull-up resistor is enabled (true/false). |


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

