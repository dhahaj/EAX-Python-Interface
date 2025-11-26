# EAX Device Test & Programming Interface - Claude Code Guide

## Project Overview

This is a PySide6 (Qt6) application for testing and programming EAX hardware devices (EAX300, EAX500 series). The application interfaces with an Arduino test fixture using TelemetrixAIO and executes configurable test sequences defined in YAML.

## Architecture

### Core Components

1. **main.py** - Main application entry point and MainWindow class
   - Orchestrates UI and application flow
   - Manages device connection/disconnection
   - Handles test execution and firmware programming
   - Uses qasync for asyncio integration with Qt

2. **test_controller.py** - Test sequence execution engine
   - Reads test sequences from config.yaml
   - Executes actions: message, delay, write_pin, wait_for_input, wait_for_button
   - Emits signals for UI updates
   - Handles cleanup sequences

3. **arduino.py** - Hardware abstraction layer (AIODevice class)
   - Wraps TelemetrixAIO for Arduino communication
   - Manages pin configuration and digital I/O
   - Handles input callbacks

4. **config_loader.py** - Configuration management
   - Loads config.yaml (pin definitions, test sequences, device settings)
   - Provides access to configuration throughout the app

5. **settings.py** - Persistent application settings
   - Stores COM port, programmer paths, UI preferences, etc.

### UI Components

- **settings_dialog.py** - Application settings dialog
- **manual_widget.py** - Manual pin control interface
- **busy_dialog.py** - Progress dialogs for long-running operations
- **status_widget.py** - Device status display
- **log_view.py** - Log viewer
- **help_dialog.py** - Help documentation viewer
- **chipSelectDialog.py** - Chip selection for programming
- **editor.py** - Configuration editor

### Supporting Modules

- **device.py** - Device class representing EAX devices under test
- **firmware_update.py** - Arduino firmware update functionality
- **applogger.py** - Logging configuration and management
- **constants.py** - Shared constants
- **globals.py** - Global instances (logger)
- **imports.py** - Centralized imports
- **usbinfo.py** - USB device information
- **up.py, up_progress.py** - Upload/programming utilities

## Configuration System

### config.yaml Structure

```yaml
devices:
  firmware_path: <path>
  firmware_files: [{ device_name, firmware_name, color }]

pins:
  - function: <name>
    io_mode: <input|output|input_pullup>
    pin_number: <pin>
    pullup_enabled: <bool>

testing:
  sequence: [{ action, params... }]
  cleanup: [{ action, params... }]

programmer_config:
  executable: <path>
  programmer: <type>
  arguments: [...]

chip_options: [<part_numbers>]

logging:
  log_file: <path>
  log_level: <level>
```

### Test Sequence Actions

| Action | Parameters | Description |
|--------|-----------|-------------|
| message | text, if_has (optional) | Display message |
| delay | duration_ms, if_has (optional) | Wait specified milliseconds |
| write_pin | function, value, if_has (optional) | Write to pin |
| wait_for_input | function, timeout_key, expected_value, message_on_pass/fail, fail_on_timeout, if_has (optional) | Wait for input |
| wait_for_button | timeout_key, message_on_fail, fail_on_timeout | Wait for button press |

## Development Guidelines

### When Making Changes

1. **Pin Configuration**: Edit config.yaml pins section, not hardcoded values
2. **Test Sequences**: Modify testing.sequence in config.yaml
3. **Device Support**: Add entries to devices.firmware_files in config.yaml
4. **UI Changes**: Modify .ui files in QtDesigner/, regenerate .py files if needed
5. **Hardware Communication**: Changes to Arduino interaction go in arduino.py
6. **Test Logic**: Modify test_controller.py for sequence execution changes

### Code Style

- Python 3.8+ with type hints (as seen in recent commits)
- Async/await pattern for I/O operations
- Qt signals/slots for UI updates
- YAML-driven configuration over hardcoding

### Key Patterns

1. **Async Operations**: Use qasync event loop, `async def` methods in main.py
2. **Pin References**: Use functional names from config.yaml, not pin numbers
3. **Logging**: Use logger from globals.py
4. **Resource Loading**: Bundled resources via resource_rc.py or external files
5. **Single Instance**: App prevents multiple simultaneous instances

### Testing

- Test fixtures in tests/ directory
- pytest.ini configuration exists
- Manual testing via Manual Control dialog in UI

### External Dependencies

- **Arduino**: Must run Telemetrix4Arduino firmware
- **Programmer**: External tool (e.g., ASIX PRESTO) for device programming
- **Hardware**: Arduino test fixture connected via USB serial

## Common Tasks

### Adding a New Device

1. Add firmware file to firmware/ directory
2. Add entry to config.yaml devices.firmware_files
3. Restart application to detect new device

### Modifying Test Sequence

1. Edit config.yaml testing.sequence
2. Application reads config on startup
3. No code changes required unless adding new action types

### Adding New Pin Function

1. Add pin definition to config.yaml pins section
2. Reference by function name in test sequences
3. Available in Manual Control dialog automatically

### Debugging Test Failures

1. Check logs (configured in config.yaml logging section)
2. Use Manual Control to test individual pins
3. Review test_controller.py execution flow
4. Check Arduino connection and firmware

## Important Notes

- **Config-Driven**: Most behavior controlled by config.yaml, not code
- **Async Architecture**: UI remains responsive during I/O operations
- **Hardware Dependencies**: Requires physical Arduino test fixture
- **Single Codebase**: All variants/devices share same code with different configs
- **Resource Bundling**: Can run standalone with bundled resources
- **Type Safety**: Recent work adding type hints (see commits)

## Recent Changes

According to git log:
- Type hints added to disconnect_device and firmware update methods
- Progress bar implementation refactored
- Job handling improved in up_progress.py
- Python analysis settings enhanced

## File Locations

- **Config**: config.yaml in application directory
- **Firmware**: firmware/ directory
- **Logs**: Per config.yaml logging.log_file
- **UI Files**: QtDesigner/ for .ui files, ui/ for generated .py
- **Resources**: images/, bundled in resource_rc.py
- **Tests**: tests/ directory

## When Editing Code

1. Always preserve async/await patterns
2. Don't hardcode pins or device settings
3. Maintain Qt signal/slot connections
4. Keep UI responsive (no blocking operations)
5. Use type hints for new/modified functions
6. Update config.yaml for configuration changes
7. Test with physical hardware when possible

## Dependencies to Be Aware Of

- PySide6: Qt6 Python bindings
- qasync: Asyncio + Qt integration
- telemetrix-aio: Arduino communication
- PyYAML: Configuration parsing
- qdarkstyle: Theme support
- pyserial: Serial port access

## Build/Distribution

- main.spec: PyInstaller specification
- Bundles resources via resource_rc.py
- Can package as standalone executable
- Includes default_resources.zip for fallback configs
