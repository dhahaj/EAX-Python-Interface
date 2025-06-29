# %%
#!/usr/bin/env python
import sys
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QWidget, QProgressBar
)

class Spinner(QWidget):
    """
    Simple busy-indicator: 12 fading spokes that rotate with a timer.
    """

    def __init__(self, radius=20, line_width=3, color=Qt.darkCyan, parent=None):
        super().__init__(parent)
        self._radius = radius
        self._line_width = line_width
        self._color = color
        self._angle = 0
        self._timer = QTimer(self, timeout=self.rotate)
        self._timer.start(80)         # adjust for speed (ms)
        size = (radius + line_width) * 2 + 2
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def rotate(self):
        self._angle = (self._angle + 30) % 360           # 30° = 12 spokes
        self.update()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._angle)

        for i in range(12):
            alpha = int(255 * (i + 1) / 12) # fade tail
            # color, width, style, cap
            pen = QPen(self._color,
                       self._line_width,
                       Qt.SolidLine,
                       Qt.RoundCap) # <- round ends
            pen.setColor(pen.color().lighter(100 + (alpha * 100 // 255)))
            painter.setPen(pen)
            painter.drawLine(QPointF(0, -self._radius),
                             QPointF(0, -self._radius // 2))
            painter.rotate(360 // 12)


class BusyDialog(QDialog):
    """
    Drop-in busy dialog.  Set `modal=True` if you want it to block interaction.
    """

    def __init__(self, text="Working...", modal=True, parent=None):
        super().__init__(parent, Qt.Dialog | Qt.FramelessWindowHint)
        if modal:
            self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.spinner = Spinner()
        layout.addWidget(self.spinner, alignment=Qt.AlignCenter)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setStyleSheet("""
            QDialog {background:#20252e; border-radius:12px;}
            QLabel  {color: white; font-size: 14pt;}
        """)


class ProgressDialog(QDialog):
    """
    Modal dialog with both an indeterminate spinner and a determinate bar.
    Call .set_progress(value, maximum) from your worker thread/slot.
    """

    def __init__(self, text="Working…", parent=None):
        super().__init__(parent, Qt.Dialog | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

        lay = QVBoxLayout(self)
        lay.setSpacing(16)
        lay.setContentsMargins(24, 24, 24, 24)

        self.label = QLabel(text, alignment=Qt.AlignCenter)
        lay.addWidget(self.label)

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)   # we’ll scale later
        self.bar.setValue(0)
        self.bar.setTextVisible(True)
        lay.addWidget(self.bar)

        self.setStyleSheet("""
            QDialog      {border-radius:12px;}
            QLabel       {font-size:16pt;}
            QProgressBar {background:#31363f; border:1px solid #444;
                          border-radius:6px; text-align:center;
                          height:14px; color:white; font-size:12pt;}
            QProgressBar::chunk {background-color:#2da1ff; border-radius:6px;}
        """)

    # public API ------------------------------------------------------------
    def set_progress(self, value, maximum=100):
        """Update the bar.  If maximum==0 we show an indeterminate bar."""
        if maximum == 0:
            self.bar.setRange(0, 0)        # Qt’s “busy” bar
        else:
            self.bar.setRange(0, maximum)
            self.bar.setValue(value)


# ───────── demo ─────────
if __name__ == "__main__":
    app = QApplication(sys.argv)

    dlg2 = BusyDialog("Please wait…", modal=True)
    dlg2.show()

    dlg = ProgressDialog("Flashing firmware…")
    dlg.show()

    # fake workload: drive progress to 100 % in 5 s
    current = {"v": 0}

    def tick():
        current["v"] += 5
        dlg.set_progress(current["v"], 0)
        if current["v"] >= 100:
            dlg.accept()
    QTimer.singleShot(100, tick)           # slight delay before first update
    timer = QTimer(interval=250, timeout=tick)
    timer.start()


    sys.exit(app.exec())
