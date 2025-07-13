from typing import Tuple
import gpsd
import RPi.GPIO as GPIO
from RPLCD import CharLCD

import Speedometer

class Cyclist:
    """
        PI Input
    """
    def __init__(
        self,
        speedometer: Speedometer,
        preferred_speed: float = 6.0,
        min_speed: float = 0.0,
        max_speed: float = 8.0,
    ):
        # Fahrerzustand
        self.preferred_speed: float = preferred_speed
        self.min_speed: float = min_speed
        self.max_speed: float = max_speed
        self.speedotmeter = speedometer
        self.lcd = CharLCD(numbering_mode = GPIO.BOARD, cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])
        gpsd.connect()


    def get_current_position(self) -> Tuple[float, float]:
        return (gpsd.get_current().lat,gpsd.get_current().lon)


    def get_current_speed(self) -> float:
        return self.speedotmeter.speed_kph
    
    def set_advicde_speed(self, adviced_speed):
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0) 
        self.lcd.write_string(f"{self.speedotmeter.speed_kph:.2f}")
        self.lcd.cursor_pos = (1, 0) 
        self.lcd.write_string(f"{adviced_speed:.2f}")