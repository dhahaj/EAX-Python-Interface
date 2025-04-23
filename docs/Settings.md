# Settings

The settings for this application are stored in the windows registry under the key `Computer\Hkey_Current_User\Software\Detex Corp\EAX Interface`. The settings can be modified by clicking on the settings menu item in the main window. The settings can also be edited by opening the registry editor and navigating to the key mentioned above.

### Descriptions for the settings

- serial_port: The serial port that is connected to the device. Example: "COM8".
- programmer_serial_number: The serial number of the programmer. Example: "1E660".
- chip_part: The part number of the chip on the device. Example: "PIC16F627A".
- last_user: The last user who used the software. Example: "dmh".
- testing_speed: The speed of testing in Hz. Example: 1584.
- auto_test: If set to true, the software will automatically start testing when it starts up.
- font_family: The font family used for display text. Example: "Segoe UI".
- font_size: The size of the font. Example: 12.
- font_weight: The weight of the font. Example: "normal".
- skip_login: If set to true, the software will not prompt for a user login.
- auto_connect: If set to true, the software will automatically attempt to connect to the device on startup.
- arduino_instance_id: The instance ID of the Arduino software. Example: 15.
- debug: If set to true, the software will log extra information for debugging purposes.
- firmware_folder: The path to the folder containing the device firmware. If empty, the software will look in the default location.
- inactivity_delay: The delay in minutes before the software will automatically log off the current user. Example: 3.
- bg_color: The background color of the software, specified as a hex color. Example: "#000000".
- fg_color: The foreground color of the software, specified as a hex color. Example: "#ffffff".
- arduino_wait: The time in seconds to wait for the Arduino software to start. Example: 2.
- shutdown_on_exception: If set to true, the software will automatically shut down if it encounters an exception.
- auto_find: If set to true, the software will automatically find and connect to the device on startup.
- sleep_tune: The delay in seconds to wait for tuning to complete. Example: 1e-06.
- firmware_location: The path to the firmware file. Example: "./firmware".
- full_screen: If set to true, the software will start in full screen mode.

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
    "font_weight": "normal",
    "font_color": "#000000",
    "skip_login": true,
    "auto_connect": false,
    "arduino_instance_id": 1,
    "debug": true,
    "firmware_folder": "",
    "firmware_location": "./firmware",
    "shutdown_on_exception": true,
    "auto_find": true,
    "sleep_tune": 1e-06,
    "arduino_wait": 2,
    "full_screen": false
}
```

![alt text](../images/SettingsMenu.png)
