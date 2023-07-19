#!/bin/env python3

from adafruit_crickit import crickit
from adafruit_motor import stepper
from time import sleep

m = crickit.stepper_motor

steps_per_rev = 200 / 1.11
steps_per_degree = steps_per_rev / 360
degree_per_temp = 18

# move 5 degrees of temp
a = int(5 * degree_per_temp * steps_per_degree)
print(f"Moving {a} steps")
for i in range(a):
    m.onestep(direction=stepper.FORWARD)
    sleep(0.01)
m.release()
