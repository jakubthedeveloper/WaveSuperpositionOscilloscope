import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout
from waveform_logic import WaveformGenerator
from oscilloscope import Oscilloscope
from controls import ControlsPanel
from controls_presets import PresetPanel


class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wave Superposition")

        grid = QGridLayout()
        self.setLayout(grid)

        self.wave = WaveformGenerator()

        # oscilloscopes
        self.scope1 = Oscilloscope("Wave 1")
        self.scope2 = Oscilloscope("Wave 2")
        self.scope_sum = Oscilloscope("Sum")

        # control panels
        self.ctrl1 = ControlsPanel("Wave 1", 1, self)
        self.ctrl2 = ControlsPanel("Wave 2", 2, self)
        self.ctrl3 = PresetPanel(self, "Presets")

        # layout grid
        grid.addWidget(self.scope1, 0, 0)
        grid.addWidget(self.scope2, 0, 1)
        grid.addWidget(self.scope_sum, 0, 2)

        grid.addWidget(self.ctrl1, 1, 0)
        grid.addWidget(self.ctrl2, 1, 1)
        grid.addWidget(self.ctrl3, 1, 2)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        grid.setRowStretch(0, 3)
        grid.setRowStretch(1, 1)

        self.wave.start(self.update_all)

    def update_all(self):
        t1, y1 = self.wave.generate(1)
        t2, y2 = self.wave.generate(2)
        ts, ys = self.wave.generate_sum()

        self.scope1.update(t1, y1)
        self.scope2.update(t2, y2)
        self.scope_sum.update(ts, ys)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec())

