from loguru import logger
import sqlite3
from datetime import datetime


class AppLogger:
    def __init__(self, logfile="logs/app_{time:YYYY-MM-DD}.log", database="newlogs.db"):
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
            cursor.execute('INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)',
                           (timestamp, level, message))
            conn.commit()

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

    def get_logs(self) -> list:
        """Fetch logs from the database for the LogView class."""
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs")
            return cursor.fetchall()
