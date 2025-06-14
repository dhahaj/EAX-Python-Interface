# Configuration File

The application settings, test sequences and pin assignments are defined in `config.yaml`. Editing this file allows the test interface to be adapted to different hardware configurations without modifying the source code.

## Main Sections

- **`app_name` / `app_version`** – Displayed in the title bar and about dialog.
- **`window`** – Strings and style options for the main window widgets.
- **`devices`** – Maps board names to firmware images and colours used in the device menu.
- **`pins`** – Defines each pin used by the fixture. Each entry includes:
  - `function` – A human readable name used throughout the configuration.
  - `io_mode` – Either `output`, `input`, or `input_pullup` depending on the wiring.
  - `pin_number` – The Arduino pin number.
  - `pullup_enabled` – Whether the internal pull‑up resistor is enabled.
- **`logging`** – Log file paths, levels and rotation settings.
- **`testing`** – Sequence of actions performed when running an automated test. The cleanup steps are listed under `testing.cleanup`.
- **`programmer_config`** – Location of the programming utility and the command line arguments used when flashing firmware.
- **`chip_options`** – List of selectable chip types in the settings dialog.
- **`settings`** – Default values for user‑changeable settings such as serial port and testing speed.

## Example Test Step

```yaml
- action: write_pin
  function: battery
  value: 1
```

Each entry under `testing.sequence` describes a single action. The example above turns on the pin defined as `battery`. Supported actions include `write_pin`, `delay`, `message`, `wait_for_button` and others used by the application code.

## Customising

1. Adjust the `firmware_files` list to add or remove supported boards.
2. Edit the `pins` section to match your fixture wiring.
3. Modify the `testing.sequence` steps to reflect the procedure required for your product.

Any changes to `config.yaml` are loaded at start‑up. Reload the configuration from the settings menu if the application is already running.
