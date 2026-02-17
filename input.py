import serial
import keyboard
import time

PORT = 'COM3'

ser = serial.Serial(PORT, 9600)
time.sleep(2)

print("Controls: A left | D right | S center")

while True:
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

