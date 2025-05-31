from PySide6.QtCore import QSettings
from PySide6.QtCore import QObject, Signal

from constants import APP_NAME, COMPANY_NAME


class Counter(QObject):
    """
    A simple counter class that uses QSettings to store and retrieve the count value.
    """

    valueChanged = Signal(int)

    def __init__(self, var_name: str):
        """
        Initialize the counter with a variable name.
        """
        super().__init__()
        self.qsettings: QSettings = QSettings(QSettings.Scope.UserScope, COMPANY_NAME, APP_NAME)
        self.var_name = var_name

    @property
    def value(self) -> int:
        return self.get()

    @value.setter
    def value(self, new_value: int):
        if isinstance(new_value, int):
            self.qsettings.setValue(self.var_name, new_value)
            self.valueChanged.emit(new_value)
            self.qsettings.sync()
        else:
            raise ValueError("Counter value must be an integer.")

    def get(self) -> int:
        """
        Get the current value of the counter.
        """
        return self.qsettings.value(self.var_name, 0, type=int)

    def increment(self):
        """
        Increment the counter by 1.
        """
        current_value = self.get()
        self.qsettings.setValue(self.var_name, current_value + 1)
        self.valueChanged.emit(current_value + 1)
        self.qsettings.sync()

    def reset(self):
        """
        Reset the counter to 0.
        """
        self.qsettings.setValue(self.var_name, 0)
        self.valueChanged.emit(0)
        self.qsettings.sync()


if __name__ == "__main__":
    # Example usage

    test_counter = Counter("test_counter")
    program_counter = Counter("program_counter")

    # Increment the counters
    test_counter.increment()
    program_counter.increment()

    # Print the current values
    print(f"Test Counter: {test_counter.get()}")
    print(f"Program Counter: {program_counter.get()}")
