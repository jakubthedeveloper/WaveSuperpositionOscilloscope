from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QLabel, QSlider, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt


class ControlsPanel(QGroupBox):
    def __init__(self, title, idx, main):
        super().__init__(title)

        self.idx = idx
        self.main = main
        self.wave = main.wave

        layout = QVBoxLayout()
        self.setLayout(layout)

        # amplitude
        la = QLabel("Amplitude")
        self.sa = QSlider(Qt.Orientation.Horizontal)
        self.sa.setRange(0, 200)
        self.sa.valueChanged.connect(self.set_amp)
        layout.addWidget(la)
        layout.addWidget(self.sa)

        # frequency
        lf = QLabel("Frequency (Hz)")
        self.sf = QSlider(Qt.Orientation.Horizontal)
        self.sf.setRange(0, 20000)
        self.sf.valueChanged.connect(self.set_freq)
        layout.addWidget(lf)
        layout.addWidget(self.sf)

        # waveform buttons
        layout.addWidget(QLabel("Waveform"))

        row = QHBoxLayout()
        self.btns = {}

        for name in ["sin", "sq", "tr"]:
            b = QPushButton(name)
            b.setCheckable(True)
            b.clicked.connect(lambda _, n=name: self.set_wave(n))
            row.addWidget(b)
            self.btns[name] = b

        layout.addLayout(row)

        self.refresh_ui()

    def refresh_ui(self):
        # amplitude
        self.sa.setValue(int(self.wave.A[self.idx] * 100))
        # frequency
        self.sf.setValue(int(self.wave.F[self.idx]))
        # waveform
        for k, b in self.btns.items():
            b.setChecked(k == self.wave.W[self.idx])

    def set_amp(self, v):
        self.wave.A[self.idx] = v / 100

    def set_freq(self, v):
        self.wave.F[self.idx] = v

    def set_wave(self, name):
        self.wave.W[self.idx] = name
        self.refresh_ui()

