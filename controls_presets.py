from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
import json
import os


class PresetPanel(QGroupBox):
    def __init__(self, main, title="Presets"):
        super().__init__(title)

        self.main = main
        layout = QVBoxLayout()
        self.setLayout(layout)

        # file path
        self.path = "presets.json"
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({}, f)

        # ---- LOAD ----
        layout.addWidget(QLabel("Load preset"))

        row_load = QHBoxLayout()
        for i in range(1, 5):
            b = QPushButton(str(i))
            b.clicked.connect(self.make_load_handler(i))
            row_load.addWidget(b)
        layout.addLayout(row_load)

        # ---- SAVE ----
        layout.addWidget(QLabel("Save preset"))

        row_save = QHBoxLayout()
        for i in range(1, 5):
            b = QPushButton(str(i))
            b.clicked.connect(self.make_save_handler(i))
            row_save.addWidget(b)
        layout.addLayout(row_save)

        # ---- RENDER MODE ----
        layout.addWidget(QLabel("Render mode (Sum)"))

        row_mode = QHBoxLayout()
        self.mode_btns = {}
        for mode, label in [("wave", "Waveform"), ("dot", "XY dot")]:
            b = QPushButton(label)
            b.setCheckable(True)
            b.clicked.connect(self.make_mode_handler(mode))
            row_mode.addWidget(b)
            self.mode_btns[mode] = b
        layout.addLayout(row_mode)

        layout.addStretch()
        self.refresh_mode_buttons()

    # ===========================
    #   UTILITY
    # ===========================
    def load_json(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_json(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    # ===========================
    #   HANDLER MAKERS (fix lambda)
    # ===========================
    def make_load_handler(self, n):
        return lambda: self.load_preset(n)

    def make_save_handler(self, n):
        return lambda: self.save_preset(n)

    def make_mode_handler(self, mode):
        return lambda: self.set_render_mode(mode)

    # ===========================
    #   SAVE
    # ===========================
    def save_preset(self, n):
        data = self.load_json()

        data[str(n)] = {
            "A1": self.main.wave.A[1],
            "F1": self.main.wave.F[1],
            "W1": self.main.wave.W[1],
            "A2": self.main.wave.A[2],
            "F2": self.main.wave.F[2],
            "W2": self.main.wave.W[2],
            "mode": getattr(self.main.scope_sum, "mode", "wave"),
        }

        self.save_json(data)

    # ===========================
    #   LOAD
    # ===========================
    def load_preset(self, n):
        data = self.load_json()

        if str(n) not in data:
            # ---- DEFAULTS ----
            self.main.wave.A[1] = 1.0
            self.main.wave.F[1] = 3000
            self.main.wave.W[1] = "sin"

            self.main.wave.A[2] = 1.0
            self.main.wave.F[2] = 3400
            self.main.wave.W[2] = "sin"

            self.main.ctrl1.refresh_ui()
            self.main.ctrl2.refresh_ui()
            self.set_render_mode("wave")
            return

        # ---- LOAD EXISTING ----
        p = data[str(n)]

        self.main.wave.A[1] = p["A1"]
        self.main.wave.F[1] = p["F1"]
        self.main.wave.W[1] = p["W1"]

        self.main.wave.A[2] = p["A2"]
        self.main.wave.F[2] = p["F2"]
        self.main.wave.W[2] = p["W2"]

        self.main.ctrl1.refresh_ui()
        self.main.ctrl2.refresh_ui()

        # optional render mode
        self.set_render_mode(p.get("mode", "wave"))

    # ===========================
    #   RENDER MODE
    # ===========================
    def set_render_mode(self, mode):
        if mode not in ("wave", "dot"):
            return
        self.main.scope_sum.set_mode(mode)
        self.refresh_mode_buttons()

    def refresh_mode_buttons(self):
        current = getattr(self.main.scope_sum, "mode", "wave")
        for mode, btn in self.mode_btns.items():
            btn.setChecked(mode == current)
