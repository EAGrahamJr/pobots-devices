#!/bin/env python3

import time
import board
from micropython import const
from adafruit_seesaw.seesaw import Seesaw

BUTTON_X = const(6)
BUTTON_Y = const(2)
BUTTON_A = const(5)
BUTTON_B = const(1)
BUTTON_SELECT = const(0)
BUTTON_START = const(16)
button_mask = const(
    (1 << BUTTON_X)
    | (1 << BUTTON_Y)
    | (1 << BUTTON_A)
    | (1 << BUTTON_B)
    | (1 << BUTTON_SELECT)
    | (1 << BUTTON_START)
)

# i2c_bus = board.STEMMA_I2C()  # The built-in STEMMA QT connector on the microcontroller
i2c_bus = board.I2C()  # Uses board.SCL and board.SDA. Use with breadboard.

count = 0
for i in range(0, 100):
    try:
        seesaw = Seesaw(i2c_bus, addr=0x50)
        print(f"Connected to seesaw after {i} tries.")
        break
    except:
        count = count + 1
        time.sleep(0.1)
else:
    print(f"Failed to connect to seesaw after {i} tries.")
    exit(1)

seesaw.pin_mode_bulk(button_mask, seesaw.INPUT_PULLUP)

last_x = 0
last_y = 0

last_start = False

while not last_start:
    x = 1023 - seesaw.analog_read(14)
    y = 1023 - seesaw.analog_read(15)

    if (abs(x - last_x) > 5) or (abs(y - last_y) > 5):
        print(x, y)
        last_x = x
        last_y = y

    buttons = seesaw.digital_read_bulk(button_mask)

    if not buttons & (1 << BUTTON_X):
        print("Button X pressed")

    if not buttons & (1 << BUTTON_Y):
        print("Button Y pressed")

    if not buttons & (1 << BUTTON_A):
        print("Button A pressed")

    if not buttons & (1 << BUTTON_B):
        print("Button B pressed")

    if not buttons & (1 << BUTTON_SELECT):
        print("Button Select pressed")

    if not buttons & (1 << BUTTON_START):
        print("Button Start pressed")
        last_start = True

    time.sleep(0.1)
