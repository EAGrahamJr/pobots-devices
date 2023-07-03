from adafruit_motor import stepper as sp
from adafruit_motor.stepper import StepperMotor
from adafruit_motor.servo import Servo
from time import sleep

_DEFAULT_RATE = 0.01


def move_servo(servo: Servo, angle: int, delta: int = 1, rate: float = _DEFAULT_RATE):
    """Move a servo to a certain angle by "stepping" by delta degrees with a pause of rate seconds between steps.

    Args:
        servo (Servo): the servo
        angle (float): where to move to
        delta (float): how many degrees to step by. Default is 1.
        rate (float): pause between steps in seconds or fractions thereof. Default is .02 seconds (20 miliiseconds). If None or <= 0, no pausing.
    """
    if rate is None or rate <= 0:
        servo.angle = angle
        return

    current = int(servo.angle)
    if angle > current:
        d = delta
    else:
        d = -delta

    for i in range(current, angle, d):
        servo.angle = i
        sleep(rate)

    servo.angle = angle


def move_stepper(
    stepper: StepperMotor,
    angle: float,
    rate: float = _DEFAULT_RATE,
    steps_per_rev: int = 200,
    gear_ratio: float = 1.0,
):
    """Move a stepper to a certain angle by "stepping" by delta degrees with a pause of rate seconds between steps.

    NOTE: This does not use microstepping.

    Args:
        stepper (StepperMotor): the stepper
        angle (float): where to move to
        rate (float): pause between steps in seconds or fractions thereof. Default is .02 seconds (20 miliiseconds). If None or <= 0, no pausing.
        steps_per_rev (int): number of steps per revolution. Default is 200.
        gear_ratio (float): gear ratio. Default is 1.0.
    """
    steps = steps_per_rev * gear_ratio * angle / 360
    if steps < 0:
        direction = sp.BACKWARD
    else:
        direction = sp.FORWARD
    steps = abs(steps)

    for i in range(int(steps)):
        stepper.onestep(direction=direction)
        sleep(rate)
