from adafruit_crickit import crickit
from adafruit_motor.stepper import StepperMotor
from pobots_devices.rotator import *


class Servos:
    """Wraps the CRICKIT Hat servo ports.

    Assumes only one CRICKIT in the system.
    """

    @staticmethod
    def ___servo(port: int) -> Servo:
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
        return s

    @staticmethod
    def servo(
        port: int, start_angle: float = 0, pulse_width_range: PulseWidthRange = None
    ) -> RotatorServo:
        """Create a RotatorServo on the given CRICKIT servo port.

        Args:
            port (int): which servo port to use (1-4)
            start_angle (float, optional): sets the initial angle of the servo. Defaults to 0.
            pulse_width_range (PulseWidthRange, optional): sets the pulse-width for the servo. Defaults to None.

        Returns:
            RotatorServo: A "steppable" servo.
        """
        s = Servos.___servo(port)
        if s.angle == None:
            if pulse_width_range != None:
                s.set_pulse_width_range(
                    pulse_width_range.min_pulse, pulse_width_range.max_pulse
                )
            s.angle = start_angle
        return RotatorServo(s)

    @staticmethod
    def sg90(port: int, start_angle: float = 0) -> RotatorServo:
        """Create a RotatorServo on the given CRICKIT servo port.

        Assumes only one CRICKIT in the system.

        Args:
            port (int): which servo port to use (1-4)
            start_angle (float, optional): sets the initial angle of the servo. Defaults to 0.

        Returns:
            RotatorServo: A "steppable" servo.
        """
        return Servos.servo(port, start_angle, PulseWidthRange.SG90())


class Steppers:
    """Wraps the CRICKIT Hat stepper ports.

    Assumes only one CRICKIT in the system.
    """

    @staticmethod
    def stepper(
        gear_ratio: float = 1.0, steps_per_rotation: int = 200
    ) -> RotatorStepper:
        """Create a RotatorStepper on the given CRICKIT stepper port.

        Args:
            gear_ratio (float): gear ratio of the stepper, defaults to 1.0
            steps_per_rotation (int): steps per rotation of the stepper. Defaults to 200.

        Returns:
            RotatorStepper: A "rotatable" stepper.
        """
        geared_stepper = GearedStepper(
            crickit.stepper_motor, gear_ratio, steps_per_rotation
        )
        return RotatorStepper(geared_stepper)
