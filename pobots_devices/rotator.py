from pobots_devices import _DEFAULT_RATE, move_servo, move_stepper
from adafruit_motor.servo import Servo
from adafruit_motor.stepper import StepperMotor

_DEFAULT_DELTA = 1


class Rotator:
    """An "abstract" class that defines the interface for an object that rotates."""

    def __init__(
        self, rate: float = _DEFAULT_RATE, delta: int = _DEFAULT_DELTA
    ) -> None:
        """Create a Rotator object."""
        self._rate = rate
        self._delta = delta

    @property
    def rate(self) -> float:
        return self._rate

    @rate.setter
    def rate(self, rate: float) -> None:
        self._rate = rate

    @property
    def delta(self) -> int:
        return self._delta

    @delta.setter
    def delta(self, delta: int) -> None:
        self._delta = delta

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, angle: float) -> None:
        """Set the angle of the Rotator.

        This should cause the physical device to move to the given angle.
        """
        raise NotImplementedError("angle is read-only")

    def step(self, forward: bool = True) -> None:
        """Causes the physical device to move one step.

        Args:
            forward (bool, optional): direction to move. Defaults to True.
        """
        raise NotImplementedError("angle is read-only")


class RotatorServo(Rotator):
    """Servo wrapper that implements the Rotator interface."""

    def __init__(
        self, servo: Servo, rate: float = _DEFAULT_RATE, delta: int = _DEFAULT_DELTA
    ) -> None:
        """Create a RotatorServo object.

        Args:
            servo (Servo): the servo to wrap
            rate (float, optional): pause between steps. Defaults to _DEFAULT_RATE.
            delta (int, optional): number of degrees to move per step. Defaults to 1.
        """
        super().__init__(rate, delta)
        self._servo = servo

    @property
    def angle(self) -> float:
        return self._servo.angle

    @angle.setter
    def angle(self, angle: float) -> None:
        move_servo(self._servo, int(angle), self._delta, self._rate)


class PulseWidthRange:
    """Simple class to denote the pulse-width range of a servo."""

    def __init__(self, min_pulse: int, max_pulse: int) -> None:
        self._min_pulse = min_pulse
        self._max_pulse = max_pulse

    @property
    def min_pulse(self) -> int:
        return self._min_pulse

    @property
    def max_pulse(self) -> int:
        return self._max_pulse

    @staticmethod
    def SG90():
        """Returns the pulse-width range for an SG90 (and clones) servo."""
        return PulseWidthRange(500, 2400)


class GearedStepper:
    """Simple class to denote a stepper motor with a gear ratio and steps per rotation."""

    def __init__(
        self, stepper: StepperMotor, gear_ratio: float, steps_per_rotation: int
    ) -> None:
        self._stepper = stepper
        self._gear_ratio = gear_ratio
        self._steps_per_rotation = steps_per_rotation

    @property
    def stepper(self) -> StepperMotor:
        return self._stepper

    @property
    def gear_ratio(self) -> float:
        return self._gear_ratio

    @property
    def steps_per_rotation(self) -> int:
        return self._steps_per_rotation


class RotatorStepper(Rotator):
    """Stepper wrapper that implements the Rotator interface.

    Because steppers have no notion of "position", this class keeps track of the current position
    and assumes that the stepper is at that position. The stepper does NOT lock into position when
    movement stops, so manual adjustments/calibration can be performed.
    """

    def __init__(self, stepper: GearedStepper, rate: float = _DEFAULT_RATE) -> None:
        """Create a RotatorStepper object.

        The current "delta" is 1 step.
        TODO translate delta into steps based on gear ratio and steps per rotation.

        Args:
            stepper (GearedStepper): the stepper to wrap
            rate (float, optional): pause between steps. Defaults to _DEFAULT_RATE.
            delta (int, optional): number of degrees to move per step. Defaults to 1.
        """
        super().__init__(rate, 1)
        self._gr = stepper
        self._gr.stepper.release()
        self._stepper_position = 0

    @property
    def angle(self) -> float:
        self._stepper_position

    @angle.setter
    def angle(self, angle: float) -> None:
        degrees_change = angle - self._stepper_position

        move_stepper(
            self._gr.stepper,
            degrees_change,
            self._rate,
            self._gr.steps_per_rotation,
            self._gr.gear_ratio,
        )

        self._stepper_position = angle
        # temporary to keep it from heating up too much
        self._gr.stepper.release()
