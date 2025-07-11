import RPi.GPIO as GPIO
import time


class Speedometer:
    PULSE_PIN = 11  # Class variable for the pin number

    def __init__(self, wheel_circumference: float):
        self.wheel_circumference = wheel_circumference
        self.last_time = time.time()  # Instance variable for the last pulse time
        self.speed_kph = 0.00  # Instance variable for the current speed

        # Set up GPIO - these should be done in the constructor
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Pass self to the callback using a lambda or functools.partial if needed
        # For GPIO callbacks, it's often cleaner to make the callback a method
        # and ensure it can be called without an instance reference if directly assigned,
        # or bind it correctly. In this case, we'll make it an instance method
        # and pass a reference to the instance's method.
        GPIO.add_event_detect(self.PULSE_PIN, GPIO.FALLING, callback=self._pulse_detected_callback, bouncetime=50)

    # Renamed to a private-like method since it's an internal callback
    def _pulse_detected_callback(self, channel):
        # The 'channel' argument is passed by RPi.GPIO, but we don't use it here.
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        if dt > 0.01:  # debounce: ignore pulses < 10 ms apart (a more typical debounce for this)
            # Calculate speed in meters/second, then convert to km/h
            # wheel_circumference is in meters, dt in seconds
            speed_mps = self.wheel_circumference / dt
            self.speed_kph = speed_mps * 3.6
        else:
            # If the debounce condition is met, it means it was likely a bounce,
            # so we might want to reset speed or ignore this pulse's effect on speed calculation
            # For simplicity, we just won't update speed if it's a bounce
            pass

    def read_speed(self) -> float:
        """
        Returns the current calculated speed in kilometers per hour.
        """
        return self.speed_kph

    def cleanup(self):
        """
        Cleans up the GPIO settings. Should be called when the program exits.
        """
        GPIO.cleanup()

