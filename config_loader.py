import yaml
from typing import List, Dict, Any, Tuple
from rich import *
import os
from util.resources import extract_file_from_resource

class ConfigLoader:
    """Load the config from a YAML file."""

    def __init__(self, filename: str = "config.yaml") -> None:
        # If the config file does not exist, try to extract it from resources
        if not os.path.exists(filename):
            try:
                filename = extract_file_from_resource(":/config.yaml")
            except FileNotFoundError as e:
                print(f"Error: {e}")
                raise FileNotFoundError(f"Config file not found: {filename}")
        self.data = self.load_from_file(filename)

    def load_from_file(self, filename: str) -> Dict[str, Any]:
        """Load the config from a YAML file."""
        with open(filename, 'r', encoding='utf-8') as stream:
            return yaml.safe_load(stream)
        
    def get(self, key: str) -> Any:
        """Get a value from the config."""
        return self.data.get(key, None) 
    
    @property
    def config(self) -> Dict[str, Any]:
        """Return the config data"""
        return self.data

    @property
    def version(self) -> str:
        """Return the version."""
        return self.data.get('version', '0.0.0')

    @property
    def settings(self) -> Dict[str, Any]:
        """Return the settings configuration."""
        return self.data.get('settings', {})

    def get_default_setting(self, key: str) -> Any:
        """Return the default value for a setting."""
        return self.settings.get(key, None)

    @property
    def pins(self) -> List[Dict[str, Any]]:
        """Return the pins configuration."""
        return self.data.get('pins', [])

    @property
    def firmware_path(self) -> str:
        """Return the firmware path."""
        return self.data.get('firmware', {}).get('path', None)

    def get_firmware(self) -> List[Dict[str, Any]]:
        """Return the firmware data."""
        return self.data.get('firmware', {}).get('files', [])

    @property
    def devices(self) -> List[str]:
        """Return a list of devices."""
        firmware = self.data.get('firmware', {})
        files = firmware.get('files', [])
        return [entry.get('basename', '') for entry in files if 'basename' in entry]

    @property
    def default_device(self) -> str:
        """Return the default device."""
        firmware = self.data.get('firmware', {})
        return firmware.get('default_device', '')

    @property
    def chip_options(self) -> List[str]:
        """Return a list of chip options."""
        return self.data.get('chip_options', [])

    def get_testing_config(self) -> List[Dict[str, Any]]:
        """Return the test instructions."""
        return self.data.get('testing', [])


def validate_config(yaml_file: str) -> Tuple[bool, List[str]]:
    """Validate the config file contains the required keys."""
    required_keys = ["firmware", "testing", "settings", "pins"]

    # Load the YAML file
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Check for required keys
    missing_keys = [key for key in required_keys if key not in data]

    if missing_keys:
        print(
            f"Error: The following keys are missing from the YAML file: {', '.join(missing_keys)}")
        return False, missing_keys
    else:
        print("YAML file is valid!")
        return True, []


if __name__ == '__main__':
    # validate_config('config.yaml')

    config = ConfigLoader()

    print(config.get('logging').get("database_file", None))
    print( config.get('logging').get('database_file', None) )
    print( config.get('logging').get('log_file', None) )
    print( config.get('logging').get('log_level', 'DEBUG') )
    print( config.get('logging').get('log_format', "{time} | {level} | {message}") )
    print( config.get('logging').get('log_rotation', "00:00") )
    print( config.get('logging').get('log_retention', "7 days") )

    # pins = config.pins
    # print(type(pins[0]))
    # print(config.version)
    # print(config.firmware_path)
    # print(config.settings)
    # print(config.get_firmware())
    # print(config.pins)
    # print(config.devices)
    # testing = config.get_test_instructions()
    # print(testing)
