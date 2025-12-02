import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import QTimer


class Oscilloscope(QWidget):
    def __init__(self, title):
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
        self.plot.setXRange(0, 0.002)
        self.plot.setYRange(-2, 2)

        # --- curves ---
        # Main bright beam (glow core)
        self.curve_main = self.plot.plot(
            pen=pg.mkPen((0, 255, 0, 255), width=3)
        )

        # Afterglow layers (smearing)
        self.curve_glow1 = self.plot.plot(
            pen=pg.mkPen((0, 255, 0, 80), width=10)
        )
        self.curve_glow2 = self.plot.plot(
            pen=pg.mkPen((0, 200, 0, 40), width=18)
        )

        # History for glow
        self.history = []

        # --- noise overlay ---
        self.noise_curve = self.plot.plot(
            pen=pg.mkPen((0, 255, 0, 20), width=1)
        )
        self.noise_timer = QTimer()
        self.noise_timer.timeout.connect(self.update_noise)
        self.noise_timer.start(40)

        # --- vignette using painter overlay ---
        self.overlay_timer = QTimer()
        self.overlay_timer.timeout.connect(self.repaint)
        self.overlay_timer.start(33)

    # ===========================================
    # NOISE
    # ===========================================
    def update_noise(self):
        x = np.linspace(0, 1, 200)
        y = np.random.normal(0, 0.01, 200)
        self.noise_curve.setData(x, y)

    # ===========================================
    # UPDATE SIGNAL (with afterglow)
    # ===========================================
    def update(self, t, y):
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

