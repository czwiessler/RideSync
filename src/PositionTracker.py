from typing import List, Tuple
import math

from datetime import timedelta

from MockedCyclist import MockedCyclist
from utils import haversine



class PositionTracker:

    # TODO loswerden, die func wird nur noch von main benutzt
    @staticmethod
    def get_current_position() -> Tuple[float, float]:
        """
        Liefert die aktuelle GPS-Position.
        Aktuell im Mock-Modus: Beispielkoordinaten für den Kölner Dom.

        :return: Tuple[float, float] mit (latitude, longitude)
        """
        latitude: float = 50.948172
        longitude: float = 6.932064
        return (latitude, longitude)

    def get_current_position_mock(
            self,
            mocked_cyclist,
            route: List[Tuple[float, float]],
            time_elapsed: timedelta  # elapsed time as timedelta
    ) -> Tuple[float, float]:
        """
        Simulate the current position along a route, moving at the current speed from SpeedTracker.

        :param route: List of waypoints (latitude, longitude)
        :param time_elapsed: elapsed time since start as timedelta
        :return: Tuple (latitude, longitude) of the current position along the route
        """
        # Keine Route: Nullpunkt
        if not route:
            return (0.0, 0.0)
        # Ein-Punkt-Route: Konstante Position
        if len(route) == 1:
            return route[0]

        # Geschwindigkeit in m/s vom mockedcyclist holen

        speed = mocked_cyclist.get_current_speed()

        # Gesamtdistanz basierend auf aktueller Geschwindigkeit
        total_distance = time_elapsed.seconds * speed
        traveled = 0.0

        # Durch Geopunkte iterieren
        for start, end in zip(route, route[1:]):
            segment_dist = haversine(start, end)
            if traveled + segment_dist >= total_distance:
                # Restdistanz berechnen und interpolieren
                remaining = total_distance - traveled
                fraction = remaining / segment_dist if segment_dist > 0 else 0.0
                lat = start[0] + (end[0] - start[0]) * fraction
                lon = start[1] + (end[1] - start[1]) * fraction
                return (lat, lon)
            traveled += segment_dist

        # Wenn Route zu Ende gefahren, letzten Punkt zurückgeben
        return route[-1]
