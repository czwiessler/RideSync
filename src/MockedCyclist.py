from typing import Tuple


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
        #TODO IMPLEMENT GPS-Schnittstelle, angeknüpft an GPS-Modul
        return self.current_position


    def get_current_speed(self) -> float:
        #TODO IMPLEMENT Tacho-Schnittstelle
        return self.current_speed


    # TODO mock wird später nicht mehr genutzt, da Fahrrad tatsächlich Geschwindigkeit ändert
    def change_velocity_mock(
            self,
            advised_speed: float,
    ) -> float:
        self.current_speed = advised_speed
        return self.current_speed

