import serial
import time

ser = serial.Serial("COM3", 9600, timeout = 1)
time.sleep(2) # IMPORTANT: wait for Arduino reset

while True:
    line = ser.readline().decode(errors='ignore').strip()
    
    if not line:
        continue

    print("RAW:", line)

    values = line.split(",")

    if len(values) == 6:
        try:
            t, p, h, x, y, z = map(float, values)
            print("Parsed:", t, p, h, x, y, z)
        except:
            print("Bad data:", line)