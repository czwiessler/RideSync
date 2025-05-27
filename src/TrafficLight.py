from typing import Tuple
import datetime
from datetime import timedelta

TimePoint = datetime.datetime

datetime.timedelta


class TrafficLight:
    def __init__(self, id: str, lat: float, lon: float) -> None:
        """
        Initialisiert eine Ampel mit Position und individuellen Zyklusparametern.
        """
        self.id: str = id
        self.latitude: float = lat
        self.longitude: float = lon

        # Neue Mock-Parameter
        self.green_duration: datetime.timedelta = datetime.timedelta(seconds=10)
        self.red_duration: datetime.timedelta = datetime.timedelta(seconds=40)
        self.offset: datetime.timedelta = datetime.timedelta(seconds=0)
        self.mock_initialized: bool = False

    def get_location(self) -> Tuple[float, float]:
        return (self.latitude, self.longitude)

    def get_id(self) -> str:
        return f"{self.id}"


    #TODO theoretisch müsste diese func iwann echtzeitphasendaten abrufen aber naja ne
    def get_next_green_phase(
            self,
            current_time: timedelta
    ) -> Tuple[timedelta, timedelta]:
        """
        Gibt die nächste Grünphase basierend auf individuellem Zyklus zurück.
        """
        cycle_length = self.green_duration + self.red_duration
        start_time = current_time - self.offset  # theoretischer Zyklusstart
        time_in_cycle = (current_time - start_time) % cycle_length

        if time_in_cycle < self.green_duration:
            phase_start = current_time - time_in_cycle
        else:
            time_to_next_green = cycle_length - time_in_cycle
            phase_start = current_time + time_to_next_green

        return phase_start, phase_start + self.green_duration

    #TODO theoretisch müsste diese func iwann echtzeitphasendaten abrufen aber naja ne
    def get_phase(
            self,
            current_time: timedelta
    ) -> Tuple[str, timedelta.seconds]: #'green' or 'red', phase rest duration

        cycle_duration = self.green_duration + self.red_duration
        # Zyklusstartzeit so berechnen, dass offset mit eingerechnet wird
        start_time = timedelta(seconds=0) + self.offset
        time_in_cycle = (current_time - start_time) % cycle_duration

        if time_in_cycle < self.green_duration:
            phase = 'green'
            remaining = self.green_duration - time_in_cycle
        else:
            phase = 'red'
            time_in_red = time_in_cycle - self.green_duration
            remaining = self.red_duration - time_in_red

        return phase, remaining