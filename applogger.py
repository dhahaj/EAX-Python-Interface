from loguru import logger
import sqlite3
from datetime import datetime

class AppLogger:
    def __init__(self, logfile="logs/app_{time:YYYY-MM-DD}.log", database="logs.db"):
        # Configure loguru to log to files with rotation
        logger.add(logfile, rotation="00:00", retention="7 days", level="DEBUG", format="{time} | {level} | {message}")

        self.database = database
        self.create_log_table()

    def create_log_table(self):
        """Creates a table for logs in the SQLite database if it doesn't exist."""
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                level TEXT,
                message TEXT
            )''')
            conn.commit()

    def log_to_db(self, level: str, message: str):
        """Log messages explicitly to the SQLite database."""
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)', (timestamp, level, message))
            conn.commit()

    def log(self, level: str, message: str):
        """Log a message with the specified level."""
        logger.log(level, message)
        self.log_to_db(level, message)

    def info(self, message: str):
        logger.info(message)
        self.log_to_db("INFO", message)

    def error(self, message: str):
        logger.error(message)
        self.log_to_db("ERROR", message)

    def debug(self, message: str):
        logger.debug(message)
        self.log_to_db("DEBUG", message)

    def critical(self, message: str):
        logger.critical(message)
        self.log_to_db("CRITICAL", message)

    def success(self, message: str):
        logger.success(message)
        self.log_to_db("SUCCESS", message)

    def warning(self, message: str):
        logger.warning(message)
        self.log_to_db("WARNING", message)

    def exception(self, message: str):
        logger.exception(message)
        self.log_to_db("EXCEPTION", message)

    def get_logs(self) -> list:
        """Fetch logs from the database for the LogView class."""
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs")
            return cursor.fetchall()


# import atexit
# import os
# import shutil
# import logging
# import zipfile
# from datetime import datetime
# from rich import print
# import re
# import sqlite3
# import os
# from logging import _nameToLevel
# from loguru import logger as log
# from threading import Lock
# import json
# from typing import List

# class AppLogger:
#     """
#     Logger class

#     This class is used to handle the logging system. It creates a logger object
#     and adds a file handler and a console handler to it. The file handler is
#     used to log all messages to a file and the console handler is used to log
#     only error messages to the console.

#     The logger object can be retrieved using the get_logger() method. The
#     shutdown() method should be called when the program is exiting to close
#     the logger object.

#     The get_logs() method can be used to get the contents of the log file.
#     """
#     database = 'logs.db'

#     def __init__(self, name: str, file_name="debug.log"):
#         """
#         Initialize the AppLogger class.

#         :param name: The name of the logger.
#         :param file_name: The name of the log file.
#         """
#         self.logger = logging.getLogger(name)
#         self.logger.setLevel(logging.DEBUG)
#         self.file_name = file_name

#         self.check_and_move_old_log_file()

#         # Create file handler
#         file_handler = logging.FileHandler(file_name, mode="a")
#         file_handler.setLevel(logging.DEBUG)

#         # Create console handler
#         console_handler = logging.StreamHandler()
#         console_handler.setLevel(logging.ERROR)

#         # Create formatters and add it to handlers
#         file_formatter = logging.Formatter(
#             "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#         )
#         console_formatter = logging.Formatter(
#             "%(name)s - %(levelname)s - %(message)s")

#         file_handler.setFormatter(file_formatter)
#         console_handler.setFormatter(console_formatter)

#         # Add the handlers to the logger
#         self.logger.addHandler(file_handler)
#         self.logger.addHandler(console_handler)
#         # atexit.register(self._shutdown)
#         # self.connection = None

#     @staticmethod
#     def get_logger() -> logging.Logger:
#         """
#         Return the logger object.

#         :return: The logger object.
#         """
#         return logging.getLogger("logger")

#     @staticmethod
#     def info(message: str) -> None:
#         """
#         Log an info message.

#         :param level: The level of the message.
#         :param message: The message to log.
#         """
#         logging.getLogger("logger").info(f"{message}")

#     @staticmethod
#     def get_logs(file_name="debug.log") -> str:
#         """
#         Get the log file contents.

#         :return: The log file contents.
#         """
#         with open(file_name, "r") as file:
#             return file.read()

#     @staticmethod
#     def get_table(file_name="debug.log") -> list:
#         logs = AppLogger.get_logs(file_name)
#         logs = logs.strip()
#         log_list = logs.split("\n")
#         for log in logs:
#             log_list.append(list(Log.parse(log)))
#         return log_list

#     @staticmethod
#     def shutdown() -> None:
#         """Shutdown the logging system."""
#         logging.shutdown()

#     def _shutdown(self):
#         """Shutdown the logging system."""
#         logging.shutdown()
#         self.connection.close()

#     def check_and_move_old_log_file(self) -> None:
#         """
#         Check if the log file exists and if it does, check the date of the file.
#         If the date of the file is not today, move the file to a new file with the date appended to the file name.
#         """
#         if os.path.exists(self.file_name):
#             # Get the date of the log file
#             print(f"file name: {self.file_name}")

#             file_date = datetime.fromtimestamp(
#                 os.path.getctime(self.file_name))
#             print(f"file creation date: {file_date}")

#             today = datetime.now()
#             print(f"todays date: {today}")

#             # If the date of the log file is older than today, move it to the
#             # logs folder and append the date to the file name.
#             if file_date.date() != today.date():
#                 print("moving file")
#                 # Create the logs folder if it doesn't exist
#                 if not os.path.exists("logs"):
#                     print("creating logs folder")
#                     os.makedirs("logs")
#                 # Create the new file name
#                 new_file_name = f"logs/{self.file_name.split('.')[0]}_{file_date.strftime('%Y-%m-%d')}.log"
#                 print(f"new file name: {new_file_name}")
#                 # Move the file
#                 try:
#                     shutil.move(
#                         self.file_name, new_file_name
#                     )  # use shutil.move instead of shutil.copy
#                 except Exception as e:
#                     print(e)
#                 # os.remove(self.file_name)
#                 open(self.file_name, "a").close()  # create a new empty file
#         else:  # File does not exist
#             print("file does not exist")
#             open(self.file_name, "a").close()

#     @staticmethod
#     def archive_logs(archive_name="logs") -> None:
#         """
#         Archive all log files into a zip archive

#         archive_name: The name of the zip archive (without extension, defaults to 'logs')
#         """
#         shutil.make_archive(archive_name, "zip", "logs")

#     @staticmethod
#     def add_to_archive(archive_name: str, file_name: str) -> None:
#         """
#         Add a file to an existing zip archive

#         archive_name: The name of the zip archive (without path or extension)
#         file_name: The name of the file to add
#         """
#         with zipfile.ZipFile(archive_name, "a") as myzip:
#             myzip.write(file_name)

#     def log(self, level: str, message: str) -> None:
#         """
#         Log a message.

#         :param level: The level of the message.
#         :param message: The message to log.
#         """
#         log_level = _nameToLevel[level]
#         self.logger.log(log_level, message)
#         # entry = self.create_entry(level, message)
#         # print(f"entry: {entry}")
#         # self.store_log_entry_to_db(entry)

#     def create_entry(self, level: str, message: str) -> str:
#         """
#         Create a log entry.

#         :param level: The level of the message.
#         :param message: The message to log.
#         """
#         return "%(asctime)s - %(name)s - %(levelname)s - %(message)s" % {
#             "asctime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "name": "logger",
#             "levelname": level,
#             "message": message
#         }

#     def create_database_and_table(self) -> None:
#         with sqlite3.connect(self.database) as connection:
#             cursor = connection.cursor()
#             cursor.execute('''
#             CREATE TABLE IF NOT EXISTS logs (
#                 id INTEGER PRIMARY KEY,
#                 timestamp TEXT,
#                 logger_name TEXT,
#                 log_level TEXT,
#                 message TEXT
#             )''')

#     def store_log_entry_to_db(self, entry: str) -> None:
#         with sqlite3.connect(self.database) as connection:
#             cursor = connection.cursor()

#             # Splitting the entry using regex
#             pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (?P<logger>\w+) - (?P<level>[A-Z]+) - (?P<message>.+)'
#             match = re.match(pattern, entry)
#             print(f"pattern {pattern}, match: {match}")
#             if match:
#                 data = match.groupdict()
#                 # print(f"data: {data}")
#                 cursor.execute('INSERT INTO logs (timestamp, logger_name, log_level, message) VALUES (?, ?, ?, ?)',
#                                (data['timestamp'], data['logger'], data['level'], data['message']))

# # SQLite Database Management
# import enum
# class Names(enum.Enum):
#     Settings    : int = 0
#     Firmware    : int = 1
#     Pins        : int = 2
#     Users       : int = 3
#     Instructions: int = 4

#     def __str__(self) -> str:
#         return self.name
    
#     def __repr__(self) -> str:
#         return str(self.value)
    
#     def __int__(self) -> int:
#         return self.value
    
    

# class LogManager:
#     """
#     LogManager class

#     This class is used to manage the SQLite database. It can be used to insert
#     log entries into the database, update existing log entries, clear all logs
#     from the database, get logs from the database and exporting logs to a file.
#     """
#     lock = Lock()
#     default_db_name = "sqlite.db"

#     def __init__(self, db_name: str="logs.db"):
#         # Connect to the SQLite database
#         self.conn = sqlite3.connect(db_name, check_same_thread=False)
#         self.cursor = self.conn.cursor()
#         self.create_table()
#         atexit.register(self.close)
#         self.db_name = db_name
#         log.debug("LogManager initialized.")

#     def log(self, level: str, message: str) -> None:
#         """Log a message."""
#         entry = self.create_entry(level, message)
#         parse_and_insert_log(self, entry)

#     def success(self, message: str) -> None:
#         """Log a success message."""
#         self.log("SUCCESS", message)

#     def info(self, message: str) -> None:
#         """Log an info message."""
#         self.log("INFO", message)

#     def warning(self, message: str) -> None:
#         """Log a warning message."""
#         self.log("WARNING", message)

#     def error(self, message: str) -> None:
#         """Log an error message."""
#         self.log("ERROR", message)

#     def critical(self, message: str) -> None:
#         """Log a critical message."""
#         self.log("CRITICAL", message)

#     def save_logs(self, log_data: list) -> None:
#         """Save a list of logs to the database after clearing the current logs."""
#         self.backup_database()
#         self.clear_all_logs()
#         for entry in log_data:
#             log_entry = f"{ entry['timestamp']} - logger - {entry['level']} - {entry['message']}"
#             log.info(log_entry)
#             self.insert_log(
#                 entry['timestamp'],
#                 "logger",
#                 entry['level'],
#                 entry['message']
#             )

#     def clear_all_logs(self) -> None:
#         """Remove all log entries from the database."""
#         with self.lock:
#             self.cursor.execute("DELETE FROM logs")
#             self.conn.commit()
#             log.debug("All logs cleared from database.")

#     def update_log(self, log_id: str, timestamp=None, logger=None, level=None, message=None) -> None:
#         """Update a log entry based on its id."""
#         columns_to_update = []
#         values_to_update = []

#         if timestamp:
#             columns_to_update.append("timestamp = ?")
#             values_to_update.append(timestamp)

#         if logger:
#             columns_to_update.append("logger = ?")
#             values_to_update.append(logger)

#         if level:
#             columns_to_update.append("level = ?")
#             values_to_update.append(level)

#         if message:
#             columns_to_update.append("message = ?")
#             values_to_update.append(message)

#         with self.lock:
#             if columns_to_update:
#                 # Add id at the end to use in the WHERE clause
#                 values_to_update.append(log_id)
#                 sql_update = f"UPDATE logs SET {', '.join(columns_to_update)} WHERE id = ?"
#                 self.cursor.execute(sql_update, values_to_update)
#                 self.conn.commit()
#                 log.debug(f"Updated log with ID: {log_id}")
#             else:
#                 log.debug(f"No changes provided for log with ID: {log_id}")

#     def create_table(self) -> None:
#         with self.lock:
#             """Create a new table for logs if it doesn't exist yet."""
#             self.cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS logs (
#                     id INTEGER PRIMARY KEY,
#                     timestamp TEXT NOT NULL,
#                     logger TEXT NOT NULL,
#                     level TEXT NOT NULL,
#                     message TEXT NOT NULL
#                 )
#             """)
#             self.conn.commit()

#     def insert_log(self, timestamp: str, logger: str, level: str, message: str) -> None:
#         """Insert a log entry into the database."""
#         with self.lock:
#             self.cursor.execute("INSERT INTO logs (timestamp, logger, level, message) VALUES (?, ?, ?, ?)",
#                                 (timestamp, logger, level, message))
#             self.conn.commit()

#     def create_entry(self, level: str, message: str) -> str:
#         """
#         Create a log entry.

#         :param level: The level of the message.
#         :param message: The message to log.
#         """
#         return "%(asctime)s - %(name)s - %(levelname)s - %(message)s" % {
#             "asctime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "name": "logger",
#             "levelname": level,
#             "message": message
#         }

#     def get_all_logs(self) -> list:
#         """Get all logs from the database."""
#         self.cursor.execute("SELECT * FROM logs")
#         logs = []
#         for row in self.cursor.fetchall():
#             log_entry = {
#                 "id": row[0],
#                 "timestamp": row[1],
#                 "logger": row[2],
#                 "level": row[3],
#                 "message": row[4]
#             }
#             logs.append(log_entry)
#         return list(logs)

#     def count_programming_errors(self) -> int:
#         """Count the number of programming errors."""
#         self.cursor.execute(
#             "SELECT COUNT(*) FROM logs WHERE level='ERROR' AND message LIKE '%program%'")
#         count = self.cursor.fetchone()[0]
#         return count

#     def count_programming_successes(self) -> int:
#         """Count the number of programming successes."""
#         self.cursor.execute(
#             """SELECT COUNT(*) 
#                FROM logs 
#                WHERE level='SUCCESS' 
#                AND message LIKE '%Programming%'"""
#         )
#         count = self.cursor.fetchone()[0]
#         return count

#     def count_devices_tested(self) -> int:
#         """Count the number of tests passed."""
#         self.cursor.execute(
#             "SELECT COUNT(*) FROM logs WHERE level='INFO' AND message LIKE '%Testing%'")
#         count = self.cursor.fetchone()[0]
#         return count

#     def import_logs(self, file_name: str) -> None:
#         """Import logs from a text file."""
#         with self.lock:
#             with open(file_name, "r") as file:
#                 for line in file:
#                     parse_and_insert_log(self, line)
#             log.debug(f"Logs imported from {file_name}")

#     def export_logs(self, file_name="debug.log") -> None:
#         """Export all logs to a text file."""
#         with open(file_name, "w") as file:
#             for this_log in self.get_all_logs():
#                 file.write(
#                     f"{this_log['timestamp']} - {this_log['logger']} - {this_log['level']} - {this_log['message']}\n")
#         log.debug(f"Logs exported to {file_name}")

#     def backup_database(self) -> None:
#         with self.lock:
#             # Append a timestamp as a unique identifier to the backup name
#             timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#             backup_filename = f"{self.db_name.replace('.db','')}_{timestamp}.db"

#             # Connect to the backup database
#             backup_conn = sqlite3.connect(backup_filename)

#             # Use the SQLite backup API to backup an active database
#             with backup_conn:
#                 self.conn.backup(backup_conn)
#             backup_conn.close()

#             self.create_dir('backups')
#             self.create_dir('backups/logs')

#             os.system(f'attrib +h {backup_filename}')
#             shutil.move(backup_filename, f'backups/logs/{backup_filename}')
#             log.info(f'Database backed up to {backup_filename}')

#     def create_dir(self, path: str) -> None:
#         if os.path.exists(path) == False:
#             os.mkdir(path)
#             os.system(f'attrib +h {path}')

#     def check_integrity(self) -> bool:
#         self.cursor.execute("PRAGMA integrity_check")
#         result = self.cursor.fetchone()
#         log.info(result)
#         return result[0] == 'ok'

#     def close(self) -> None:
#         """Close the database connection."""
#         log.info("Closing database connection.")
#         self.conn.close()

#     def get_default_settings(self, name: Names) -> str:
#         """Get the default settings."""
#         with sqlite3.connect(self.default_db_name) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM defaults")
#             data = cursor.fetchall()
#         text = data[name.value][3]
#         try:
#             print(json.loads(text))
#         except:
#             print(text)

# # Regular Expression for Log Parsing
# pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:,\d{3})?) - (?: ?(?P<logger>[\w\.]+) - )?(?P<level>[A-Z]+) - (?P<message>.+)"

# def parse_and_insert_log(log_manager: LogManager, log_entry: str) -> None:
#     """Parse a log entry and insert it into the database."""
#     match = re.match(pattern, log_entry)
#     print(log_entry)
#     if match:
#         data = match.groupdict()
#         log_manager.insert_log(
#             data['timestamp'], data['logger'], data['level'], data['message'])
#         log.debug(f"Inserted log: {data}")
#     else:
#         log.debug("Log format didn't match. Entry skipped.")


# class Log:
#     """
#     Log class

#     This class is used to represent a log entry. It has a date, level and
#     message attribute. It can be initialized with a string or with the
#     individual attributes.
#     """

#     def __init__(self, value: str=None, date: str=None, level: str=None, message: str=None):
#         if value is not None:
#             value = value.split(" - ")
#             value = [v.strip() for v in value]
#             self.date = value[0]
#             self.level = value[2]
#             self.message = value[3]
#         else:
#             self.date = date
#             self.level = level
#             self.message = message

#     @staticmethod
#     def parse(value: str) -> tuple:
#         value = value.split(" - ")
#         value = [v.strip() for v in value]
#         return (value[0], value[2], value[3])

#     def __str__(self) -> str:
#         return f"{self.date} {self.level} {self.message}"


# if __name__ == "__main__":
#     logger = AppLogger("logger")
#     logger.info("test")

#     print(AppLogger.get_logs())
