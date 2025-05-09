import yaml
from typing import List, Dict, Any, Tuple
import os
from util.resources import extract_file_from_resource
import copy

class ConfigLoader:
    """Load the config from a YAML file."""


    def __init__(self, filename: str = "config.yaml") -> None:
        self.filename = filename
        # If the config file does not exist, try to extract it from resources
        if not os.path.exists(filename):
            try:
                import util.config_resources_rc
                filename = extract_file_from_resource(":/config.yaml")
                print(f"Config file extracted from resources: {filename}")
            except FileNotFoundError as e:
                print(f"Error: {e}")
                raise FileNotFoundError(f"Config file not found: {filename}")
        self.data = self.load_from_file(filename)

    def load_from_file(self, filename: str) -> Dict[str, Any]:
        """Load the config from a YAML file."""
        try:
            with open(filename, 'r', encoding='utf-8') as stream:
                return yaml.safe_load(stream)
        except FileNotFoundError:
            print(f"Config file not found: {filename}")
            raise
        except yaml.YAMLError as e:
            print(f"YAML parsing error in file {filename}: {e}")
            raise

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
        return [entry.get('device_name', '') for entry in files if 'device_name' in entry]

    @property
    def default_device(self) -> str:
        """Return the default device."""
        firmware = self.data.get('firmware', {})
        return firmware.get('default_device', '')

    @property
    def chip_options(self) -> List[str]:
        """Return a list of chip options."""
        return self.data.get('chip_options', [])

    def get_test_sequence(self) -> List[Dict[str, Any]]:
        """Return the list of test steps."""
        return self.data.get('testing', {}).get('sequence', [])

    @property
    def test_sequence(self) -> List[Dict[str, Any]]:
        """Return the test sequence."""
        return self.get_test_sequence()

    def get_cleanup_sequence(self) -> List[Dict[str, Any]]:
        """Return the list of cleanup steps."""
        return self.data.get('testing', {}).get('cleanup', [])
    
    def reload(self) -> bool:
        """Reload the config from the file, do nothing if the file has an error."""
        # keep the old config data in case of error
        old_config = copy.deepcopy(self.data)
        try:
            new = self.load_from_file(self.filename)
            if not new:
                raise ValueError("Loaded empty config")
            self.data = new
            return True
        except Exception as e:
            print(f"Error reloading config file: {e}")
            self.data = old_config
            return False



_config_singleton: "ConfigLoader|None" = None

def get_instance(**kwargs) -> "ConfigLoader":
    """
    Return the process-wide ApplicationSettings.
    The first call constructs it, later calls hand bac  k the same object.
    Extra kwargs are silently ignored after the first call.
    """
    global _config_singleton
    if _config_singleton is None:
        _config_singleton = ConfigLoader(**kwargs)
    return _config_singleton


if __name__ == '__main__':
    config = ConfigLoader()
    print(config.get_test_sequence())
    # print(config.get('logging').get("database_file", None))
    # print( config.get('logging').get('database_file', None) )
    # print( config.get('logging').get('log_file', None) )
    # print( config.get('logging').get('log_level', 'DEBUG') )
    # print( config.get('logging').get('log_format', "{time} | {level} | {message}") )
    # print( config.get('logging').get('log_rotation', "00:00") )
    # print( config.get('logging').get('log_retention', "7 days") )

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
