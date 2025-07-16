import datetime
from datetime import timedelta
from typing import Tuple, List


class TrafficLight:
    def __init__(self, id: str, lat: float, lon: float) -> None:
        """
        Initialisiert eine Ampel mit Position und individuellen Zyklusparametern.
        """
        self.id: str = id
        self.latitude: float = lat
        self.longitude: float = lon

        # Mock-Parameter
        self.green_duration: datetime.timedelta = datetime.timedelta(seconds=10)
        self.red_duration: datetime.timedelta = datetime.timedelta(seconds=40)
        self.offset: datetime.timedelta = datetime.timedelta(seconds=0)
        self.mock_initialized: bool = False

    def get_location(self) -> Tuple[float, float]:
        return (self.latitude, self.longitude)

    def get_id(self) -> str:
        return f"{self.id}"

    def get_phase(
            self,
            current_time: timedelta
    ) -> Tuple[str, timedelta.seconds]:  # 'green' or 'red', phase rest duration
        """
        Bestimmt die aktuelle Phase der Ampel und die verbleibende Zeit bis zum Phasenwechsel.
        :param current_time:
        :returns : Tuple mit Phase ('green' oder 'red') und verbleibender Zeit in der Phase als timedelta
        """
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

    def get_next_green_starts(
        self,
        current_time: timedelta,
    ) -> List[timedelta]:
        """
        Gibt für die kommenden 50 Zyklen die Zeit in Sekunden bis zum Grünstart zurück.
        :param current_time:
        :return: Liste von timedeltas in sekunden bis zum Beginn der nächsten 50 Grünphasen
        """
        cycle_duration = self.green_duration + self.red_duration
        # Zeit innerhalb des Zyklus unter Berücksichtigung des Offsets
        time_in_cycle = (current_time - self.offset) % cycle_duration
        # Verzögerung bis zum nächsten Grünstart
        # first_delay = cycle_duration - time_in_cycle

        if time_in_cycle < self.red_duration:
            first_delay = self.red_duration - time_in_cycle
        else:
            first_delay = cycle_duration - (time_in_cycle - self.red_duration)

        starts: List[timedelta] = []
        for i in range(50):
            starts.append(first_delay + i * cycle_duration)
        return starts
