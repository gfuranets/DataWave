import serial
import time
import keyboard

ser = serial.Serial("COM3", 9600, timeout = 1)
time.sleep(2) # IMPORTANT: wait for Arduino reset
print("Controls: A left | D right | S center")

while True:
    # Data reading
    line = serial.readline().decode(errors = 'ignore').strip()

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
        serial.write(b'A')
        print("Sent: A (left)")
        time.sleep(0.1)

    if keyboard.is_pressed('d'):
        serial.write(b'D')
        print("Sent: D (right)")
        time.sleep(0.1)

    if keyboard.is_pressed('s'):
        serial.write(b'S')
        print("Sent: S (center)")
        time.sleep(0.1)


    line = ser.readline().decode(errors = 'ignore').strip()
    
    if not line:
        continue

    # print("RAW:", line)

    values = line.split(",")

    if len(values) == 6:
        try:
            t, p, h, x, y, z = map(float, values)
            print(t, p, h, x, y, z)
        except:
            print("Bad data:", line)
