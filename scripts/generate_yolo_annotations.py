import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANN_DIR = os.path.join(BASE_DIR, "data", "annotations")
os.makedirs(ANN_DIR, exist_ok=True)

# YOLO class mapping:
# 0: LM7805_Voltage_Regulator
# 1: NE555_Precision_Timer
# 2: ATmega328P_Microcontroller
# 3: ESP32_WROOM_32_MCU
# 4: L298N_Motor_Driver
# 5: Electrolytic_Capacitor
# 6: Ceramic_Capacitor
# 7: Resistor_Axial
# 8: Diode_Rectifier
# 9: Crystal_Oscillator

annotations = {
    "arduino_uno_atmega328p.txt": [
        "2 0.65 0.61 0.50 0.22",  # ATmega328P
        "5 0.36 0.74 0.20 0.16",  # Electrolytic Capacitor
        "9 0.34 0.47 0.15 0.11",  # 16MHz Crystal
        "0 0.20 0.60 0.12 0.15"   # Voltage Regulator
    ],
    "esp32_dev_board.txt": [
        "3 0.63 0.50 0.38 0.40",  # ESP32-WROOM-32
        "0 0.27 0.42 0.12 0.10",  # AMS1117 3.3V
        "6 0.35 0.48 0.08 0.12"   # Decoupling Caps
    ],
    "lm7805_power_supply.txt": [
        "0 0.46 0.57 0.23 0.25",  # LM7805 Regulator
        "5 0.25 0.61 0.16 0.38",  # 2200uF Filter Capacitor
        "8 0.37 0.40 0.05 0.12",  # 1N4007 Diode
        "7 0.49 0.73 0.08 0.16"   # Resistors
    ],
    "ne555_timer_board.txt": [
        "1 0.51 0.49 0.10 0.18",  # NE555 Timer IC
        "5 0.52 0.63 0.09 0.10",  # 10uF Capacitor
        "6 0.70 0.50 0.07 0.15"   # 103 Ceramic Cap
    ]
}

for fname, lines in annotations.items():
    p = os.path.join(ANN_DIR, fname)
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Saved YOLO annotation: {fname}")
