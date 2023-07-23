import subprocess
import threading
import os
import time
from tkfontchooser import askfont
from tkinter import filedialog
from applogger import AppLogger
import usercreationdialog

from tkinter import (
    Menu,
    Button,
    END,
    Label,
    StringVar,
    messagebox,
    simpledialog,
)
from tkinter.font import Font
from tkinter.ttk import Frame
import tkinter as tk
from constants import *

app_logger = AppLogger("logger").get_logger()


class ManualControlWindow:
    """
    A class to create the manual control window. It creates a new Tkinter window with buttons
    for controlling the GPIO pins on the Arduino. 

    Attributes:
        root: The Tkinter root window.
        window: The parent window.
        usb_dev: The USB device object.
    """

    def __init__(self, parent=None, device=None):
        self.root = tk.Tk() # Create the root window
        self.root.title("Manual Control")
        self.root.call("source", "azure.tcl")
        self.root.call("set_theme", APPLICATION_THEME)
        self.root.iconbitmap("images\\pcb.ico")
        self.root.protocol("WM_DELETE_WINDOW", func=self.close)
        self.root.geometry("350x550")

        # self.pack()
        self.create_widgets()

        self.window = parent.window
        self.window.withdraw() # Hide the main window
        self.root.attributes("-topmost", 1)
        self.root.attributes("-topmost", 0)

        self.usb_dev = device # Get the USB device object

        self.values = [0, 0, 0, 0] # Placeholder for the pin values

    def create_widgets(self):
        read_button = tk.Button(
            master=self.root,
            text="battery",
            command=self.toggle_battery,
            width=20,
            height=4,
        )
        read_button.pack(pady=20)

        write_button = tk.Button(
            master=self.root,
            text="low battery",
            command=self.toggle_low_battery,
            width=20,
            height=4,
        )
        write_button.pack(pady=20)

        read_button = tk.Button(
            master=self.root,
            text="testing indicator",
            command=self.toggle_testing_indicator,
            width=20,
            height=4,
        )
        read_button.pack(pady=20)

        write_button = tk.Button(
            master=self.root,
            text="indicator",
            command=self.toggle_indicator,
            width=20,
            height=4,
        )
        write_button.pack(pady=20)

    def toggle_battery(self):
        pin = self.usb_dev.get_pin_by_function("battery")
        value = not self.values[0]
        self.usb_dev.digital_write(pin, value)
        self.values[0] = value

    def toggle_low_battery(self):
        pin = self.usb_dev.get_pin_by_function("low battery")
        value = not self.values[1]
        self.usb_dev.digital_write(pin, value)
        self.values[1] = value

    def toggle_testing_indicator(self):
        pin = self.usb_dev.get_pin_by_function("testing indicator")
        value = not self.values[2]
        self.usb_dev.digital_write(pin, value)
        self.values[2] = value

    def toggle_indicator(self):
        pin = self.usb_dev.get_pin_by_function("indicator")
        value = not self.values[3]
        self.usb_dev.digital_write(pin, value)
        self.values[3] = value

    def close(self):
        # set all pins low
        for pin in self.usb_dev.pins:
            self.usb_dev.digital_write(pin["pin_number"], 0)
        pin = self.usb_dev.get_pin_by_function("indicator")
        self.usb_dev.digital_write(pin, 1)
        self.window.deiconify()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


class MainWindow:
    """
    A class to create the main GUI. The GUI has a text box for displaying messages, a menu bar,
    labels for the selected device and USB connections and buttons for testing and programming.

    Attributes:
        parent: The main application process.
        window: The main window of the GUI.
        settings: The settings for the GUI.
        device_name: The name of the device being used.
        blocked: A boolean indicating if the GUI is currently blocked.
        queue: A list of commands to execute in the GUI.
        blinker_running: A boolean indicating if the blinker thread is running.
        blink_thread: The thread for the blinker.
        device: The USB handler for managing the USB connection.
    """

    def __init__(self, parent=None, settings=DEFAULT_SETTINGS):
        self.parent = parent
        self.window = tk.Tk()
        self.window.call("source", "azure.tcl")
        self.window.tk.call("set_theme", APPLICATION_THEME)
        self.window.iconbitmap("images\\pcb.ico")

        self.window.attributes("-topmost", 1)
        self.window.attributes("-topmost", 0)

        self.settings = settings
        self.device_name = None
        self.waiting = False

        if self.settings.get(KEY_DEBUG):
            app_logger.info("Main window initialized")

        font = Font(
            family=self.settings.get(KEY_FONT_FAMILY),
            size=self.settings.get(KEY_FONT_SIZE),
            weight=self.settings.get(KEY_FONT_WEIGHT),
        )

        # Initialize variables
        self.blocked = False
        self.queue = []
        # self.device = None
        self.blinker_running = False

        self.blink_thread = threading.Thread(target=self.do_blink)

        # Setup the GUI components
        self.setup_components(_font=font)

        # Populate the text area with the testing instructions
        self.load_text_from_file()
        self.testing = False
        self.button_pressed = False
        self.device = self.parent.usb_handler

    def setup_components(self, _font=None):
        """
        Setup the GUI components.
        """
        self.window.geometry("1000x700+350+350")
        self.window.title("EAX-500 Interface")

        # Handle window closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create frame for the bottom of the window
        self.bottom_frame = Frame(self.window)
        self.bottom_frame.pack(side="bottom", fill="x")

        # Create menu
        self.menu = Menu(self.window)  # Top Menu
        self.window.config(menu=self.menu)  # Add menu to window

        self.file_menu = Menu(self.menu, tearoff=0, font=_font)  # Top File Menu
        self.menu.add_cascade(label="File", menu=self.file_menu)  # Add File Menu
        self.file_menu.add_command(label="Logout", command=self.logout)  # Logout
        self.file_menu.add_command(  # Connect to Arduino
            label="Connect",
            command=lambda: self.connect(id=self.settings.get(KEY_ARDUINO_INSTANCE_ID)),
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_closing)

        self.settings_menu = Menu(self.menu, tearoff=0, font=_font)  # Top Settings Menu

        # Populate the device menu
        self.populate_menu(font=_font)

        self.menu.add_cascade(  # Add Settings Menu
            label="Settings", menu=self.settings_menu
        )
        self.settings_menu.add_command(  # Opens the settings file in notepad
            label="Modify Settings", command=self.open_settings
        )
        self.settings_menu.add_command(  # Displays the contents of the settings file in the text area
            label="Show Settings", command=self.show_settings
        )

        self.settings_menu.add_separator(background="gray")

        self.settings_menu.add_command(  # Add User
            label="Add User",
            command=self.add_user  # lambda: usercreationdialog.UserCreationDialog(self.window, user_settings=self.parent.settings, callback=self.add_user, title="Add User"),
            # command=lambda: messagebox.showinfo("Add User", "Not implemented yet"),
        )
        self.settings_menu.add_command(  # Remove User
            label="Remove User",
            command=lambda: messagebox.showinfo("Remove User", "Not implemented yet"),
        )
        self.settings_menu.add_command(  # Change Font
            label="Change Font", command=self.get_font  # FontChooser(self.window)
        ),
        self.settings_menu.add_command(  # Change Test Speed
            label="Test Speed",
            command=lambda: self.get_user_input(
                "Test Speed", "Enter Test Speed (%):", "testing_speed", "float"
            ),
        )
        self.settings_menu.add_command(  # Set Auto Login
            label="Auto Login",
            command=lambda: self.settings.set(
                "skip_login", messagebox.askyesno("Auto Login", "Login automatically?")
            ),
        )
        self.settings_menu.add_command(  # Set Auto Testing
            label="Auto Testing",
            command=lambda: self.settings.set(
                "auto_test",
                messagebox.askyesno("Auto Testing", "Run test automatically?"),
            ),
        )
        self.settings_menu.add_command(  # Select the chip
            label="Select Chip",
            command=lambda: self.get_user_input(
                "Select Chip", "Enter Chip: ", "chip_part"
            ),
        )
        self.settings_menu.add_command(  # Set the programmer serial number
            label="Programmer Serial Number",
            command=lambda: self.get_user_input(
                "Programmer Serinal Number",
                "Enter Serial Number: ",
                "programmer_serial_number",
            ),
        )
        self.settings_menu.add_command(  # Set the Arduino ID
            label="Arduino ID",
            command=lambda: self.get_user_input(
                "Arduino ID",
                "Enter the Arduino board ID: ",
                "arduino_instance_id",
                "int",
            ),
        )
        self.settings_menu.add_command(  # Show the manual control window
            label="Manual Control",
            command=lambda: self.show_manual_control(),
        )
        self.settings_menu.add_command(  # Select the firmware location
            label="Firmware Location",
            command=lambda: self.set_firmware_folder(),  # folder_dialog.select_folder(location=".", callback=self.settings.set(KEY_FIRMWARE_FOLDER, )),
        )
        self.help_menu = Menu(self.menu, tearoff=0, font=_font)  # Top Help Menu
        self.menu.add_cascade(label="Help", menu=self.help_menu)  # Add Help Menu
        self.help_menu.add_command(  # Shows the log file in the text area
            label="Show Log", command=self.show_log
        )

        options = [{"font": "parent"}]
        self.help_menu.add_command(  # Shows a dialog with information about the program
            label="About",
            command=lambda: messagebox.showinfo(
                "About",
                "EAX-300/500 Testing Interface\n\nVersion 0.0.1\n\nDesigned by: Daniel Hahaj\nhttps://github.com/dhahaj/eax500-tk_interface.git\nVisit the repository for more information.\n\n©2023 Detex Corporation",
                parent=self.window,
            ),
        )

        self.menu.add_separator(background="gray")

        self.menu.add_cascade(  # Add an easy way to connect to the fixture
            label="Connect",
            command=lambda: self.connect(id=self.settings.get(KEY_ARDUINO_INSTANCE_ID)),
        )

        # Create text area
        self.text_area_frame = tk.Frame(self.window)
        self.text_area_frame.pack(fill="both", expand=True)
        self.text_area = tk.Text(
            self.text_area_frame, wrap="word", state="disabled", font=_font
        )
        self.text_area.pack(
            side="left", fill="both", expand=True, padx=(10, 0), pady=(10, 0)
        )

        # Create Scrollbar
        self.scrollbar = tk.Scrollbar(
            self.text_area_frame, command=self.text_area.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        # Configure the text area to use the scrollbar
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        # Set up selected device
        self.selected_device = StringVar()
        self.selected_device.set("No device selected")

        self.firmware = None

        # Create buttons
        self.program_button = Button(
            self.bottom_frame,
            text="Program",
            height=2,
            width=10,
            font=_font,
            takefocus=1,
            command=self.program,
            padx=(3),
        )
        self.program_button.grid(row=0, column=0, sticky="w")

        # Create label for selected device
        self.device_label = Label(
            self.bottom_frame, textvariable=self.selected_device, font=_font
        )
        self.device_label.grid(row=0, column=1)

        self.usb_label = Label(self.bottom_frame, text="USB: Disconnected", font=_font)
        self.usb_label.config(fg="red")
        self.usb_label.grid(row=0, column=2)

        self.test_button = Button(
            self.bottom_frame,
            text="Test",
            height=2,
            width=10,
            font=_font,
            command=self.run_test,
            padx=(3),
        )
        self.test_button.grid(row=0, column=3, sticky="e")

        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_columnconfigure(2, weight=1)

    def populate_menu(self, font=None):
        """Populate the device menu."""
        self.device_menu = Menu(self.menu, tearoff=0, font=font)  # Top Device Menu
        self.menu.add_cascade(label="Device", menu=self.device_menu)

        for firmware in FIRMWARES:
            label_text = firmware["name"]
            version = firmware["version"]

            if label_text == "EAX500":
                self.device_menu.add_separator(background="gray")

            self.device_menu.add_command(
                label=label_text,
                command=lambda label_text=label_text, version=version: self.select_device(
                    label_text, version
                ),
            )

    def set_firmware_folder(self, folder="."):
        """Set the firmware folder."""
        new_folder = filedialog.askdirectory(
            initialdir=".", title="Select Firmware Folder"
        )
        if self.settings.get(KEY_DEBUG):
            print(f"Folder Selected: {new_folder}")
        self.settings.set(KEY_FIRMWARE_FOLDER, new_folder)

    def set_font(self, family="TkDefaultFont", size=12, style="normal"):
        """Set the font for the application."""
        # self.font = font
        # self.window.option_add("*Font", self.font)
        self.font = Font(family=family, size=size, weight=style)
        # self.text_area.config(font=self.font)
        # self.device_label.config(font=self.font)
        # self.usb_label.config(font=self.font)
        # self.button1.config(font=self.font)
        # self.button2.config(font=self.font)
        # self.menu.config(font=self.font)
        # self.file_menu.config(font=self.font)
        # self.device_menu.config(font=self.font)
        # self.help_menu.config(font=self.font)
        self.settings.set(KEY_FONT_FAMILY, family)
        self.settings.set(KEY_FONT_SIZE, size)
        self.settings.set(KEY_FONT_WEIGHT, style)
        # self.reload_window()
        self.show_settings()

    def add_user(self):
        """Add a user to the list of users."""
        # import user
        # user.
        # if self.settings.get(KEY_DEBUG):
        #     print(f'Adding user: {user}')
        # self.users.append(user)
        # self.user

        # Create a dialog to get the information for the new user
        dialog = usercreationdialog.UserCreationDialog(
            self.window, user_settings=self.parent.settings, dialog_title="Add User"
        )
        user = dialog.user_data
        if self.settings.get(KEY_DEBUG):
            print(f"Adding user: {user}")

    def show_manual_control(self):
        """Show the manual control window."""
        if self.device is not None and self.device.is_connected():
            manual = ManualControlWindow(self, device=self.device)
            manual.run()

    def device_connected_callback(self, connected, msg=None):
        """
        Callback function for when the device is connected or disconnected.

        :param connected: True if the device is connected, False otherwise.
        """
        if connected:  # Device connected
            print("Device connected!")
            app_logger.info("Fixture connected.")
            self.device.write_pin_by_func(pin_function="indicator", value=1)
            self.usb_label.config(fg="green")
            self.usb_label.config(text=f"USB Connected: {self.device.serial_port.port}")
            self.add_text("\r\nConnection established.")
            self.toggle_connect()  # Disable the connect button

        else:  # Device not connected
            print("Device failed to connect!")
            self.add_text("\r\nUnable to connect to device.")
            self.toggle_connect(_state="normal")
            app_logger.info("Unable to connect to device.")
            self.usb_label.config(fg="red")
            self.usb_label.config(text="USB: Disconnected")

    def connect(self, id=1):
        """
        Connect to the device.

        :param id: The instance ID of the Arduino board. Default is 1.
        """
        if self.settings.get(KEY_DEBUG):
            print("Number of active threads:", threading.active_count())
        if self.device is None:
            self.add_text("\r\nConnecting to fixture...")
            self.toggle_connect()  # Disable the connect button
            self.device.connect()  # Connect to the device
        elif not self.device.is_connected():
            self.device.connect()
            self.toggle_connect()  # Disable the connect button
            self.add_text("\r\nConnecting to fixture...")
        else:
            self.add_text("\r\nAlready connected to fixture.")

    def select_device(self, device, version):
        """
        Select the device to program. This will change the color of the device label.

        :param device: The device to program.
        """
        if not self.blocked:
            if self.settings.get(KEY_DEBUG):
                print(f"Device {device} selected")
            app_logger.info(f"Device {device} selected")

            # Change the color of the device label
            if device == "EAX500" or device == "EAX300":
                self.device_label.config(fg="green")
            else:
                self.device_label.config(fg="orange")

            self.selected_device.set(f"Selected device: {device}")
            self.device_name = device
            # Set the firmware file for use later
            self.firmware = f"firmware/{device}_{version}.hex"

    def set_user(self, user):
        """
        Set the user.

        :param user: The user.
        """
        app_logger.info(f"User {user} selected")
        self.user = user

    def add_text(self, text):
        """
        Add text to the text area.

        :param text: The text to add.
        """
        print(
            f"This function is being run by thread: {threading.current_thread().name}"
        )
        # Temporarily make the text widget editable
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(END, text + "\n")
        self.text_area.see(END)
        # Disable the text widget again
        self.text_area.config(state=tk.DISABLED)

    def clear_text(self):
        """
        Clear all text from the text area.
        """
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, END)
        # self.load_text_from_file("instructions.txt")  # Replace with your filename
        self.text_area.config(state=tk.DISABLED)

    def load_text_from_file(self, filename="instructions.txt"):
        """
        Load text from a file and add it to the text area.

        :param filename: The name of the file to load.
        """
        if os.path.exists(filename):
            with open(filename, "r") as file:
                content = file.read()
            self.add_text(content)
        else:
            self.add_text(f"{filename} not found!")

    def logout(self):
        """Logout of the application."""
        # if not self.blocked and not settings.get("skip_login"):
        if self.device is not None and self.device.is_connected():
            self.device.write_pin_by_func(pin_function="indicator", value=0)
            self.device.cleanup()
        # self.window.withdraw()
        # login = Login(window=self.window ,settings=settings, callback=self.set_user)
        # login.run()
        self.parent.user_logout()

    def program(self):
        """Program the device."""
        if not self.blocked and self.firmware is not None:
            # Check if the firmware file exists
            if not os.path.exists(self.firmware):
                self.add_text(f"{self.firmware} not found!")
                return

            self.blink_thread = threading.Thread(target=self.do_blink)
            self.blink_thread.start()

            self.blinker_running = True
            self.settings.__load__()

            chip = self.settings.get("chip_part")
            serial = self.settings.get("programmer_serial_number")
            command = ["up.exe", f"/part {chip} /q1 /s {serial} /p {self.firmware}"]

            if self.settings.get("debug"):
                print(" ".join(command))

            thread = threading.Thread(target=self.run_command, args=(command,))
            self.blocked = True

            # if self.parent.settings.get("debug"):
            #     self.add_text("Running test...")
            #     self.run_test()

            app_logger.info(f"Programming {self.device} started")
            thread.start()

    def run_command(self, command):
        """
        Run a command in a separate thread.

        :param command: The command to run.
        """
        self.settings.__load__()
        process = subprocess.run(command)
        self.blocked = False
        self.stop_blink()
        if process.returncode == 0:
            if self.settings.get("auto_test"):
                self.run_test()
            self.add_text("Programming successful.")
            app_logger.info(f"Programming {self.device} successful")
        else:
            self.add_text("Programming failed.")
            app_logger.error(
                f"Programming {self.device} failed. Error code: {process.returncode}"
            )

    def run_test(self):
        """Run the test."""
        if self.testing:
            self.button_pressed = True
        elif not self.blocked and self.device is not None and self.device.is_connected():
            self.blinker_running = False
            app_logger.info(f"Testing {self.device_name} started")
            self.clear_text()
            # Clear the queue
            self.queue = []
            speed = self.settings.get("testing_speed")

            self.queue.append(  # turn on indicator
                (1, self.device.write_pin_by_func, "testing indicator", 1)
            )

            self.queue.append(  # Add tasks to the queue
                (100, self.add_text, f"Starting test for {self.device_name}...")
            )

            self.queue.append(
                (
                    int(DEFAULT_TESTING_SPEED * speed),
                    self.add_text,
                    "\nTurning on battery power...",
                )
            )

            self.queue.append(  # turn on battery
                ((1), self.device.write_pin_by_func, "battery", 1)
            )

            self.queue.append(
                (
                    int(DEFAULT_TESTING_SPEED * speed),
                    self.add_text,
                    "Starting low battery test...",
                )
            )

            self.queue.append(  # turn on low battery
                ((1), self.device.write_pin_by_func, "low battery", 1)
            )

            self.queue.append((int(2000 * speed), self.add_text, "Low battery off."))

            self.queue.append(  # turn off low battery
                ((1), self.device.write_pin_by_func, "low battery", 0)
            )

            self.queue.append(
                (
                    int(1000 * speed),
                    self.add_text,
                    "Perform the following:\n\t  1. Press the key switch: The siren sounds\n\t  2. Press the cylinder switch: The LEDs turn on",
                )
            )

            self.queue.append((int(5000 * speed), self.add_text, "Testing complete."))

            self.queue.append((1, self.wait_for_button))

            self.queue.append(  # turn off battery
                ((1), self.device.write_pin_by_func, "battery", 0)
            )

            self.queue.append((1000, self.clear_text))

            self.queue.append((100, self.load_text_from_file, "instructions.txt"))

            self.queue.append(  # turn off indicator
                ((1), self.device.write_pin_by_func, "testing indicator", 0)
            )

            self.testing = True
            self.blocked = True
            # Start processing the queue
            self.process_queue()

        else:
            self.add_text("Cannot run test.")
            app_logger.error(f"Testing {self.device} blocked.")

    def process_queue(self):
        """Process the queue."""
        if self.waiting:
            return
        if self.queue:
            delay, task, *args = self.queue.pop(0)  # Get the next task
            print("\nTask started")
            self.window.after(
                delay, lambda: self.execute_task(task, args)
            )  # Execute the task after the delay
            print("Task executed\n")
        else:
            self.blocked = False
            self.testing = False

    def wait_for_button(self):
        print(f"Waiting for button {self.button_pressed}")
        self.waiting = True
        if not self.button_pressed:
            self.window.after(100, self.wait_for_button)
        else:
            self.button_pressed = False
            self.waiting = False
            self.process_queue()

    def execute_task(self, task, args):
        """
        Execute a task.

        :param task: The task to execute.
        :param args: The arguments to pass to the task.
        """
        task(*args)
        self.process_queue()  # Continue processing the queue

    def open_settings(self):
        """Open the settings file."""
        command = ["notepad.exe", "settings.json"]
        subprocess.Popen(command)

    def show_settings(self):
        """Show the settings in the text area."""
        self.clear_text()  # clear the text area
        self.settings.__load__()  # reload the settings
        self.add_text("Settings:\r\n")
        self.add_text("Settings file: settings.json")
        self.add_text(f"Settings file location: {self.settings.get_path()}")
        self.add_text("\r\n")
        self.add_text(f"Serial Port: {self.settings.get(KEY_SERIAL_PORT)}")
        self.add_text(
            f"Programmer serial number: {self.settings.get('programmer_serial_number')}"
        )
        self.add_text(f"Chip part: {self.settings.get(KEY_CHIP_PART)}")
        self.add_text(f"Auto test: {self.settings.get(KEY_AUTO_TEST)}")
        self.add_text(f"Testing speed: {self.settings.get(KEY_TESTING_SPEED)}")
        self.add_text(
            f"Font: {self.settings.get('font_family')}, {self.settings.get('font_size')}, {self.settings.get('font_style')}"
        )
        self.add_text(
            f"Arduino Instance ID: {self.settings.get(KEY_ARDUINO_INSTANCE_ID)}"
        )
        self.add_text(f"Skip Login: {self.settings.get(KEY_SKIP_LOGIN)}")
        self.add_text(f"Debug: {self.settings.get(KEY_DEBUG)}")
        self.add_text(f"Firmware Location: {self.settings.get(KEY_FIRMWARE_FOLDER)}")

    def get_font(self):
        """Get the font."""
        _font = self.settings.get("font_family")
        _size = self.settings.get("font_size")
        _style = self.settings.get("font_style")
        # current_font = Font(
        font_dict = {"family": _font, "size": int(_size), "weight": _style}
        fc = askfont(self.window, **font_dict)
        # fc = FontChooser(master=self.window) #, **font_dict)
        # fc.mainloop()
        # self.new_font = askfont(self.window, **current_font)#, title="Select Font", command=self.set_font)
        # print(fc)
        self.set_font(family=fc["family"], size=fc["size"], style=fc["weight"])
        # return new_font

    def toggle_connect(self, _state="disabled"):
        """Set the state of the connect menu items."""
        self.file_menu.entryconfig("Connect", state=_state)
        self.menu.entryconfig("Connect", state=_state)

    def toggle_state(self, _state="normal"):
        """Toggle the state of the window."""
        # state = self.window.state()
        if _state == "normal":
            self.window.deiconify()
        # self.window.state(_state)
        else:
            self.window.withdraw()
            # self.window.state("normal")

    def show_log(self):
        """Show the logs in the text area."""
        self.clear_text()
        self.add_text("Logs:\r\n")
        self.add_text(AppLogger.get_logs())

    def get_user_input(self, title, prompt, key, type=None):
        """
        Get user input.

        :param title: The title of the dialog box.
        :param prompt: The prompt to display.
        :param key: The key to store the value in.
        :param type: The type of the value.
        """
        # self.window.withdraw()  # hide the main window

        initialvalue = self.settings.get(key)

        if type == "int":
            user_input = simpledialog.askinteger(
                title=title, prompt=prompt, initialvalue=initialvalue
            )
        elif type == "float":
            user_input = simpledialog.askfloat(
                title=title, prompt=prompt, initialvalue=initialvalue
            )
        else:
            user_input = simpledialog.askstring(
                title=title, prompt=prompt, initialvalue=initialvalue
            )

        if user_input is not None:
            self.settings.set(key, user_input)
            print(user_input)
            self.settings.__save__()
        self.window.deiconify()  # show the main window

    def on_closing(self):
        """Handle the window closing."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # if self.device != None and self.device.is_connected():
            #     self.device.cleanup()
            # self.window.quit()
            self.parent.exit()

    def do_blink(self):
        """Blink the indicator light."""
        value = 0  # not self.device.read_pin(pin)
        self.blinker_running = True
        while self.blinker_running:
            self.device.write_pin_by_func("indicator", value)
            value = not value
            time.sleep(0.25)
        self.device.write_pin_by_func("indicator", 1)

    def stop_blink(self):
        """Stop the indicator light from blinking."""
        self.blinker_running = False
        try:
            self.blink_thread.join()
        except RuntimeError as e:
            print(e)

    def reload_window(self):
        """Reload the window."""
        self.test_button = Button(
            self.bottom_frame,
            text="Test",
            height=2,
            width=10,
            font=self.font,
            command=self.run_test,
            padx=(3),
        )
        # self.window.destroy()
        # self.window = tk.Tk()

    def close(self):
        """
        Close the window.
        """
        # self.window.destroy()
        self.parent.exit()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    main = MainWindow()
    main.run()
