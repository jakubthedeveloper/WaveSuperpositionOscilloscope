import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import QTimer


class Oscilloscope(QWidget):
    def __init__(self, title, mode="wave"):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- plot widget ---
        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot)

        # --- background ---
        self.plot.setBackground("#000800")  # very dark green
        self.plot.hideAxis("bottom")
        self.plot.hideAxis("left")

        # fixed ranges
        vb = self.plot.getPlotItem().getViewBox()
        vb.disableAutoRange(axis=pg.ViewBox.XAxis)
        vb.disableAutoRange(axis=pg.ViewBox.YAxis)

        # state
        self.mode = None
        self.history = []  # waveform history (for glow)
        self.dot_history = []  # XY history (for smear)

        # --- curves (waveform) ---
        self.curve_main = self.plot.plot(
            pen=pg.mkPen((0, 255, 0, 255), width=3)
        )
        self.curve_glow1 = self.plot.plot(
            pen=pg.mkPen((0, 255, 0, 80), width=10)
        )
        self.curve_glow2 = self.plot.plot(
            pen=pg.mkPen((0, 200, 0, 40), width=18)
        )

        # XY dot trail
        self.dot_tail = self.plot.plot(
            pen=pg.mkPen((0, 255, 0, 50), width=8)
        )

        # --- dot (XY) ---
        self.dot = self.plot.plot(
            pen=None,
            symbol="o",
            symbolBrush=pg.mkBrush(0, 255, 0, 220),
            symbolSize=12,
        )

        # --- vignette using painter overlay ---
        self.overlay_timer = QTimer()
        self.overlay_timer.timeout.connect(self.repaint)
        self.overlay_timer.start(33)

        self.set_mode(mode)

    # ===========================================
    # UPDATE SIGNAL (with afterglow)
    # ===========================================
    def update(self, t, y):
        if self.mode == "wave":
            self._update_wave(t, y)
        elif self.mode == "dot":
            # for dot mode, expect t to be scalar x, y to be scalar y
            self._update_dot(t, y)

    def _update_wave(self, t, y):
        # save history for glow
        self.history.insert(0, (t.copy(), y.copy()))
        self.history = self.history[:3]

        # main bright trace
        self.curve_main.setData(t, y)

        # glow trails
        if len(self.history) > 1:
            t1, y1 = self.history[1]
            self.curve_glow1.setData(t1, y1)

        if len(self.history) > 2:
            t2, y2 = self.history[2]
            self.curve_glow2.setData(t2, y2)

        self.dot.setData([], [])

    def _update_dot(self, x, y):
        # keep short history for smear effect
        self.dot_history.append((x, y))
        self.dot_history = self.dot_history[-60:]

        xs, ys = zip(*self.dot_history)

        self.history.clear()
        self.curve_main.setData([], [])
        self.curve_glow1.setData([], [])
        self.curve_glow2.setData([], [])
        self.dot_tail.setData(xs, ys)
        self.dot.setData([x], [y])

    # ===========================================
    # VIGNETTE / BLOOM OVERLAY
    # ===========================================
    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # subtle vignette
        gradient_color = QColor(0, 20, 0, 150)
        brush = QBrush(gradient_color)
        painter.fillRect(self.rect(), brush)

        painter.end()

    # ===========================================
    # MODE SWITCHING
    # ===========================================
    def set_mode(self, mode):
        self.mode = mode
        if mode == "wave":
            self.plot.setXRange(0, 0.002)
            self.plot.setYRange(-2, 2)
            self.curve_main.show()
            self.curve_glow1.show()
            self.curve_glow2.show()
            self.dot_tail.hide()
            self.dot.hide()
            self.dot_history.clear()
        elif mode == "dot":
            # symmetric range for XY dot plot
            self.plot.setXRange(-2, 2)
            self.plot.setYRange(-2, 2)
            self.curve_main.hide()
            self.curve_glow1.hide()
            self.curve_glow2.hide()
            self.dot_tail.show()
            self.dot.show()
