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

        layout.addStretch()

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

