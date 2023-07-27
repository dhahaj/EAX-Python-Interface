from tkinter.constants import *
from constants import *
from login import Login
from windows import MainWindow, ManualControlWindow
from settings import Settings
import usbhandler
from applogger import AppLogger

class Application:
    """
    This is the main application class.
    """

    def __init__(self):
        # initialize the application
        self.state = ST_INIT
        self.settings = Settings()
        # setup the USB handler
        self.usb_handler = usbhandler.USBHandler(
            port=self.settings.get(KEY_COM_PORT),
            arduino_instance_id=self.settings.get(KEY_ARDUINO_INSTANCE_ID),
            device_connected_callback=self.connection_callback,
            debug=self.settings.get(KEY_DEBUG),
        )

        # setup the main window
        self.main_window = MainWindow(
            parent=self, settings=self.settings
        )
         # setup the login window
        self.login_window = Login(
            parent=self,
            window=self.main_window,
            settings=self.settings,
            callback=self.user_login,
        )
        # self.login_window = None
        # setup the login window
        # if self.settings.get(KEY_SKIP_LOGIN):  # no login screen
            # self.login_window.root.withdraw()
        # self.main_window.run()
        # else:  # login screen
            # self.main_window.window.withdraw()
           
            # self.login_window.run()
     
        self.user = None
        self.state = ST_LOGGED_OUT
        self.main_window.run()

    def get_setting(self, key):
        # return a setting from the settings file
        return self.settings.get(key)

    def set_setting(self, key, value):
        # set a setting in the settings file
        self.settings.set(key, value)

    def transition_to_main(self):
        # handle transition to main window state
        self.state = ST_LOGGED_IN
        self.main_window.run()

    def manual_control(self):
        # handle manual control
        pass

    def user_login(self, username):
        """handle user login"""
        
        if username is None:
            self.exit()
            return
        
        self.user = username
        self.login_window.withdraw()
        self.main_window.deiconify()
        self.settings.set(KEY_LAST_USER, self.login_window.username_entry.get())
        AppLogger.info(f"User {self.user} logged in.")
        self.login_window.password_entry.delete(0, END)
        # self.transition_to_main()

    def user_logout(self):
        # handle user logout
        self.user = None
        self.main_window.withdraw()
        if self.login_window is None:
            self.login_window = Login(self, self.main_window, self.settings, self.user_login)
            self.login_window.run()
        else:
            self.login_window.deiconify()

    def connection_callback(self, connected, msg=None):
        # handle connection callback
        self.main_window.device_connected_callback(connected, msg)

    def run(self):
        # main application loop
        # self.main_window.mainloop()

        if self.settings.get(KEY_AUTO_LOGIN): # no login screen
            self.login_window.withdraw()
            self.main_window.run()
        else:
            self.login_window.run()

    def exit(self):
        # exit the application
        if self.login_window is not None:
            self.login_window.destroy()
        try:
            self.main_window.destroy()
            self.usb_handler.cleanup()
        except Exception as e:
            print(f"Exception occurred while exiting application: {e}")


def run_application():  
    app = Application()
    app.run()


if __name__ == "__main__":
    run_application()
