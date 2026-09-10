"""
Datasheet Generator for PCB Component & Circuit Troubleshooting Assistant.
Generates 6 official manufacturer-style specification sheets in data/datasheets/.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASHEETS_DIR = os.path.join(BASE_DIR, "data", "datasheets")
os.makedirs(DATASHEETS_DIR, exist_ok=True)

def create_pdf(filename, title, subtitle, pages_content):
    pdf_path = os.path.join(DATASHEETS_DIR, filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        fontName='Helvetica-Bold'
    )
    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#059669'),
        fontName='Helvetica-Bold'
    )
    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1e293b'),
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica'
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica',
        leftIndent=15
    )

    elements = []

    for page_idx, sections in enumerate(pages_content):
        if page_idx > 0:
            elements.append(PageBreak())

        elements.append(Paragraph(title, title_style))
        elements.append(Paragraph(f"{subtitle} | Page {page_idx + 1}", sub_style))
        elements.append(Spacer(1, 10))

        for sec in sections:
            elements.append(Paragraph(sec["heading"], h2_style))
            elements.append(Spacer(1, 4))
            for item in sec["items"]:
                if isinstance(item, str):
                    elements.append(Paragraph(item, body_style))
                    elements.append(Spacer(1, 4))
                elif isinstance(item, list):
                    # Table data
                    table = Table(item, colWidths=[120, 180, 200])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f766e')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                        ('TOPPADDING', (0, 0), (-1, 0), 5),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f1f5f9')])
                    ]))
                    elements.append(table)
                    elements.append(Spacer(1, 8))

    doc.build(elements)
    print(f"Generated datasheet: {filename}")

def build_all():
    # 1. LM7805
    lm7805_pages = [
        [
            {
                "heading": "1. Device Overview & Absolute Maximum Ratings",
                "items": [
                    "The LM7805 is a 3-terminal monolithic positive voltage regulator designed for local, on-card regulation. Features internal current limiting, thermal shutdown protection, and safe operating area protection.",
                    [
                        ["Parameter", "Symbol / Rating", "Recommended Operating Value"],
                        ["Input Voltage Range", "VI = 7.0V to 35.0V", "Optimal Vin = 7.5V to 12.0V"],
                        ["Output Voltage", "VO = 5.0V (+-4%)", "4.8V min, 5.2V max at 1A"],
                        ["Maximum Output Current", "IO = 1.5A (with heatsink)", "0.5A continuous without heatsink"],
                        ["Operating Temperature", "TJ = 0°C to 125°C", "Thermal shutdown at TJ > 150°C"],
                        ["Dropout Voltage", "VD = 2.0V typical", "Vin must exceed Vout by >= 2.0V"]
                    ],
                    "Note: If input voltage drops below 7.0V, the device falls out of regulation and output drops below 5.0V."
                ]
            },
            {
                "heading": "2. Pinout Configuration (TO-220 & TO-92 Packages)",
                "items": [
                    "Looking at the front of the TO-220 package (metal tab facing backward):",
                    "• Pin 1 (INPUT): Unregulated DC input from power supply or battery (+7V to +35V DC).",
                    "• Pin 2 (GROUND): Common circuit ground. Connected internally to the metallic mounting tab/heatsink.",
                    "• Pin 3 (OUTPUT): Regulated +5.0V DC output rail.",
                    "Thermal Warning: Because Pin 2 is connected to the heatsink tab, connecting the tab to an external chassis will tie that chassis directly to electrical ground."
                ]
            }
        ],
        [
            {
                "heading": "3. Mandatory Bypass Capacitors & Typical Application Circuit",
                "items": [
                    "Bypass capacitors are required to suppress high-frequency oscillations and handle rapid load transients:",
                    "• Input Capacitor (Cin): 0.33 uF ceramic capacitor placed within 2 cm of Pin 1 to counteract input lead inductance.",
                    "• Output Capacitor (Cout): 0.1 uF ceramic capacitor on Pin 3 to improve transient response and phase margin.",
                    "• Bulk Filter Capacitor: When powered from an AC rectified supply, place a 1000 uF electrolytic capacitor upstream of Cin."
                ]
            },
            {
                "heading": "4. Troubleshooting & Thermal Failure Modes",
                "items": [
                    "• Problem 1: Regulator is boiling hot and output drops to ~1.2V.\nCause: Thermal Overload Shutdown. Power dissipation P = (Vin - Vout) * Iload. For 12V input at 0.5A, P = (12 - 5) * 0.5 = 3.5 Watts. Without a heatsink, the junction temperature exceeds 150°C in seconds. Solution: Add extruded aluminum heatsink or lower input voltage to 7.5V.",
                    "• Problem 2: Output measures 5.0V on multimeter, but microcontroller resets randomly.\nCause: High frequency oscillation. The multimeter averages the voltage, but Cin or Cout is missing, causing 200 mV oscillation spikes. Solution: Solder 0.1 uF ceramic capacitors directly adjacent to the regulator pins.",
                    "• Problem 3: Output voltage is 0V.\nCause: Reverse polarity on Pin 1, short circuit between Pin 3 and Ground, or input voltage under 7.0V."
                ]
            }
        ]
    ]
    create_pdf("LM7805_Voltage_Regulator_Datasheet.pdf", "LM7805 3-Terminal 5V Regulator", "Texas Instruments Specification", lm7805_pages)

    # 2. NE555 Timer
    ne555_pages = [
        [
            {
                "heading": "1. Technical Specifications & Functional Blocks",
                "items": [
                    "The NE555 is a precision timing circuit capable of producing accurate time delays or oscillation. In the time-delay (monostable) mode, the timed interval is controlled by a single external resistor and capacitor network.",
                    [
                        ["Specification", "Standard Limit", "Notes"],
                        ["Supply Voltage (VCC)", "4.5V to 16.0V DC", "Functional down to 4.5V; nominal 5V to 12V"],
                        ["Max Output Current", "200 mA (Source / Sink)", "Can drive relays and LEDs directly"],
                        ["Timing Range", "Microseconds to Hours", "Determined by external RC values"],
                        ["Threshold Voltage", "2/3 * VCC", "Resets internal flip-flop"],
                        ["Trigger Voltage", "1/3 * VCC", "Sets internal flip-flop (active low)"]
                    ]
                ]
            },
            {
                "heading": "2. Pinout Configuration (8-Pin DIP & SOIC)",
                "items": [
                    "• Pin 1 (GND): Ground reference (0V).",
                    "• Pin 2 (TRIG): Trigger input. When voltage drops below 1/3 VCC, comparator sets flip-flop and output goes HIGH.",
                    "• Pin 3 (OUT): Output pin. High state delivers VCC - 1.5V; low state pulls to GND + 0.1V.",
                    "• Pin 4 (RESET): Active-low master reset. Connect to VCC for normal operation. If left floating, noise triggers false resets.",
                    "• Pin 5 (CTRL): Control voltage access. Directly biases internal 2/3 VCC divider. Must connect 10 nF capacitor to GND for noise immunity.",
                    "• Pin 6 (THRES): Threshold input. When voltage rises above 2/3 VCC, comparator resets flip-flop and output goes LOW.",
                    "• Pin 7 (DISCH): Open-collector discharge pin. Discharges timing capacitor to ground in tandem with output state.",
                    "• Pin 8 (VCC): Positive DC supply voltage (+5V to +15V)."
                ]
            }
        ],
        [
            {
                "heading": "3. Astable Multivibrator (Oscillator) Design Formulas",
                "items": [
                    "In astable mode, the timer free-runs as a square wave generator with frequency:\nFrequency f = 1.44 / ((R1 + 2*R2) * C1)\nHigh Time T_high = 0.693 * (R1 + R2) * C1\nLow Time T_low = 0.693 * R2 * C1\nDuty Cycle D = (R1 + R2) / (R1 + 2*R2)",
                    "Design Rule: R1 must be at least 1 kOhm to prevent shorting VCC to ground during the discharge cycle through Pin 7."
                ]
            },
            {
                "heading": "4. Troubleshooting & Circuit Diagnostics",
                "items": [
                    "• Symptom 1: Timer does not oscillate; output remains stuck HIGH.\nInspection: Check Pin 4 (RESET). If Pin 4 is floating or below 0.7V, the timer is held in reset. Check Pin 6 (Threshold); if voltage cannot reach 2/3 VCC due to capacitor leakage, output will never reset.",
                    "• Symptom 2: Severe supply rail noise whenever output switches.\nCause: Large 'crowbar' current spike (up to 400 mA) occurs internally when output totem-pole switches states. Solution: Solder a 0.1 uF ceramic cap in parallel with a 10 uF tantalum cap between Pin 8 and Pin 1.",
                    "• Symptom 3: Erratic timing intervals under motor or relay loads.\nSolution: Add 10 nF capacitor from Pin 5 to GND to stabilize comparator reference voltage."
                ]
            }
        ]
    ]
    create_pdf("NE555_Precision_Timer_Datasheet.pdf", "NE555 Precision Timer IC", "Texas Instruments Specification", ne555_pages)

    # 3. ATmega328P
    atmega_pages = [
        [
            {
                "heading": "1. Architecture Overview & Operating Characteristics",
                "items": [
                    "The ATmega328P is a low-power CMOS 8-bit microcontroller based on the AVR enhanced RISC architecture. Executes 1 instruction per clock cycle, achieving throughputs approaching 1 MIPS per MHz.",
                    [
                        ["Parameter", "Operating Range", "Critical Engineering Constraint"],
                        ["Operating Voltage", "1.8V to 5.5V DC", "5.0V required for 16 MHz / 20 MHz clock"],
                        ["Flash Program Memory", "32 KB (with 0.5 KB Bootloader)", "10,000 write/erase endurance cycles"],
                        ["SRAM Data Memory", "2 KB internal", "Stack overflow occurs if RAM fills"],
                        ["Max DC Current per I/O", "40.0 mA absolute max", "Recommended <= 20.0 mA per pin"],
                        ["Max DC Current VCC/GND", "200.0 mA total device limit", "Sum of all pin currents must not exceed 200mA"]
                    ]
                ]
            },
            {
                "heading": "2. Primary Pinouts & Bus Interfaces (DIP-28 Package)",
                "items": [
                    "• Pin 1 (PC6 / RESET): Active-low reset. Must have external 10 kOhm pullup resistor to VCC. Pull to GND to reset MCU.",
                    "• Pin 7 (VCC) & Pin 8 (GND): Main digital power supply. Requires 0.1 uF decoupling capacitor directly adjacent.",
                    "• Pin 9 (XTAL1) & Pin 10 (XTAL2): Inverting oscillator amplifier pins. Connect 16 MHz crystal with twin 22 pF ceramic caps to GND.",
                    "• Pin 20 (AVCC): Power supply for Port A and Analog-to-Digital Converter. Must connect to VCC via low-pass LC filter (10 uH + 100 nF).",
                    "• Pin 21 (AREF): Analog reference voltage pin. Connect 100 nF capacitor to GND. Never tie directly to external 5V if internal 1.1V ref is active!",
                    "• Pin 27 (PC4 / SDA) & Pin 28 (PC5 / SCL): Hardware I2C bus. Requires external 4.7 kOhm pullup resistors on both lines.",
                    "• Pin 17 (MOSI), Pin 18 (MISO), Pin 19 (SCK): Hardware SPI bus used for high-speed communication and ICSP programming."
                ]
            }
        ],
        [
            {
                "heading": "3. Analog-to-Digital Converter (ADC) Guidelines",
                "items": [
                    "The ATmega328P includes a 10-bit successive approximation ADC with 6 multiplexed channels (Port C, ADC0 to ADC5).",
                    "ADC Clock Requirement: The ADC requires an input clock frequency between 50 kHz and 200 kHz for maximum 10-bit resolution. With a 16 MHz system clock, configure the ADC prescaler to 128 (16 MHz / 128 = 125 kHz).",
                    "Input Impedance: The ADC is optimized for analog signals with an output impedance of 10 kOhm or less. If source impedance is high, add a 10 nF capacitor to ground or buffer with an op-amp."
                ]
            },
            {
                "heading": "4. Troubleshooting Common Hardware Faults",
                "items": [
                    "• Fault 1: AVR programmer reports 'Device signature = 0x000000' or 'Target not responding'.\nCauses: Crystal clock is not oscillating (missing 22 pF caps), RESET pin is not pulled HIGH, or SPI MOSI/MISO connections are swapped. Solution: Verify 5V on Pin 7, verify 10 kOhm on Pin 1, check crystal.",
                    "• Fault 2: Microcontroller resets spontaneously when relay or motor turns on.\nCause: Inductive voltage dip on VCC triggering internal Brown-Out Detector (BOD). Solution: Add a 470 uF electrolytic capacitor across the main power rails and install a flyback diode on the relay coil.",
                    "• Fault 3: ADC readings fluctuate wildly.\nCause: AVCC (Pin 20) left disconnected or AREF (Pin 21) floating without decoupling cap. Solution: Connect AVCC to VCC and decouple AREF with 100 nF."
                ]
            }
        ]
    ]
    create_pdf("ATmega328P_Microcontroller_Datasheet.pdf", "ATmega328P 8-Bit AVR Microcontroller", "Microchip Technology Specification", atmega_pages)

    # 4. ESP32-WROOM-32
    esp32_pages = [
        [
            {
                "heading": "1. Electrical Characteristics & RF Power Specifications",
                "items": [
                    "ESP32-WROOM-32 is a powerful, generic Wi-Fi + Bluetooth + BLE MCU module powered by the dual-core Tensilica Xtensa 32-bit LX6 microprocessor operating up to 240 MHz.",
                    [
                        ["Parameter", "Specification", "Engineering Note"],
                        ["Operating Voltage (VDD)", "3.0V to 3.6V DC", "STRICT: Applying 5.0V destroys the chip!"],
                        ["Peak Power Supply Current", "500 mA minimum capability", "Wi-Fi TX bursts draw up to 450 mA"],
                        ["Digital I/O Voltage", "3.3V LVTTL logic", "Inputs are NOT 5V tolerant"],
                        ["Deep-Sleep Current", "5 uA to 15 uA", "Optimal for ultra-low power IoT sensors"],
                        ["Operating Frequency", "Up to 240 MHz (600 DMIPS)", "Internal 520 KB SRAM + 4 MB Flash"]
                    ]
                ]
            },
            {
                "heading": "2. Critical Strapping Pins & Boot Modes",
                "items": [
                    "The ESP32 module has 5 strapping pins that configure the chip state at power-up / reset. Incorrect external pullups will cause boot failures:",
                    "• GPIO0: Boot Mode Selection. During reset, pull HIGH for normal SPI Flash boot. Pull LOW to enter UART Download/Flashing mode.",
                    "• GPIO2: Flashing constraint. Must be left floating or pulled LOW during flashing. Connected to onboard LED on many dev boards.",
                    "• GPIO12 (MTDI): Flash Voltage Selection. Must be LOW at boot to configure internal flash LDO to 3.3V. If pulled HIGH, flash is overvolted to 1.8V and chip panics.",
                    "• GPIO15 (MTDO): Debug log output. Must be pulled HIGH to enable silent boot; LOW outputs debug ROM messages.",
                    "• EN (CHIP_PU): Enable pin. Must have 10 kOhm pullup to 3V3 and 1 uF capacitor to GND to delay boot until power rail stabilizes."
                ]
            }
        ],
        [
            {
                "heading": "3. Power Supply Design & Decoupling Recommendations",
                "items": [
                    "Wi-Fi Transmission Demands: When the 2.4 GHz RF power amplifier activates, current jumps from 30 mA to 450 mA within 10 nanoseconds. Standard USB-to-UART bridge LDOs (e.g. AMS1117-3.3) fail if decoupling is inadequate.",
                    "Mandatory Decoupling Architecture:",
                    "• 1x 10 uF low-ESR ceramic or tantalum capacitor located immediately adjacent to the VDD pin.",
                    "• 2x 0.1 uF ceramic capacitors in parallel for high-frequency attenuation.",
                    "• Total power rail impedance must be less than 0.2 Ohms to prevent voltage sag below 2.8V."
                ]
            },
            {
                "heading": "4. Troubleshooting Diagnostic Guide",
                "items": [
                    "• Error: 'Brownout detector was triggered at core 0 / 1'.\nCause: The 3.3V power supply collapsed below 2.8V during Wi-Fi connection handshake. Solution: Use dedicated 3.3V regulator rated for >= 800 mA (e.g., AP2112K or LM1117-3.3) with large 470 uF bulk capacitor.",
                    "• Error: 'A fatal error occurred: Failed to connect to ESP32: Timed out waiting for packet header'.\nCause: GPIO0 is not held LOW during bootloader synchronization, or EN capacitor is missing. Solution: Hold BOOT button (pulls GPIO0 low) while pressing and releasing EN (Reset).",
                    "• Error: GPIO input reading false positives or ghost triggers.\nCause: Floating inputs. ESP32 internal pullups are relatively weak (~50 kOhm). Solution: Add external 10 kOhm pullup or pulldown resistors on sensor lines."
                ]
            }
        ]
    ]
    create_pdf("ESP32_WROOM_32_Datasheet.pdf", "ESP32-WROOM-32 Wi-Fi & BLE MCU", "Espressif Systems Specification", esp32_pages)

    # 5. L298N Motor Driver
    l298n_pages = [
        [
            {
                "heading": "1. Device Overview & Maximum Ratings",
                "items": [
                    "The L298N is an integrated monolithic circuit in a 15-lead Multiwatt package. It is a high voltage, high current dual full-bridge driver designed to accept standard TTL logic levels and drive inductive loads such as relays, solenoids, DC motors, and stepper motors.",
                    [
                        ["Parameter", "Rating Value", "Operating Condition"],
                        ["Motor Supply Voltage (Vs)", "Up to 46.0V DC", "Minimum Vs = 4.5V; typical 12V to 24V"],
                        ["Logic Supply Voltage (Vss)", "4.5V to 7.0V DC", "Nominal 5.0V for internal logic gates"],
                        ["Peak Output Current (per channel)", "3.0A (non-repetitive)", "Pulse duration t <= 100 us"],
                        ["Continuous Output Current", "2.0A per channel", "Total continuous 4A with proper heatsink"],
                        ["Input Logic High (VIH)", "2.3V to Vss", "Compatible with 3.3V and 5V microcontrollers"]
                    ]
                ]
            },
            {
                "heading": "2. Pinout & H-Bridge Control Logic (Multiwatt 15)",
                "items": [
                    "• Pin 4 (Vs): Motor power supply (+12V to +35V DC).",
                    "• Pin 9 (Vss): Logic power supply (+5V DC).",
                    "• Pin 8 (GND): Common circuit ground. Must be connected to microcontroller ground!",
                    "• Pin 5 (IN1) & Pin 7 (IN2): Bridge A direction inputs. IN1=HIGH, IN2=LOW drives Forward; IN1=LOW, IN2=HIGH drives Reverse; IN1=IN2 stops motor.",
                    "• Pin 6 (ENA): Bridge A Enable input. Apply PWM signal (0-100% duty cycle) to regulate motor speed.",
                    "• Pin 2 (OUT1) & Pin 3 (OUT2): Bridge A outputs connected to Motor A terminals.",
                    "• Pin 10 (IN3), Pin 12 (IN4), Pin 11 (ENB), Pin 13 (OUT3), Pin 14 (OUT4): Bridge B controls for Motor B.",
                    "• Pin 1 & Pin 15 (Current Sensing A & B): Connect to GND directly, or via 0.5 Ohm sense resistors for current monitoring."
                ]
            }
        ],
        [
            {
                "heading": "3. Inductive Spike Protection (Flyback Diodes)",
                "items": [
                    "CRITICAL PROTECTION REQUIREMENT: DC motors generate extreme inductive back-EMF voltage spikes (exceeding 100V) when commutating or stopping. The internal bipolar transistors of the L298N do NOT have internal suppression diodes.",
                    "• Each output pin (OUT1, OUT2, OUT3, OUT4) MUST be clamped to Vs and GND using 8 external fast-recovery diodes.",
                    "• Recommended Diode: 1N5819 Schottky diode or 1N4937 fast recovery diode (trr < 200 ns). Do NOT use standard 1N4007 rectifier diodes as their slow reverse recovery time will damage the L298N."
                ]
            },
            {
                "heading": "4. Troubleshooting & Thermal Diagnostics",
                "items": [
                    "• Issue 1: Motor driver smokes or heats up to > 100°C within seconds.\nCause: Bipolar transistor saturation loss. The L298N has an internal Vce saturation drop of ~2.0V to 3.0V. At 2A load, internal power dissipation is P = 2.5V * 2A = 5 Watts! Solution: A large aluminum heatsink with thermal paste is mandatory for currents above 0.8A.",
                    "• Issue 2: Motor does not turn, but logic LEDs light up.\nCause: Vs (Pin 4) disconnected or Enable jumper missing. If ENA (Pin 6) is left floating, Bridge A is disabled. Solution: Tie ENA to Vss or apply PWM.",
                    "• Issue 3: Microcontroller crashes or reboots when motor reverses direction.\nCause: Ground loop noise or motor inductive back-EMF resetting the MCU. Solution: Separate motor power supply from logic supply and connect grounds at a single star-ground point."
                ]
            }
        ]
    ]
    create_pdf("L298N_Dual_Motor_Driver_Datasheet.pdf", "L298N Dual Full-Bridge Driver", "STMicroelectronics Specification", l298n_pages)

    # 6. Passive Components Guide
    passives_pages = [
        [
            {
                "heading": "1. Capacitor Types, Polarity & Decoupling Practices",
                "items": [
                    "Capacitors store electrical energy electrostatically and filter noise on circuit supply rails.",
                    [
                        ["Capacitor Type", "Typical Values", "Polarity & Typical Usage"],
                        ["Electrolytic (Aluminum)", "1 uF to 4700 uF", "POLARIZED. Long lead is (+), stripe is (-). Bulk power filtering."],
                        ["Ceramic (Multilayer MLCC)", "10 pF to 10 uF", "NON-POLARIZED. Symmetrical. High-frequency noise bypass."],
                        ["Tantalum", "0.1 uF to 220 uF", "POLARIZED. Highly sensitive to overvoltage. Low ESR bypass."],
                        ["Film (Polyester/Poly)", "1 nF to 1 uF", "NON-POLARIZED. Audio, timing filters, precision resonators."]
                    ],
                    "FATAL HAZARD: Reverse Polarity on Electrolytic Capacitors. Connecting negative voltage to the positive lead of an aluminum electrolytic capacitor initiates rapid electrolysis of the aluminum oxide dielectric, producing hydrogen gas, case rupture, and catastrophic explosion. Always verify polarity stripe before powering up!"
                ]
            },
            {
                "heading": "2. Resistor Color Codes & Power Derating",
                "items": [
                    "4-Band Resistor Decoding Rule:\n• Band 1 = 1st Significant Digit | Band 2 = 2nd Significant Digit | Band 3 = Multiplier (10^N) | Band 4 = Tolerance (Gold = +-5%, Silver = +-10%).\n• Color Values: Black(0), Brown(1), Red(2), Orange(3), Yellow(4), Green(5), Blue(6), Violet(7), Gray(8), White(9).",
                    "Example: Brown-Black-Red-Gold = 1 - 0 * 10^2 = 1,000 Ohms (1 kOhm) +-5%.",
                    "Power Dissipation Law: P = I^2 * R = V^2 / R. Standard axial resistors are rated for 0.25W (1/4 Watt). Derating guideline: Never operate a resistor above 60% of its rated wattage (e.g., maximum 0.15W on a 1/4W resistor) to prevent thermal degradation and resistance drift."
                ]
            }
        ],
        [
            {
                "heading": "3. Diodes & Semiconductor Protection Devices",
                "items": [
                    "• 1N4007 Standard Silicon Rectifier: Maximum Repetitive Reverse Voltage = 1000V, Forward Current = 1.0A. Forward Voltage Drop Vf = 0.7V. Primary use: 50/60 Hz AC line rectification and DC reverse-polarity protection.",
                    "• 1N4148 High-Speed Switching Diode: Reverse Recovery Time trr = 4 ns, Max Current = 200 mA. Primary use: High-speed digital logic, clipping, small signal detection.",
                    "• 1N5819 Schottky Barrier Diode: Forward Voltage Drop Vf = 0.35V at 1A, ultra-fast switching. Primary use: High-efficiency DC-DC buck converters and inductive flyback suppression.",
                    "• Zener Diodes (e.g. 1N4733A 5.1V): Operates in reverse breakdown region to clamp voltage. Must always use series current-limiting resistor to prevent thermal destruction."
                ]
            },
            {
                "heading": "4. Circuit Troubleshooting & Multimeter Testing Protocol",
                "items": [
                    "• Diode Mode Test: Red probe on Anode, Black probe on Cathode (side with silver stripe). Silicon diode reads ~0.5V to 0.7V. Schottky reads ~0.2V to 0.4V. Reverse bias should read 'OL' (Open Loop). If reading 0.00V in both directions, diode is shorted.",
                    "• In-Circuit Resistor Testing: Resistance measurements taken with power OFF. Note that parallel components in the circuit will cause the multimeter to read a LOWER resistance than the nominal value. To confirm an open resistor, desolder one lead.",
                    "• Blown Electrolytic Capacitor Signs: Bulging or domed aluminum top vent, brown electrolytic fluid crust around base, or high ESR causing excessive ripple on oscilloscope."
                ]
            }
        ]
    ]
    create_pdf("Passive_Components_Capacitors_Resistors_Guide.pdf", "PCB Passives: Capacitors, Resistors & Diodes", "IEEE Components Specification Guide", passives_pages)

if __name__ == "__main__":
    build_all()
    print("All 6 electronic component datasheets successfully generated.")
