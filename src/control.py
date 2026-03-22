import serial
import time
import keyboard

ser = serial.Serial("COM3", 9600, timeout = 1)
time.sleep(2) # IMPORTANT: wait for Arduino reset
print("Controls: A left | D right | S center")

def control():
    while True:
        # Data reading
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

        # ----------------------------------------------------------

        # Controls
        if keyboard.is_pressed('a'):
            ser.write(b'A')
            print("Sent: A (left)")
            time.sleep(0.1)

        if keyboard.is_pressed('d'):
            ser.write(b'D')
            print("Sent: D (right)")
            time.sleep(0.1)

        if keyboard.is_pressed('s'):
            ser.write(b'S')
            print("Sent: S (center)")
            time.sleep(0.1)
