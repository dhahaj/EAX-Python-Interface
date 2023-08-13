import atexit
import os
import shutil
import logging
from turtle import st
import zipfile
from datetime import datetime
import time
from rich import print
import re
import sqlite3
import os
from logging import _levelToName, _nameToLevel 


class AppLogger:
    """
    Logger class

    This class is used to handle the logging system. It creates a logger object
    and adds a file handler and a console handler to it. The file handler is
    used to log all messages to a file and the console handler is used to log
    only error messages to the console.

    The logger object can be retrieved using the get_logger() method. The
    shutdown() method should be called when the program is exiting to close
    the logger object.

    The get_logs() method can be used to get the contents of the log file.
    """
    database = 'logs.db'

    def __init__(self, name, file_name="debug.log"):
        """
        Initialize the AppLogger class.

        :param name: The name of the logger.
        :param file_name: The name of the log file.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.file_name = file_name

        self.check_and_move_old_log_file()

        # Create file handler
        file_handler = logging.FileHandler(file_name, mode="a")
        file_handler.setLevel(logging.DEBUG)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)

        # Create formatters and add it to handlers
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_formatter = logging.Formatter(
            "%(name)s - %(levelname)s - %(message)s")

        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        # atexit.register(self._shutdown)
        # self.connection = None

    @staticmethod
    def get_logger() -> logging.Logger:
        """
        Return the logger object.

        :return: The logger object.
        """
        return logging.getLogger("logger")

    @staticmethod
    def info(message):
        """
        Log an info message.

        :param level: The level of the message.
        :param message: The message to log.
        """
        logging.getLogger("logger").info(f"{message}")

    @staticmethod
    def get_logs(file_name="debug.log") -> str:
        """
        Get the log file contents.

        :return: The log file contents.
        """
        with open(file_name, "r") as file:
            return file.read()

    @staticmethod
    def get_table(file_name="debug.log") -> list:
        logs = AppLogger.get_logs(file_name)
        logs = logs.strip()
        log_list = logs.split("\n")
        for log in logs:
            log_list.append(list(Log.parse(log)))
        return log_list

    @staticmethod
    def shutdown():
        """Shutdown the logging system."""
        logging.shutdown()

    def _shutdown(self):
        """Shutdown the logging system."""
        logging.shutdown()
        self.connection.close()

    def check_and_move_old_log_file(self) -> None:
        """
        Check if the log file exists and if it does, check the date of the file.
        If the date of the file is not today, move the file to a new file with the date appended to the file name.
        """
        if os.path.exists(self.file_name):
            # Get the date of the log file
            print(f"file name: {self.file_name}")

            file_date = datetime.fromtimestamp(
                os.path.getctime(self.file_name))
            print(f"file creation date: {file_date}")

            today = datetime.now()
            print(f"todays date: {today}")

            # If the date of the log file is older than today, move it to the
            # logs folder and append the date to the file name.
            if file_date.date() != today.date():
                print("moving file")
                # Create the logs folder if it doesn't exist
                if not os.path.exists("logs"):
                    print("creating logs folder")
                    os.makedirs("logs")
                # Create the new file name
                new_file_name = f"logs/{self.file_name.split('.')[0]}_{file_date.strftime('%Y-%m-%d')}.log"
                print(f"new file name: {new_file_name}")
                # Move the file
                try:
                    shutil.move(
                        self.file_name, new_file_name
                    )  # use shutil.move instead of shutil.copy
                except Exception as e:
                    print(e)
                # os.remove(self.file_name)
                open(self.file_name, "a").close()  # create a new empty file
        else:  # File does not exist
            print("file does not exist")
            open(self.file_name, "a").close()

    @staticmethod
    def archive_logs(archive_name="logs") -> None:
        """
        Archive all log files into a zip archive

        archive_name: The name of the zip archive (without extension, defaults to 'logs')
        """
        shutil.make_archive(archive_name, "zip", "logs")

    @staticmethod
    def add_to_archive(archive_name, file_name) -> None:
        """
        Add a file to an existing zip archive

        archive_name: The name of the zip archive (without path or extension)
        file_name: The name of the file to add
        """
        with zipfile.ZipFile(archive_name, "a") as myzip:
            myzip.write(file_name)

    def log(self, level, message):
        """
        Log a message.

        :param level: The level of the message.
        :param message: The message to log.
        """
        log_level = _nameToLevel[level]
        self.logger.log(log_level, message)
        # entry = self.create_entry(level, message)
        # print(f"entry: {entry}")
        # self.store_log_entry_to_db(entry)

    def create_entry(self, level, message):
        """
        Create a log entry.

        :param level: The level of the message.
        :param message: The message to log.
        """
        return "%(asctime)s - %(name)s - %(levelname)s - %(message)s" % {
            "asctime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": "logger",
            "levelname": level,
            "message": message
        }

    def create_database_and_table(self) -> None:
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                logger_name TEXT,
                log_level TEXT,
                message TEXT
            )''')

    def store_log_entry_to_db(self, entry):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()

            # Splitting the entry using regex
            pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (?P<logger>\w+) - (?P<level>[A-Z]+) - (?P<message>.+)'
            match = re.match(pattern, entry)
            print(f"pattern {pattern}, match: {match}")
            # if match:
            # data = match.groupdict()
            # print(f"data: {data}")
            cursor.execute('''
                INSERT INTO logs (timestamp, logger_name, log_level, message)
                VALUES (?, ?, ?, ?)
                ''', 
                (data['timestamp'], data['logger'], data['level'], data['message'])
            )

# SQLite Database Management
class LogManager:

    def __init__(self, db_name="logs.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)  # Connect to the SQLite database
        self.cursor = self.conn.cursor()
        self.create_table()
        atexit.register(self.close)

    def log(self, level, message):
        entry=self.create_entry(level, message)
        print(f"entry: {entry}")
        parse_and_insert_log(self, entry)
        # self.insert_log(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "logger", level, message)

    def create_table(self):
        """Create a new table for logs if it doesn't exist yet."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                timestamp TEXT NOT NULL,
                logger TEXT NOT NULL,
                level TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def insert_log(self, timestamp, logger, level, message):
        """Insert a log entry into the database."""
        print(f"inserting log: {timestamp}, {logger}, {level}, {message}")
        self.cursor.execute("INSERT INTO logs (timestamp, logger, level, message) VALUES (?, ?, ?, ?)",
                            (timestamp, logger, level, message))
        self.conn.commit()

    def create_entry(self, level, message) -> str:
        """
        Create a log entry.

        :param level: The level of the message.
        :param message: The message to log.
        """
        return "%(asctime)s - %(name)s - %(levelname)s - %(message)s" % {
            "asctime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": "logger",
            "levelname": level,
            "message": message
        }

    def get_all_logs(self) -> list:
        self.cursor.execute("SELECT * FROM logs")
        logs = []
        for row in self.cursor.fetchall():
            log_entry = {
                # "id": row[0],
                "timestamp": row[1],
                # "logger": row[2],
                "level": row[3],
                "message": row[4]
            }
            logs.append(log_entry)
        return list(logs)

    def count_programming_errors(self) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM logs WHERE level='ERROR' AND message LIKE '%program%'")
        count = self.cursor.fetchone()[0]
        return count
    
    def count_programming_successes(self) -> int:
        self.cursor.execute("""
        SELECT COUNT(*) 
        FROM logs 
        WHERE level='INFO' 
        AND message LIKE '%Programming%'
        """)
        count = self.cursor.fetchone()[0]
        return count

    def close(self):
        """Close the database connection."""
        print("Closing database connection.")
        self.conn.close()

# Regular Expression for Log Parsing
pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<logger>[\w\.]+) - (?P<level>[A-Z]+) - (?P<message>.+)'

def parse_and_insert_log(log_manager, log_entry):
    """Parse a log entry and insert it into the database."""
    match = re.match(pattern, log_entry)
    if match:
        data = match.groupdict()
        log_manager.insert_log(data['timestamp'], data['logger'], data['level'], data['message'])
        print(f"Inserted log: {data}")
    else:
        print("Log format didn't match. Entry skipped.")

class Log:
    """
    Log class

    This class is used to represent a log entry. It has a date, level and
    message attribute. It can be initialized with a string or with the
    individual attributes.
    """

    def __init__(self, value=None, date=None, level=None, message=None):
        if value is not None:
            value = value.split(" - ")
            value = [v.strip() for v in value]
            self.date = value[0]
            self.level = value[2]
            self.message = value[3]
        else:
            self.date = date
            self.level = level
            self.message = message

    @staticmethod
    def parse(value):
        value = value.split(" - ")
        value = [v.strip() for v in value]
        return (value[0], value[2], value[3])

    def __str__(self):
        return f"{self.date} {self.level} {self.message}"


# if __name__ == "__main__":
#     logger = AppLogger("logger")
#     logger.info("test")

#     print(AppLogger.get_logs())
