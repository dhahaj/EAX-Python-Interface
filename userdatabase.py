import sqlite3
import bcrypt


class UserDatabase:
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
