import sqlite3
import bcrypt


class UserDatabase:
    """
    A class to represent a user database. This class is used to create, read, update and delete users. It also
    provides methods to check if a user is an admin and to check if a password is correct. The database is stored in
    a SQLite database file.

    Attributes
    ----------
    conn : sqlite3.Connection
        The connection to the SQLite database.
    database_file : str
        The path to the SQLite database file.

    Methods
    -------
    to_dict()
        Returns a list of dictionaries containing all users in the database.
    __str__()
        Returns a string representation of the UserDatabase object.
    remove_user(username)
        Removes a user from the database.
    is_admin(username)
        Checks if a user is an admin.
    to_json()
        Returns a list of dictionaries containing all users in the database.
    get_user(username)
        Returns a dictionary containing the user with the given username.
    get_users()
        Returns a list of all usernames in the database.
    create_users_table()
        Creates the users table in the database.
    insert_user(username, password, is_admin)
        Inserts a user into the database.
    check_password(username, password_to_check)
        Checks if a password is correct for a given user.
    purge()
        Removes the users table from the database.
    close()
        Closes the connection to the database.
    """
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_users_table()

        self.database_file = db_name

    def to_dict(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        users = []
        for row in rows:
            users.append(
                {
                    "id": row[0],
                    "username": row[1],
                    "password": row[2],  # Do NOT display this in a real application!
                    "is_admin": row[3],
                }
            )
        return users

    def __str__(self):
        return f"UserDatabase: {self.database_file}"

    def remove_user(self, username):
        c = self.conn.cursor()
        c.execute("DELETE FROM users WHERE username=?", (username,))
        self.conn.commit()

    def is_admin(self, username):
        c = self.conn.cursor()
        c.execute("SELECT is_admin FROM users WHERE username=?", (username,))
        row = c.fetchone()
        if row is None:
            print("No such user")
            return None
        else:
            return row[0]

    def to_json(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        users = []
        for row in rows:
            users.append(
                {
                    "id": row[0],
                    "username": row[1],
                    "password": row[2],  # Do NOT display this in a real application!
                    "is_admin": row[3],
                }
            )
        return users

    def get_user(self, username):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        row = c.fetchone()
        if row is None:
            print("No such user")
            return None
        else:
            user = {
                "id": row[0],
                "username": row[1],
                "password": row[2],  # Do NOT display this in a real application!
                "is_admin": row[3],
            }
            return user

    def get_users(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        users = []
        for row in rows:
            users.append(row[1])
        return users

    def create_users_table(self):
        try:
            c = self.conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            is_admin BOOLEAN NOT NULL
                        );""")
        except Exception as e:
            print(e)

    def insert_user(self, username, password, is_admin):
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        try:
            c = self.conn.cursor()
            c.execute(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                (username, hashed, is_admin),
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Username {username} is already taken.")

    def check_password(self, username, password_to_check):
        c = self.conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        row = c.fetchone()
        if row is None:
            print("No such user")
        else:
            hashed = row[0]
            if bcrypt.checkpw(password_to_check.encode("utf-8"), hashed):
                return True
        return False

    def purge(self):
        c = self.conn.cursor()
        c.execute("DROP TABLE users")
        self.conn.commit()

    def close(self):
        print("Closing database connection...")
        self.conn.close()
