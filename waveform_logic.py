import numpy as np
from PyQt6.QtCore import QTimer


def sin_wave(A, f, t): return A * np.sin(2*np.pi*f*t)
def sq_wave(A, f, t): return A * np.sign(np.sin(2*np.pi*f*t))
def tr_wave(A, f, t): return A * (2/np.pi) * np.arcsin(np.sin(2*np.pi*f*t))

WAVE = {
    "sin": sin_wave,
    "sq": sq_wave,
    "tr": tr_wave
}


class WaveformGenerator:
    def __init__(self):
        self.sample_rate = 2000
        self.window = 0.002

        self.phase = {1: 0.0, 2: 0.0}

        self.A = {1: 1.0, 2: 1.0}
        self.F = {1: 3000, 2: 3400}
        self.W = {1: "sin", 2: "sin"}

        self.S = {1: 0.000005, 2: 0.000005}

        self.timer = QTimer()
        self.timer.setInterval(8)

    def start(self, cb):
        self.timer.timeout.connect(cb)
        self.timer.start()

    def generate(self, idx):
        self.phase[idx] += self.S[idx]
        t = np.linspace(0, self.window, self.sample_rate)
        y = WAVE[self.W[idx]](self.A[idx], self.F[idx], t + self.phase[idx])
        return t, y

    def generate_sum(self):
        t = np.linspace(0, self.window, self.sample_rate)
        y1 = WAVE[self.W[1]](self.A[1], self.F[1], t + self.phase[1])
        y2 = WAVE[self.W[2]](self.A[2], self.F[2], t + self.phase[2])
        return t, y1 + y2

