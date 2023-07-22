import tkinter as tk
from tkinter import simpledialog
from user import SingleUser


class UserCreationDialog(simpledialog.Dialog):
    """
    This class is used to create a dialog for the user to create a new user.
    """
    def __init__(self, parent, user_settings=None, dialog_title=None):
        """ Initialize the UserCreationDialog class. """
        self.user_data = None  # Initialize user_data attribute
        super().__init__(parent, title=dialog_title)

    def apply(self):
        """ Apply the user data. """
        username = self.e1.get()
        password = self.e2.get()
        is_admin = bool(self.admin_var.get())
        user = SingleUser(username, password, is_admin)
        self.user_data = user  # Store the user data

    def body(self, master):
        """ Create the body of the dialog. """
        self.title("User Creation")
        tk.Label(master, text="Username:").grid(row=0)
        tk.Label(master, text="Password:").grid(row=1)
        tk.Label(master, text="Admin:").grid(row=2)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master, show="*")
        self.admin_var = tk.IntVar()
        self.e3 = tk.Checkbutton(master, variable=self.admin_var)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        return self.e1  # initial focus

    def run(self):
        self.mainloop()
        return self.user
