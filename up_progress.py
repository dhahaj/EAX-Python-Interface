# up_qt.py  –  drive UP.exe quietly and stream its progress into a QProgressBar
# PySide6-only, Windows-only, works with 32- or 64-bit UP package.
import ctypes
import shutil
import os
import sys
import time
from PySide6.QtCore import QObject, QProcess, QTimer, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, \
    QProgressBar, QLabel

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
    progressChanged = Signal(int)          # 0-100 %
    finished = Signal(int)          # UP.exe exit code

    def __init__(self, ppr: str, window_id: str = "up1", timeout_s: int = 180, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.ppr = os.path.abspath(ppr)
        self.win_id = window_id
        self.timeout_s = timeout_s

        self._proc = QProcess(self)
        self._timer = QTimer(self, interval=100)      # 100 ms poll
        self._t0 = time.perf_counter()
        self._h_map = None
        self._view = None
        self._proc.finished.connect(self._on_process_finished)
        self._timer.timeout.connect(self._poll_progress)

    def start(self) -> None:
        up_exe = shutil.which("up.exe")
        if not up_exe:
            raise FileNotFoundError("up.exe not found on PATH")

        args = ["/p", self.ppr, "/q", "/w", self.win_id]
        self._proc.setProgram(up_exe)
        self._proc.setArguments(args)

        # Hide console window only if the Qt build supports it (Qt ≥ 6.5)
        if hasattr(self._proc, "setCreateProcessArgumentsModifier"):
            CREATE_NO_WINDOW = 0x08000000
            self._proc.setCreateProcessArgumentsModifier(
                lambda si: setattr(si, "dwFlags", si.dwFlags | CREATE_NO_WINDOW)
            )

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
    def _on_process_finished(self, exit_code: int,
                             status: QProcess.ExitStatus) -> None:
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
    def __init__(self, ppr_path: str = 'firmware/template.ppr') -> None:
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
        self.job = UPJob(ppr)                 # window id defaults to “up1”
        self.job.progressChanged.connect(self.pb.setValue)
        self.job.progressChanged.connect(lambda v:
                                         self.lbl.setText(f"{v}%"))
        self.job.finished.connect(self._job_done)
        self.job.start()
        self.lbl.setText("running…")

    @Slot(int)
    def _job_done(self, code: int) -> None:
        self.lbl.setText(f"done (rc={code})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = MainWnd(f"{'firmware/template.ppr'  if len(sys.argv) < 2 else sys.argv[1]}")
    wnd.resize(300, 100)
    wnd.show()
    sys.exit(app.exec())
