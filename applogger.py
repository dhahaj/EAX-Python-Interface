from loguru import logger
import sqlite3
from datetime import datetime
import config_loader
import sys


class AppLogger:

    def __init__(self, logfile="logs/app_{time:YYYY-MM-DD}.log", database="logs.db"):

        logger.remove()  # ditch the default DEBUG→stderr sink
        try:
            self.log_config = config_loader.get_config().get('logging')
            if sys.stderr and hasattr(sys.stderr, "write"):
                logger.add(sys.stderr, level=self.log_config.get('console_log_level', 'DEBUG').upper())
            logger.add(
                self.log_config.get('log_file', logfile),
                rotation=self.log_config.get('log_rotation', "00:00"),
                retention=self.log_config.get('log_retention', "30 days"),
                level=self.log_config.get('log_level', 'DEBUG').upper(),
                format=self.log_config.get('log_format', "{time} | {level} | {message}"),
            )

            self.db_log_level = self.log_config.get('db_log_level', 'DEBUG').upper()
            self._db_level_no = logger.level(self.db_log_level).no if self.db_log_level else logger.level('DEBUG').no
            self.database = self.log_config.get('database_file', database)

        except Exception as e:
            print(f"Error loading config: {e}")
            self.log_config = None
            logger.add(logfile, rotation="00:00", retention="30 days", level='DEBUG', format="{time} | {function} | {level} | {message}")
            self.database = database
            self._db_level_no = logger.level('DEBUG').no

        self.use_database = self.log_config.get('use_database', True) if self.log_config else True

        self.migrate_schema()
        self.create_log_table()

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
        if self.use_database and logger.level(level).no >= self._db_level_no:
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
        self._emit("ERROR", message, extra_depth=1)

    def trace(self, message: str):
        self._emit("TRACE", message)

    def catch(self, exception: Exception):
        """Catch exceptions and log them."""
        logger.exception(exception)
        self._emit("CRITICAL", str(exception.__class__.__name__) + ": " + str(exception), extra_depth=1)

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

    def size(self) -> int:
        """Get the size of the logs in the SQLite database."""
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM logs")
            count = cursor.fetchone()[0]
        return count

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

    def search_logs(self, search_term: str, function: str = None) -> list:
        """Search logs in the SQLite database for a specific term."""
        results = []
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            if function:
                cursor.execute("SELECT * FROM logs WHERE message LIKE ? AND function LIKE ?", ('%' + search_term + '%', '%' + function + '%'))
            else:
                cursor.execute("SELECT * FROM logs WHERE message LIKE ?", ('%' + search_term + '%',))
            rows = cursor.fetchall()
            for row in rows:
                log_entry = {
                    "id": row[0],
                    "timestamp": row[1],
                    "level": row[2],
                    "message": row[3],
                    "function": row[4]
                }
                results.append(log_entry)
        return results

    def log_from_file(self, log_file: str) -> list:
        """Read a log file and return its contents as a list of dictionaries."""
        logs = []
        with open(log_file, "r") as file:
            for line in file:
                try:
                    # Assuming the log format is consistent with the database schema
                    timestamp, level, function, message = line.strip().split(" | ", 3)
                    log_entry = {
                        "timestamp": timestamp,
                        "level": level,
                        "function": function,
                        "message": message
                    }
                    logs.append(log_entry)
                except ValueError as e:
                    logger.error(f"Error parsing line in log file {log_file}: {e}")
        return logs

    def tail(self, n: int = 10) -> list:
        """Get the last n lines from the SQLite database."""
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (n,))
            rows = cursor.fetchall()
            logs = []
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


_singleton: "AppLogger | None" = None


def get_logger() -> AppLogger:
    """Get the singleton instance of AppLogger."""
    global _singleton
    if _singleton is None:
        _singleton = AppLogger()
    return _singleton


if __name__ == "__main__":
    log_ = get_logger()
    print(log_)
    log_.info("This is an info message")
    log_.error("This is an error message")
    log_.debug("This is a debug message")
    log_.success("This is a success message")
    log_.warning("This is a warning message")
    log_.critical("This is a critical message")
    log_.exception("This is an exception message")
    log_.trace("This is a trace message")

    try:
        1 / 0
    except Exception as e:
        log_.catch(e)

    for i in log_.tail(10):
        print(i)
