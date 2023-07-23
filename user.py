from constants import *
import json
import os
import bcrypt

class User:
    """
    This class is used to handle the user data.
    """
    def __init__(self, filename="users.json"):
        """
        Initialize the User class.

        :param filename: The name of the file to store the user data.
        """
        # Default users
        self.users = DEFAULT_USERS
        self.filename = filename
        self.users = self.load(self.filename)

    def load(self, filename=None):
        """
        Load the users from a JSON file.

        :param filename: The filename to load the users from.
        """
        if filename is None:
            filename = self.filename
        
        # Check if the file exists
        if os.path.exists(filename):
            # Load settings from file
            with open(filename, "r") as file:
                try:
                    data = json.load(file)
                    if isinstance(data, list):
                        self.users = data
                    else:
                        print("Invalid format in user file. Expected a list.")
                        self.users = []
                except json.JSONDecodeError:
                    print("Failed to decode JSON from user file.")
                    self.users = []
        else: # File does not exist
            print(f"User file {filename} does not exist.")
            self.users = []
        if self.users is None:
            print("No users loaded. self.users is None.")
        elif isinstance(self.users, list):
            print(f"{len(self.users)} users loaded.")
        else:
            print("Unexpected error in load_users(). self.users is not a list.")
        
    def save_users(self):
        """ Save the users to a JSON file. """
        with open(self.filename, 'w') as file:
            json.dump(self.users, file, indent=4)

    def validate_credentials(self, username, password_attempt):
        """
        Validate the user credentials.

        :param username: The username to validate.
        :param password: The password hash to validate.
        :return: True if the credentials are valid, False otherwise.
        """
        self.load()
        for user in self.users:
            if user['username'] == username:
                password_attempt = password_attempt.encode('utf-8')
                password_hash = user['password'].encode('utf-8')
                return bcrypt.checkpw(password_attempt, password_hash)
        return False

    @staticmethod
    def add_user(username, password, admin=False, filename=None):
        """
        Add a user to the user list.
        
        :param username: The username to add.
        :param password: The password to add.
        :param admin: True if the user is an admin, False otherwise.
        :return: True if the user was added, False otherwise.
        """
        if filename is None:
            filename = "users.json"
        
        users = User.load_users(filename)

        # Check if the user already exists
        for user in users:
            if user['username'] == username:
                print(f"User {username} already exists.")
                return

        # Hash the password        
        password = password.encode('utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt())
        password = password.decode('utf-8')

        # Add the user to the list and save the list
        users.append({'username': username, 'password': password, 'admin': admin})
        
        """ Save the users to a JSON file. """
        with open(filename, 'w') as file:
            json.dump(users, file, indent=4)

    @staticmethod
    def load_users(filename=None):

        if filename is None:
            filename = "users.json"
        users = None
        # Check if the file exists
        if os.path.exists(filename):
            # Load settings from file
            with open(filename, "r") as file:
                try:
                    data = json.load(file)
                    if isinstance(data, list):
                        users = data
                    else:
                        print("Invalid format in user file. Expected a list.")
                        users = []
                except json.JSONDecodeError:
                    print("Failed to decode JSON from user file.")
                    users = []
        else:
            print(f"User file {filename} does not exist.")
            users = []
        if users is None:
            print("No users loaded. self.users is None.")
        elif isinstance(users, list):
            print(f"{len(users)} users loaded.")
        else:
            print("Unexpected error in load_users(). self.users is not a list.")
        
        return users

    def remove_user(self, username):
        """
        Remove a user from the user list.
        
        :param username: The username to remove.
        :return: True if the user was removed, False otherwise.
        """
        if username in self.users:
            del self.users[username]
            self.save_users()
        else:
            print(f"User {username} does not exist.")

    def is_admin(self, username):
        """
        Check if a user is an admin.

        :param username: The username to check.
        :return: True if the user is an admin, False otherwise.
        """
        return self.users[username]['admin']
        
    def get_user(self, username):
        """
        Get a single user.

        :param username: The username to get.
        :return: The user if it exists, None otherwise.
        """
        for user in self.users:
            if user['username'] == username:
                return user
        return None


class SingleUser:
    """
    This class defines a single user.
    """
    def __init__(self, username, password, admin=False):
        """
        Initialize the User class.

        :param username: The username of the user.
        :param password: The password of the user.
        :param admin: True if the user is an admin, False otherwise.
        """
        self.username = username
        self.password = password
        self.admin = admin

    def __str__(self):
        return f"User: {self.username}, Admin: {self.admin}"
    
    def is_admin(self):
        """
        Check if the user is an admin.

        :return: True if the user is an admin, False otherwise.
        """
        return self.admin
    
    def check_password(self, password):
        """
        Check if the password matches the user's password.

        :param password: The hashed password to check.
        :return: True if the password matches, False otherwise.
        """
        password_attempt = password_attempt.encode('utf-8')
        password_hash = self.user['password'].encode('utf-8')
        return bcrypt.checkpw(password_attempt, password_hash)