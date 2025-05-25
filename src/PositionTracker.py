"""
Holt aktuell GPS-Position im Mock-Modus.
"""

from typing import List, Tuple
import math


class PositionTracker:
    @staticmethod
    def get_current_position() -> Tuple[float, float]:
        """
        Liefert die aktuelle GPS-Position.
        Aktuell im Mock-Modus: Beispielkoordinaten für den Kölner Dom.

        :return: Tuple[float, float] mit (latitude, longitude)
        """
        # === Mock-Modus ===
        latitude: float = 50.948172  # Beispiel: Köln Dom
        longitude: float = 6.932064
        return (latitude, longitude)
        # TODO: Später echte GPS-Integration
        # === Original TinyGPS++-Logik (später) ===
        # import gpsd
        # packet = gpsd.get_current()
        # if packet.mode >= 2:
        #     return (packet.lat, packet.lon)
        # else:
        #     raise RuntimeError("Ungültige GPS-Position")

    @staticmethod
    def haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """
        Calculate the great-circle distance between two points on the Earth (in meters) using the Haversine formula.
        :param coord1: (latitude, longitude)
        :param coord2: (latitude, longitude)
        :return: distance in meters
        """
        R = 6371000.0  # Earth radius in meters
        lat1, lon1 = map(math.radians, coord1)
        lat2, lon2 = map(math.radians, coord2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def get_current_position_mock(
            self,
            route: List[Tuple[float, float]],
            duration: float  # elapsed time in seconds
    ) -> Tuple[float, float]:
        """
        Simulate the current position along a route, moving at 6 meters per second.

        :param route: List of waypoints (latitude, longitude)
        :param duration: Time elapsed in seconds
        :return: (latitude, longitude) of the current position along the route
        """
        # No route or single-point route: return origin or only point
        if not route:
            return (0.0, 0.0)
        if len(route) == 1:
            return route[0]

        # Total distance to travel based on 6 m/s speed
        total_distance = duration * 3.0  # meters
        traveled = 0.0

        # Walk through each segment
        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]
            segment_dist = self.haversine(start, end)

            # If the target distance falls within this segment
            if traveled + segment_dist >= total_distance:
                remaining = total_distance - traveled
                fraction = remaining / segment_dist if segment_dist > 0 else 0.0
                lat = start[0] + (end[0] - start[0]) * fraction
                lon = start[1] + (end[1] - start[1]) * fraction
                return (lat, lon)

            # Otherwise, subtract segment and continue
            traveled += segment_dist

        # If traveled beyond the last point, return the final waypoint
        return route[-1]
