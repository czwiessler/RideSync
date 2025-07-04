import RPi.GPIO as GPIO
import time


class Speedomter:
    def __init__(self, wheel_circumrefecrence: float):
        self.wheel_circumrefence = wheel_circumrefecrence
    PULSE_PIN = 17

    last_time = time.time()

    speed_kph = 0.00

    def pulse_detected(self, channel):
        global last_time
        global speed_kph
        now = time.time()
        dt = now - last_time
        last_time = now

        if dt > 0.1:  # debounce: ignore pulses < 100 ms apart
            speed_kph = (self.wheel_circumrefence / dt) * 3.6

    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(PULSE_PIN, GPIO.FALLING, callback=pulse_detected, bouncetime=50)

    def read_speed():
        return speed_kph