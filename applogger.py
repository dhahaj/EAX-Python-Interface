from loguru import logger
import sqlite3
from datetime import datetime
import config_loader
from device import Device


class AppLogger:

    def __init__(self, logfile="logs/app_{time:YYYY-MM-DD}.log", database="logs.db"):

        try:
            log_config = config_loader.get_instance().get('logging')
            logger.add(
                log_config.get('log_file', logfile),
                rotation=log_config.get('log_rotation', "00:00"),
                retention=log_config.get('log_retention', "7 days"),
                level=log_config.get('log_level', 'DEBUG'),
                format=log_config.get('log_format', "{time} | {level} | {message}"),
            )
            self.database = log_config.get('database_file', database)
        except Exception as e:
            print(f"Error loading config: {e}")
            log_config = None
            logger.add(logfile, rotation="00:00", retention="35 MB", level='DEBUG', format="{time} | {function} | {level} | {message}")
            self.database = database

        self.migrate_schema()
        self.create_log_table()
        self.init_statistics_table()

    def create_log_table(self):
        """Creates a table for logs in the SQLite database if it doesn't exist."""
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                level TEXT,
                message TEXT,
                function TEXT
            )''')
            conn.commit()

    def _emit(self, level: str, message: str, *, extra_depth: int = 0):
        function_name = None

        def capture(record):
            nonlocal function_name
            function_name = record["function"]

        # Emit log and capture function name
        logger.opt(depth=2 + extra_depth).patch(capture).log(level.upper(), message)

        # Log to database with captured function name
        self.log_to_db(level.upper(), message, function_name or 'unknown')

    def log_to_db(self, level: str, message: str, function: str):
        """Log messages explicitly to the SQLite database."""
        try:
            with sqlite3.connect(self.database) as conn:
                cursor = conn.cursor()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    'INSERT INTO logs (timestamp, level, message, function) VALUES (?, ?, ?, ?)',
                    (timestamp, level, message, function)
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"SQLite error: {e}")

    def clear_logs(self):
        """Clear all logs from the SQLite database."""
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM logs")
            conn.commit()

    def add_log(self, timestamp: str, level: str, message: str, function: str):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO logs (timestamp, level, message, function) VALUES (?, ?, ?, ?)',
                (timestamp, level, message, function)
            )
            conn.commit()

    def migrate_schema(self):
        """Check and migrate the database schema if necessary."""
        try:
            with sqlite3.connect(self.database) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(logs)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'function' not in columns:
                    cursor.execute("ALTER TABLE logs ADD COLUMN function TEXT DEFAULT 'unknown'")
                    conn.commit()
                    logger.info("Database schema migrated: added 'function' column.")
        except Exception as e:
            logger.error(f"Error migrating schema: {e}")

    def log(self, level: str, message: str):
        self._emit(level, message)

    def info(self, message: str):
        self._emit("INFO", message)

    def error(self, message: str):
        self._emit("ERROR", message)

    def debug(self, message: str, extra_depth: int = 0):
        self._emit("DEBUG", message, extra_depth=extra_depth)

    def critical(self, message: str):
        self._emit("CRITICAL", message)

    def success(self, message: str):
        self._emit("SUCCESS", message)

    def warning(self, message: str):
        self._emit("WARNING", message)

    def exception(self, message: str):
        self._emit("EXCEPTION", message, extra_depth=1)

    def get_logs(self) -> list:
        logs = []
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs")
            rows = cursor.fetchall()
            for row in rows:
                log_entry = {
                    "id": row[0],
                    "timestamp": row[1],
                    "level": row[2],
                    "message": row[3],
                    "function": row[4]
                }
                logs.append(log_entry)
        return logs

    def read_log_into_database(self, log_file: str):
        """Read a log file and insert its contents into the SQLite database."""
        with open(log_file, "r") as file:
            for line in file:
                # Assuming the log format is consistent with the database schema
                timestamp, level, function, message = line.strip().split(" | ", 3)
                print(f"timestamp: {timestamp}, level: {level}, function: {function}, message: {message}")
                self.add_log(timestamp, level, message, function)

    def dump_logs(self):
        """Dump all logs from the SQLite database."""
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def init_statistics_table(self):
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS test_runs (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                device    TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """)
            conn.commit()

    def increment_tests_run(self, device: str = None) -> None:
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("INSERT INTO test_runs (device, timestamp) VALUES (?, ?)", (device, timestamp))
            conn.commit()

    def get_tests_run(self) -> int:
        with sqlite3.connect(self.database) as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM test_runs")
            total, = cur.fetchone()
            return total    



if __name__ == "__main__":
    logger = AppLogger()

    logger.increment_tests_run(device="EAX500")
    total_tests = logger.get_tests_run()    
    print(f"Total tests run: {total_tests}")