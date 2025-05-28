from typing import Tuple, List
from datetime import timedelta

from SpeedAdvisor import SpeedAdvisor
from TrafficLight import TrafficLight


class MockedCyclist:
    """
    MockedRadfahrer hält Zustand und wählt Geschwindigkeit mittels SpeedAdvisor.
    """
    def __init__(
        self,
        start_position: Tuple[float, float],
        preferred_speed: float = 6.0,
        min_speed: float = 1.0,
        max_speed: float = 10.0
    ):
        # Fahrerzustand
        self.current_position: Tuple[float, float] = start_position
        self.current_speed: float = preferred_speed
        self.preferred_speed: float = preferred_speed
        self.min_speed: float = min_speed
        self.max_speed: float = max_speed

    def get_current_position(self) -> Tuple[float, float]:
        """
        Liefert die aktuelle Position des Fahrers.
        """
        return self.current_position

    def get_current_speed(self) -> float:
        """
        Liefert die aktuelle Geschwindigkeit des Fahrers.
        """
        return self.current_speed

    def choose_velocity(
            self,
            advised_speed: float,
                        ) -> float:
        self.current_speed = advised_speed
        return self.current_speed


    # def choose_velocity(
    #     self,
    #     next_light: TrafficLight,
    #     duration: timedelta
    # ) -> float:
    #     """
    #     Bestimmt die empfohlene Geschwindigkeit, um die nächste Grünphase zu erreichen.
    #     Nutzt SpeedAdvisor.choose_best_phase_and_speed.
    #
    #     :param next_light: Die nächste relevante TrafficLight-Instanz
    #     :param duration: Seit Programmstart verstrichene Zeit als timedelta
    #     :return: Neue Geschwindigkeit (m/s)
    #     """
    #     # Erfrage die Startzeiten der nächsten Grünphasen
    #     green_starts: List[timedelta] = next_light.get_next_green_starts(duration)
    #
    #     # Delegiere an SpeedAdvisor
    #     phase, recommended = SpeedAdvisor.choose_best_phase_and_speed(
    #         current_position=self.current_position,
    #         next_light=next_light,
    #         green_starts=green_starts,
    #         now=duration
    #     )
    #
    #     # Auf min/max begrenzen
    #     new_speed = max(self.min_speed, min(recommended, self.max_speed))
    #     self.current_speed = new_speed
    #     return new_speed
