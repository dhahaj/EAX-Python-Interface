from settings import Settings
from user import User
from constants import APPLICATION_THEME
import tkinter as tk
from tkinter import StringVar
from applogger import AppLogger
from rich import print


class Login(tk.Toplevel):
    """
    A class to create a login GUI. The GUI has two entry fields for username and password, and a login button.
    The login button calls the login() method, which checks if the username and password are correct.
    The is_logged_in() method returns True if the user is logged in, and False otherwise.
    """

    def __init__(self, parent, window, settings, callback=None):
        """
        Initialize the login GUI Window.
        """
        super().__init__(window) # Initialize the superclass

        self.parent = parent
        self.settings = settings
        self.window = window
        self.callback = callback
        print("[bold]Login window initialized[/bold]")

        self.users = User()  # Create a user object
        self.users.load()  # Load the users from the users.json file

        # self.root = tk.Tk()  # Create the root window
        self.title("Login")  # Set the title of the window
        # self.call("source", "azure.tcl")  # Set the theme of the window
        # self.call("set_theme", APPLICATION_THEME)  # Set the theme of the window
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.attributes("-topmost", 1)  # Make the window always on top
        self.iconbitmap("images/pcb.ico")  # Set the icon of the window
        self.geometry("300x150+300+250")  # Set the size of the window
        self.username_label = tk.Label(
            self, text="Username:"
        )  # Create a label for the username
        self.password_label = tk.Label(
            self, text="Password:"
        )  # Create a label for the password

        self.username = StringVar()
        self.username_entry = tk.Entry(  # Create an entry field for the username
            self, textvariable=self.username, takefocus=True, 
        )
        self.password_entry = tk.Entry(
            self, show="*",
        )  # Create an entry field for the password

        self.login_button = tk.Button(
            self, text="Login", command=self.login
        )  # Create a login button
        self.cancel_button = tk.Button(
            self, text="Cancel", command=self.close
        )  # Create a cancel button

        # Place the widgets in the window
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        self.login_button.grid(row=2, column=0, padx=10, pady=10)
        self.cancel_button.grid(row=2, column=1, padx=10, pady=10)

        # Create a label to display a message if the login fails
        self.failure_label = tk.Label(self, text="")
        self.failure_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.login_status = False
        self.user = None
        self.admin = None

        # Bind the Enter and Escape keys
        self.bind("<Return>", lambda event: self.login())
        self.bind("<Escape>", lambda event: self.close())

    def close(self):
        """
        Close the login GUI.
        """
        # if self.parent is not None:
            # self.parent.exit()
        self.parent.user_login(None)

    def login(self):
        """
        Check if the username and password are correct.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        # if username in self.users and self.users[username] == password:
        if self.users.validate_credentials(username, password):
            self.login_status = True
            self.user = username
            self.settings.set("last_user", self.username_entry.get())
            # AppLogger("logger").get_logger().info(f"User {self.user} logged in.")

            # if self.parent is None:
            #     self.parent = MainWindow(self, self.settings)
            self.parent.user_login(username)
        else:
            self.failure_label.config(text="Invalid username or password.", fg="red")
            self.login_status = False
            self.user = None

    def is_logged_in(self):
        """
        Return the login status.
        """
        return self.login_status

    def get_user(self):
        """
        Return the username.
        """
        return self.user

    def get_admin(self):
        """
        Return the admin status.
        """
        return self.admin

    def run(self):
        """
        Run the login GUI.
        """
        self.username.set(self.settings.get("last_user"))
        print(self.username.get())
        self.mainloop()

if __name__ == "__main__":
    settings = Settings()
    login_window = Login(None, None, settings)
    login_window.run()
    if login_window.is_logged_in():
        print("Logged in")
    else:
        print("Not logged in")