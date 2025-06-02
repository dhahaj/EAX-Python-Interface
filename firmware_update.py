from qtpy.QtCore import QProcess, Signal, Slot
import os
from qtpy.QtWidgets import QMainWindow


class FirmwareUpdateProcess(QProcess):
    """Process to update the test fixture firmware."""

    # emit decoded stdout whenever new data arrives
    outputReceived = Signal(str)
    # emit exit code when finished
    finishedWithCode = Signal(int, QProcess.ExitStatus, bool)

    def __init__(self, parent: QMainWindow = None):
        super().__init__(parent)
        self.parent: QMainWindow = parent
        self.setWorkingDirectory(os.getcwd())
        self.errorOccurred.connect(self._on_error)
        self.finished.connect(self._on_finished)
        self.readyReadStandardOutput.connect(self._read_standard_output)
        self.readyReadStandardError.connect(self._read_standard_error)
        self.device_connected = False

    @Slot()
    def _read_standard_output(self):
        """Read the standard output of the process."""
        output = self.readAllStandardOutput().data().decode()
        self.outputReceived.emit(output)

    @Slot()
    def _read_standard_error(self):
        """Read the standard error of the process."""
        error = self.readAllStandardError().data().decode()
        self.outputReceived.emit(error)

    @Slot(int, QProcess.ExitStatus)
    def _on_finished(self, exit_code, exit_status):
        self.finishedWithCode.emit(exit_code, exit_status, self.device_connected)

    @Slot(QProcess.ProcessError)
    def _on_error(self, error: QProcess.ProcessError):
        self.parent.on_error(error)
        self.finishedWithCode.emit(-1, QProcess.ExitStatus.NormalExit, self.device_connected)

    def run(self, program: str, args: list[str] = None):
        """Convenience method to start a process."""
        self.setProgram(program)
        self.setArguments(args or [])
        self.start()
