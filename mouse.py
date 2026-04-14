from pynput.mouse import Controller
import serial
import time

ser = serial.Serial("COM3", 9600, timeout = 1)
mouse = Controller()
x, y = mouse.position

while True:
    x_curr, y_curr = mouse.position

    dx = x_curr - x
    dy = y_curr - y
    # print(dx, dy)

    x, y = x_curr, y_curr   

    ser.write(f"{dx},{dy}\n".encode())
    print(ser.readline())
    time.sleep(0.1)
