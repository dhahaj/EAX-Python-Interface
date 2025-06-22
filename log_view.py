from qtpy.QtCore import QByteArray
from qtpy.QtCore import Qt, QDateTime
from qtpy.QtWidgets import QWidget, QTableWidgetItem
from qtpy.QtCore import QThread, Signal
from typing import List, Dict
from ui.ui_LogView import Ui_LogView
from ui.ui_ProgressBar import Ui_ProgressBar
from settings import get_instance
from imports import get_stylesheet, take_screenshot
from globals import logger as log

class LogView(QWidget, Ui_LogView):
    """
    A widget for displaying logs entries.

    :param data: The log data to be displayed, expected as a list of dict objects.
    :param callback: Optional callback function to be called when the dialog is closed and entries have been removed.
    :param *args: Optional additional arguments.
    """

    def __init__(self, data, callback=None, *args):
        super().__init__()
        self.setupUi(self)
        self.load_data(data)
        self.tableWidget.itemChanged.connect(self.on_item_changed)
        self.data = data
        self.callback = callback
        self.data_changed = False
        self.settings = get_instance()
        print('LogView settings =', self.settings)

        self.restoreGeometry(self.settings.app_settings.value("logwindow/geometry", QByteArray()))
        self.setStyleSheet(get_stylesheet(self.settings))

    def on_item_changed(self, item) -> None:
        row, col = item.row(), item.column()

        row_data = [self.tableWidget.item(row, column).text() for column in range(self.tableWidget.columnCount())]
        print(f"Row {row_data}")
        new_value = item.text()
        original_data = self.data[row]

        print(f"Original data: {original_data}")
        print(f"Data at row {row}, column {col} has been changed to: {new_value}")

        # if col == 1:
        #     logg.update_log(row_data[0], timestamp=new_value)
        # elif col == 2:
        #     logg.update_log(row_data[0], level=new_value)
        # elif col == 3:
        #     logg.update_log(row_data[0], message=new_value)

    def delete_selected_rows(self) -> None:
        """Deletes the currently selected rows from the table."""
        selected_rows = set(index.row() for index in self.tableWidget.selectedIndexes())
        self.data_changed = True
        for row in sorted(selected_rows, reverse=True):
            self.tableWidget.removeRow(row)

    def load_data(self, data) -> None:
        horHeaders = ["id", "timestamp", "function", "level", "message"]
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setHorizontalHeaderLabels(horHeaders)
        fmt = "yyyy-MM-dd HH:mm:ss"
        for i, entry in enumerate(data):
            ts_str = entry.get("timestamp")
            ts_item = QTableWidgetItem(ts_str)

            # store a sortable key in UserRole
            dt = QDateTime.fromString(ts_str, fmt)
            ts_item.setData(Qt.UserRole, dt.toSecsSinceEpoch())

            # the rest of the columns
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(entry.get("id"))))
            self.tableWidget.setItem(i, 1, ts_item)
            self.tableWidget.setItem(i, 2, QTableWidgetItem(entry.get("function")))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(entry.get("level")))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(entry.get("message")))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        # enable sorting and force an initial “newest-first” view
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.sortItems(1, Qt.SortOrder.DescendingOrder)
        self.tableWidget.resizeColumnToContents(2)

    def closeEvent(self, event) -> None:
        self.settings.app_settings.setValue("logwindow/geometry", self.saveGeometry())
        if self.data_changed and self.callback is not None:
            self.callback(self.extract_data())
        self.deleteLater()
        event.accept()

    def keyPressEvent(self, event) -> None:
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_F2:
            take_screenshot()
        elif key == Qt.Key_Delete:
            self.delete_selected_rows()
        super().keyPressEvent(event)

    def extract_data(self) -> List[Dict[str, str]]:
        """Extracts data from the table and returns as a list of dictionaries."""
        # progress = QProgressBar(self)
        # progress.setRange(0, self.tableWidget.rowCount())
        # progress.setWindowModality(Qt.WindowModal)
        # progress.setWindowTitle("Saving data...")
        # progress.show()

        data = []
        for i in range(self.tableWidget.rowCount()):
            timestamp = self.tableWidget.item(i, 1).text()
            function = self.tableWidget.item(i, 2).text()
            level = self.tableWidget.item(i, 3).text()
            message = self.tableWidget.item(i, 4).text()
            data.append({"timestamp": timestamp, "function": function, "level": level, "message": message})
        return data


class SaveWorker(QThread):
    """
    A worker thread for saving log data to the database.

    :param data: The log data to be saved.
    """

    progress_changed = Signal(int)

    def __init__(self, data: List[Dict[str, str]]):
        super(SaveWorker, self).__init__()
        self.data = data
        self.length = self.data.__len__()
        self.setObjectName("SaveWorker")

    def run(self):
        log.clear_logs()
        self.setPriority(QThread.HighestPriority)
        rows = [
            (e['timestamp'], e['level'], e['message'], e['function'])
            for e in self.data
        ]
        import sqlite3
        CHUNK = 1000
        SQL = "INSERT INTO logs (timestamp, level, message, function) " "VALUES (?, ?, ?, ?)"
        with sqlite3.connect(log.database) as conn:
            cur = conn.cursor()
            for i in range(0, len(rows), CHUNK):
                cur.executemany(SQL, rows[i: i + CHUNK])
                conn.commit()  # one commit per chunk
                self.progress_changed.emit((i + CHUNK) * 100 // len(rows))

                self.progress_changed.emit(100)
                log.info("Logs saved successfully.")




class ProgressBar(QWidget, Ui_ProgressBar):
    """
    A progress bar dialog window.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.settings = get_instance()
        # print("ProgressBar settings =", self.settings)

        self.setStyleSheet(get_stylesheet(self.settings))

    def update_progress(self, value: int) -> None:
        self.progressBar.setValue(value)
        if value >= 100:
            self.close()
