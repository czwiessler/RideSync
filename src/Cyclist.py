from typing import Tuple
import gpsd

import Speedometer

class Cyclist:
    """
        PI Input
    """
    def __init__(
        self,
        speedometer: Speedometer,
        preferred_speed: float = 6.0,
        min_speed: float = 1.0,
        max_speed: float = 10.0,
    ):
        # Fahrerzustand
        self.preferred_speed: float = preferred_speed
        self.min_speed: float = min_speed
        self.max_speed: float = max_speed
        self.speedotmeter = speedometer
        gpsd.connect()


    def get_current_position(self) -> Tuple[float, float]:
        return (gpsd.get_current().lat,gpsd.get_current().lon)


    def get_current_speed(self) -> float:
        return self.speedotmeter.speed_kph