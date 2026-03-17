import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import board
import time
from umodbus.serial import Serial as ModbusRTUMaster

baudrates = [9600, 4800]
slave_ids = range(1, 10)

def scan_modbus():

    host = None
    found_devices = []

    for baud in baudrates:

        print(f"\nTesting Baudrate: {baud}")

        if host is not None:
            try:
                host._uart.deinit()
                print("Previous UART deinitialized")
            except:
                pass

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

                time.sleep(0.1)

            except Exception as e:
                print(f"    No response ({e})")

            time.sleep(0.05)

    print("\n===== SCAN COMPLETE =====")

    if found_devices:
        for b, s in found_devices:
            print(f"Device found → Baudrate: {b}, Slave ID: {s}")
    else:
        print("No devices found")

    print("=========================\n")


scan_modbus()
