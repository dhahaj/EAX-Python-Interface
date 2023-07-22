from tkinter.constants import *
from constants import *
from login import Login
from eax500 import MainWindow
from settings import Settings
import usbhandler


class Application:
    """
    This is the main application class.
    """

    def __init__(self, main_window=None, login_window=None):
        # initialize the application
        self.state = ST_INIT
        self.settings = Settings()
        global Login, MainWindow
        # setup the USB handler
        self.usb_handler = usbhandler.USBHandler(
            port=self.settings.get(KEY_SERIAL_PORT),
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

        # setup the login window
        if not self.settings.get(KEY_SKIP_LOGIN):  # no login screen
            # self.main_window.window.withdraw()
            # setup the main window
            self.main_window.run()
        else:  # login screen
            self.main_window.toggle_state("withdrawn")
            # self.main_window.toggle_connect()
            self.login_window.run()
     
            # self.login_window.username_entry.insert(
            #     self.settings.get(KEY_LAST_USER), END
            # )

        # # see if we are skipping the login screen
        # if not self.settings.get(KEY_SKIP_LOGIN):
        #     self.main_window.window.withdraw()
        #     self.login_window.username_entry.insert(
        #         self.settings.get(KEY_LAST_USER), END
        #     )
        #     self.login_window.run()
        # else:
        #     self.main_window.run()
        #     self.login_window.root.withdraw()

        self.user = None
        self.state = ST_LOGGED_OUT

        if self.settings.get(KEY_LAST_USER):
            self.transition_to_main()

    def get_setting(self, key):
        # return a setting from the settings file
        return self.settings.get(key)

    def set_setting(self, key, value):
        # set a setting in the settings file
        self.settings.set(key, value)

    def transition_to_login(self):
        # handle transition to login state
        self.state = ST_LOGGING_IN

    def transition_to_main(self):
        # handle transition to main window state
        self.state = ST_LOGGED_IN
        self.main_window.run()

    def transition_to_logout(self):
        # handle transition to logout state
        self.state = ST_LOGGED_OUT

    def transition_to_exit(self):
        # handle transition to exit state
        self.state = ST_EXITING

    def get_state(self):
        # return the current state
        return self.state

    def user_login(self, username):
        # handle user login
        self.user = username
        self.login_window.root.withdraw()
        self.main_window.window.deiconify()
        self.settings.set(KEY_LAST_USER, self.login_window.username_entry.get())
        self.login_window.password_entry.delete(0, END)
        self.transition_to_main()

    def user_logout(self):
        # handle user logout
        self.user = None
        self.main_window.window.withdraw()
        self.login_window.root.deiconify()

    def connection_callback(self, connected, msg=None):
        # handle connection callback
        self.main_window.device_connected_callback(connected, msg)

    def run(self):
        # main application loop
        self.main_window.window.mainloop()

    def exit(self):
        # exit the application
        self.login_window.root.destroy()
        self.main_window.window.destroy()
        self.usb_handler.cleanup()


app = None
login_window = None
main_window = None

def run_application():
    '''
    Run the application.
    '''
    global app
    global login_window
    global main_window

    app = Application(login_window=login_window, main_window=main_window)
    app.run()


def exit_handler():
    # handle application exit
    if app is not None:
        app.exit()


if __name__ == "__main__":
    run_application()
