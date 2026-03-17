import sys
import os
import time

# Detect platform
MICROPYTHON = False

try:
    import board
    import busio
    MICROPYTHON = True
except:
    pass

# -------------------------
# CONFIGURATION
# -------------------------

baudrates = [9600, 4800]
slave_ids = range(1, 10)

# -------------------------
# MODBUS SCAN FUNCTION
# -------------------------

def scan_modbus():

    found_devices = []

    # =========================
    # MICROCONTROLLER MODE
    # =========================
    if MICROPYTHON:
        from umodbus.serial import Serial as ModbusRTUMaster

        for baud in baudrates:

            print(f"\nTesting Baudrate: {baud}")

            host = ModbusRTUMaster(
                tx_pin=board.TX,
                rx_pin=board.RX,
                baudrate=baud
            )

            for slave in slave_ids:

                try:
                    print(f"  Trying Slave ID: {slave}")

                    data = host.read_holding_registers(
                        slave_addr=slave,
                        starting_addr=0,
                        register_qty=1,
                        signed=False
                    )

                    print("\n=== DEVICE FOUND ===")
                    print(f"Baudrate : {baud}")
                    print(f"Slave ID : {slave}")
                    print(f"Data     : {data}")
                    print("====================\n")

                    found_devices.append((baud, slave))

                except Exception:
                    print("    No response")

                time.sleep(0.05)

    # =========================
    # RASPBERRY PI MODE
    # =========================
    else:
        import serial
        from umodbus.serial import Serial as ModbusRTUMaster

        PORT = "/dev/ttyACM0"

        for baud in baudrates:

            print(f"\nTesting Baudrate: {baud}")

            try:
                host = ModbusRTUMaster(
                    port=PORT,
                    baudrate=baud
                )
            except Exception as e:
                print("Serial init error:", e)
                continue

            for slave in slave_ids:

                try:
                    print(f"  Trying Slave ID: {slave}")

                    data = host.read_holding_registers(
                        slave_addr=slave,
                        starting_addr=0,
                        register_qty=1,
                        signed=False
                    )

                    print("\n=== DEVICE FOUND ===")
                    print(f"Baudrate : {baud}")
                    print(f"Slave ID : {slave}")
                    print(f"Data     : {data}")
                    print("====================\n")

                    found_devices.append((baud, slave))

                except Exception:
                    print("    No response")

                time.sleep(0.05)

    # =========================
    # RESULT SUMMARY
    # =========================

    print("\n===== SCAN COMPLETE =====")

    if found_devices:
        for b, s in found_devices:
            print(f"Device found → Baudrate: {b}, Slave ID: {s}")
    else:
        print("No devices found")

    print("=========================\n")


# Run
scan_modbus()
