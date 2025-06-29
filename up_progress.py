# up_qt.py  –  drive UP.exe quietly and stream its progress into a QProgressBar
# PySide6-only, Windows-only, works with 32- or 64-bit UP package.
from settings import get_instance
import ctypes
import shutil
import os
import sys
import time
import ini
from config_loader import get_config
from settings import get_instance as get_settings
from constants import KEY_CHIP_PART
from qtpy.QtCore import Qt
from PySide6.QtCore import QObject, QProcess, QTimer, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, \
    QProgressBar, QLabel
from ui.ui_ProgressBar import Ui_ProgressBar
from imports import get_stylesheet

# ---------------------------------------------------------------------------
#  Win32 helpers (same as before, but prototypes included)
# ---------------------------------------------------------------------------
k32 = ctypes.windll.kernel32

OpenFileMappingW = k32.OpenFileMappingW
OpenFileMappingW.argtypes = (ctypes.c_uint, ctypes.c_bool, ctypes.c_wchar_p)
OpenFileMappingW.restype = ctypes.c_void_p

MapViewOfFile = k32.MapViewOfFile
MapViewOfFile.argtypes = (ctypes.c_void_p, ctypes.c_uint,
                          ctypes.c_uint, ctypes.c_uint,
                          ctypes.c_size_t)
MapViewOfFile.restype = ctypes.c_void_p

UnmapViewOfFile = k32.UnmapViewOfFile
UnmapViewOfFile.argtypes = (ctypes.c_void_p,)
UnmapViewOfFile.restype = ctypes.c_bool

CloseHandle = k32.CloseHandle
CloseHandle.argtypes = (ctypes.c_void_p,)
CloseHandle.restype = ctypes.c_bool

FILE_MAP_READ = 0x0004
INT_SIZE = ctypes.sizeof(ctypes.c_int)


class UPJob(QObject):
    """
    UPJob class for managing UNISOFT UP.exe programming processes with progress monitoring.
    This class runs UP.exe as a QProcess and monitors its progress via shared memory.
    It provides real-time progress updates and handles timeouts and process completion.

    Methods:
        start(): Launches the UP.exe process with appropriate arguments and begins
                 monitoring progress via shared memory
        firmware_path (str): Path to the firmware file to be programmed
        job = UPJob("path/to/firmware.hex")
        to monitor programming progress in real-time. The process will be automatically
        terminated if it exceeds the specified timeout duration.
    Attributes:
        progressChanged (Signal): Emitted when programming progress changes (0-100%)
        finished (Signal): Emitted when the UP.exe process finishes with its exit code
    Args:
        firmware_path (str): Path to the firmware file to be programmed.
            This should be a valid file path to the firmware binary.
        window_id (str, optional): Window identifier used for shared memory naming. 
            Defaults to "up1".
        timeout_s (int, optional): Maximum time in seconds allowed for programming.
            Defaults to 180 seconds.
        parent (QObject, optional): Parent QObject. Defaults to None.
    Raises:
        FileNotFoundError: If up.exe is not found on the system PATH
    Examples:
        ```python
        job = UPJob("my_project.ppr")
        job.progressChanged.connect(update_progress_bar)
        job.finished.connect(on_programming_done)
        job.start()
        ```
    Note:
        This class uses Windows API functions to access shared memory created by UP.exe
        to monitor programming progress in real-time.
    """
    progressChanged = Signal(int)   # 0-100 %
    finished = Signal(int)          # UP.exe exit code

    def __init__(self,
                 firmware_path: str,
                 timeout_s: int = 180,
                 parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.firmware_path = firmware_path
        self.win_id = "up1" 
        self.timeout_s = timeout_s

        self._proc = QProcess(self)
        self._timer = QTimer(self, interval=25) # 25 ms poll
        self._t0 = time.perf_counter()
        self._h_map = None
        self._view = None
        self._proc.finished.connect(self._on_process_finished)
        self._timer.timeout.connect(self._poll_progress)

        ini_path = 'firmware/template.ppr'
        ppr = ini.load(ini_path)  # load the template PPR file
        settings = get_settings()

        ppr["Hardware"]["Part"] = settings.get(KEY_CHIP_PART, "PIC16F628A") # set chip part
        ppr["Hardware"]["PortBase"] = "-1"  # use first available programmer
        ppr['HexFile']['FileName'] = os.path.basename(self.firmware_path) # set firmware file name
        ppr['SpecSettings.PREST']['ProgPower'] = "1"  # enable power during programming

        # write the PPR file to disk
        ini.dump(ppr, ini_path)

    def start(self) -> None:
        if not (up_exe := shutil.which("up.exe")):
            up_exe = get_config().get_programmer_path()
        args = get_config().get_programmer_arguments()
        self._proc.setProgram(up_exe)
        self._proc.setArguments(args)
        self._proc.start()
        self._timer.start()     # begin polling for shared memory + progress

    @Slot()
    def _poll_progress(self) -> None:
        # ① attach to mapping once; ② read int every tick; ③ stop on 100 % or timeout
        if self._h_map is None:
            name = f"{self.win_id}_Progress"
            self._h_map = OpenFileMappingW(FILE_MAP_READ, False, name)
            if not self._h_map:
                if time.perf_counter() - self._t0 > 20:      # 20 s attach timeout
                    self._abort("Failed to open shared memory")
                return

            self._view = MapViewOfFile(self._h_map, FILE_MAP_READ, 0, 0, INT_SIZE)
            if not self._view:
                self._abort("MapViewOfFile failed")
                return

            self._c_int_ptr = ctypes.cast(self._view, ctypes.POINTER(ctypes.c_int))

        # read current value
        val = self._c_int_ptr.contents.value
        self.progressChanged.emit(val)

        if val >= 100:
            self._timer.stop()     # will wait for UP.exe to exit normally
        elif time.perf_counter() - self._t0 > self.timeout_s:
            self._abort("Programming timed out")

    @Slot(int, QProcess.ExitStatus)
    def _on_process_finished(self, exit_code: int, status: QProcess.ExitStatus) -> None:
        self._timer.stop()
        self._cleanup()
        self.finished.emit(exit_code)

    def _abort(self, reason: str) -> None:
        print("UPJob abort:", reason, file=sys.stderr)
        self._proc.kill()
        self._proc.waitForFinished(1000)
        self._on_process_finished(-1, QProcess.CrashExit)

    def _cleanup(self) -> None:
        if self._view:
            UnmapViewOfFile(self._view)
        if self._h_map:
            CloseHandle(self._h_map)


# ---------------------------------------------------------------------------
#  Tiny demo window
# ---------------------------------------------------------------------------

class MainWnd(QWidget):
    def __init__(self, ppr_path: str = 'firmware/EAX505_591.hex') -> None:
        super().__init__()
        self.setWindowTitle("UP programmer demo")

        self.pb = QProgressBar(minimum=0, maximum=100)
        self.lbl = QLabel("idle")
        btn = QPushButton("Program")

        lay = QVBoxLayout(self)
        lay.addWidget(self.pb)
        lay.addWidget(self.lbl)
        lay.addWidget(btn)

        btn.clicked.connect(lambda _=None: self.start_job(ppr_path))
        

    def start_job(self, ppr: str) -> None:
        self.progress_bar = ProgressBar()
        self.progress_bar.label.setText("Programming…")
        self.progress_bar.progressBar.setValue(50)
        self.progress_bar.show()

        self.job = UPJob(ppr) # window id defaults to “up1”
        self.job.progressChanged.connect(self.pb.setValue)
        self.job.progressChanged.connect(lambda v: self.lbl.setText(f"{v}%"))
        self.job.progressChanged.connect(lambda v: self.progress_bar.update_progress(v))
        self.job.finished.connect(self._job_done)
        self.job.start()
        self.lbl.setText("running…")


    @Slot(int)
    def _job_done(self, code: int) -> None:
        self.lbl.setText(f"done (rc={code})")
        self.progress_bar.close()
        self.close()


class ProgressBar(QWidget, Ui_ProgressBar):
    """
    A progress bar dialog window.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setStyleSheet(get_stylesheet(get_instance()))

    def update_progress(self, value: int) -> None:
        self.progressBar.setValue(value)
        if value >= 100:
            self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = MainWnd()
    wnd.resize(300, 100)
    wnd.show()
    sys.exit(app.exec())
