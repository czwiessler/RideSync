# traffic_light.py
"""
Python-Übersetzung der C++-Klasse TrafficLight.
Verwaltet Standort und Grünphasen einer Ampel.
"""

from typing import Tuple, List
import datetime


TimePoint = datetime.datetime
Phase = Tuple[TimePoint, TimePoint]


class TrafficLight:
    def __init__(self, lat: float, lon: float, phases: List[Phase]) -> None:
        """
        Initialisiert eine Ampel mit Position und Liste von Grünphasen.

        :param lat: Breitengrad
        :param lon: Längengrad
        :param phases: Liste von Tupeln (start_time, end_time)
        """
        self.latitude: float = lat
        self.longitude: float = lon
        self.green_phases: List[Phase] = phases

    def get_location(self) -> Tuple[float, float]:
        """
        Liefert die Koordinaten der Ampel.

        :return: (latitude, longitude)
        """
        return (self.latitude, self.longitude)

    def get_next_green_phase(self, current_time: TimePoint) -> Phase:
        """
        Gibt die nächste noch nicht abgelaufene Grünphase zurück.
        Falls keine Phase mehr übrig ist, wird die erste Phase um 24h verschoben.
        Wenn keine Phasen definiert sind, wird (now, now) zurückgegeben.

        :param current_time: Aktueller Zeitpunkt
        :return: Tuple (start_time, end_time)
        """
        # TODO: aktuell noch mock, weil Phasen nicht geladen werden
        # Suche erste Phase, deren Ende in der Zukunft liegt
        for phase in self.green_phases:
            if current_time < phase[1]:
                return phase

        # Zyklisches Verhalten: erste Phase am nächsten Tag
        if self.green_phases:
            first_phase = self.green_phases[0]
            delta = datetime.timedelta(days=1)
            return (first_phase[0] + delta, first_phase[1] + delta)

        # Keine Phasen: Dummy-Phase jetzt
        now = datetime.datetime.now()
        return (now, now)
