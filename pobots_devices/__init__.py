from adafruit_crickit import crickit
from adafruit_motor.stepper import StepperMotor
from adafruit_motor.servo import Servo
from time import sleep

_DEFAULT_RATE = .02

def move_servo(servo, angle: int, delta:int = 1, rate: float = _DEFAULT_RATE):
    """Move a servo to a certain angle by "stepping" by delta degrees with a pause of rate seconds between steps.

    Args:
        servo (Servo): the servo
        angle (float): where to move to
        delta (float): how many degrees to step by (default 1.0)
        rate (float): pause between steps in seconds or fractions thereof
    """
    current = int(servo.angle)
    if angle > current:
        d = delta
    else:
        d = -delta

    for i in range(current, angle, d):
        servo.angle = i
        sleep(rate)

    servo.angle = angle

class RotatorServo:
    def __init__(self, servo:Servo) -> None:
        self._servo = servo

    @property
    def angle(self) -> float:
        return self._servo.angle

    @angle.setter
    def angle(self, angle: float) -> None:
        move_servo(self._servo, int(angle))

class Rotators:
    def __init__(self) -> None:
        pass

    @staticmethod
    def servo(port: int) -> RotatorServo:

        if port == 1:
            s = crickit.servo_1
        elif port == 2:
            s = crickit.servo_2
        elif port == 3:
            s = crickit.servo_3
        elif port == 4:
            s = crickit.servo_4
        else:
            raise ValueError("Invalid servo port")
        return RotatorServo(s)

    @staticmethod
    def xxg90(port: int, start_angle = 0) -> RotatorServo:
        """Create a RotatorServo for an SG90 or MG90 servo on the specified port.

        This sets the putlse width range to 500-2400, which is the range for the SG90 and MG90 servos.

        param port: the port number (1-4)
        """
        if port == 1:
            s = crickit.servo_1
        elif port == 2:
            s = crickit.servo_2
        elif port == 3:
            s = crickit.servo_3
        elif port == 4:
            s = crickit.servo_4
        else:
            raise ValueError("Invalid servo port")
        if s.angle == None:
            s.set_pulse_width_range(min_pulse=500, max_pulse=2400)
            s.angle = start_angle

        return RotatorServo(s)