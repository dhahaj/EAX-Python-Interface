
from constants import *




class Device:

    def __init__(self, name):
        self.name = name
        self.version = None
        self.firmware = None
        self.set_version()
        self.set_firmware()

    def set_version(self):
        """ Set the version of the device. """
        for firmware in FIRMWARES:
            if firmware[FIRMWARE_NAME] == self.name:
                self.version = firmware[FIRMWARE_VERSION]
                break

    def set_firmware(self):
        """ Set the firmware of the device. """
        self.firmware = f'{self.name}_{self.version}.hex'

    def get_name(self):
        return self.name
    
    def get_version(self):
        return self.version
    
    def get_firmware(self):
        return f'firmware/{self.firmware}'
    
    def set_name(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}_{self.version}.hex'

    def __repr__(self):
        return f'{self.name}_{self.version}.hex'
    
    def __eq__(self, other):
        if not isinstance(other, Device):  # suggestion 1
            return False
        return self.name == other.name and self.version == other.version
    

    

