from loguru import logger as log
import atexit
import sqlite3
import bcrypt
import os
import datetime
import shutil
from typing import List
from threading import Lock


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
    db_name = 'users.db'
    lock = Lock()

    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_users_table()

        atexit.register(self.close)

    @property
    def admin(self) -> bool:
        return self.is_admin('admin')

    @property
    def users(self) -> List[str]:
        return self.get_users()

    @property
    def database_file(self) -> str:
        return self.db_name

    def load_from_database(self) -> list:
        '''Returns a list of dictionaries containing all users in the database.'''
        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()
        users = []
        [users.append({
            'id': row[0],
            'username': row[1],
            'password': row[2],
            'is_admin': row[3],
        }) for row in rows]

        return users

    def __str__(self) -> str:
        return f'UserDatabase: {self.db_name}'

    def remove_user(self, username: str) -> None:
        with self.lock:
            self.cursor.execute(
                'DELETE FROM users WHERE username=?', (username,))
            self.conn.commit()

    def is_admin(self, username: str) -> bool:
        self.cursor.execute(
            'SELECT is_admin FROM users WHERE username=?', (username,))
        val = self.cursor.fetchone()
        return False if not val else bool(val[0])

    def get_user(self, username: str) -> dict:
        """ Returns a dictionary containing the user with the given username. """
        self.cursor.execute(
            'SELECT * FROM users WHERE username=?', (username,))
        row = self.cursor.fetchone()
        return None if not row else {
            'id': row[0],
            'username': row[1],
            'password': row[2],
            'is_admin': row[3],
        }

    def get_users(self) -> List[str]:
        """ Returns a list of all usernames in the database. """
        return [user['username'] for user in self.load_from_database()]

    def create_users_table(self) -> None:
        with self.lock:
            try:
                self.cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL,
                                is_admin BOOLEAN NOT NULL
                            );'''
                )
            except Exception as exception:
                log.exception(exception)

    def insert_user(self, username: str, password: str, is_admin: bool) -> bool:
        if username.strip() == '' or password == '':
            return False
        with self.lock:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            try:
                c = self.conn.cursor()
                c.execute(
                    'INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)',
                    (username, hashed, is_admin),
                )
                self.conn.commit()
                return True
            except sqlite3.IntegrityError:
                print(f'Username {username} is already taken.')
                return False

    def check_password(self, username: str, password_to_check: str) -> bool:
        self.cursor.execute(
            'SELECT password FROM users WHERE username=?', (username,))
        row = self.cursor.fetchone()
        return False if not row else True if bcrypt.checkpw(password_to_check.encode('utf-8'), row[0]) else False

    def purge(self) -> None:
        with self.lock:
            self.cursor.execute('DROP TABLE users')
            self.conn.commit()

    def backup_database(self) -> None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_filename = f"{self.db_name.replace('.db', '')}_{timestamp}.db"
        # Connect to the backup database
        backup_conn = sqlite3.connect(backup_filename)

        # Use the SQLite backup API to backup an active database
        with backup_conn:
            self.conn.backup(backup_conn)
        backup_conn.close()

        self.create_dir('backups')
        self.create_dir('backups/users')

        os.system(f'attrib +h {backup_filename}')
        shutil.move(backup_filename, f'backups/users/{backup_filename}')
        log.info(f'User database backed up to {backup_filename}')

    def create_dir(self, path: str) -> None:
        """ Creates a directory if it doesn't exist. """
        if not os.path.exists(path):
            os.mkdir(path)
            os.system(f'attrib +h {path}')

    def check_integrity(self) -> bool:
        """ Checks the integrity of the database. """
        self.cursor.execute("PRAGMA integrity_check")
        result = self.cursor.fetchone()
        log.info(result)
        return result[0] == 'ok'

    def close(self) -> None:
        self.conn.close()
        self.lock.release()
        log.info('Database connection closed...')
