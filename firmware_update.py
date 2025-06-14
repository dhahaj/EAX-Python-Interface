import os
from qtpy.QtCore import QProcess, Signal, Slot

class FirmwareUpdateProcess(QProcess):
    """Process to update the firmware.

    This class handles the firmware update process by managing the QProcess
    and providing signals to communicate with the main application.

    Signals:
        outputReceived (str): Emitted when new output is received from the process.
        finishedWithCode (int, QProcess.ExitStatus, bool): Emitted when the process finishes,
            providing the exit code, exit status, and whether a device was connected.
    Slots:
        _read_standard_output(): Reads the standard output of the process.
        _read_standard_error(): Reads the standard error of the process.
        _on_finished(int, QProcess.ExitStatus): Handles the process finishing.
        _on_error(QProcess.ProcessError): Handles errors that occur during the process.
    Attributes:
        parent (QObject): The parent object for this process.
        device_connected (bool): Indicates whether a device is connected.
        
    """

    # emit decoded stdout whenever new data arrives
    outputReceived = Signal(str)
    # emit exit code when finished
    finishedWithCode = Signal(int, QProcess.ExitStatus, bool)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
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
