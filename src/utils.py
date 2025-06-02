# utils.py

from typing import Tuple, List
import math

def haversine(
        coord1: Tuple[float, float],
        coord2: Tuple[float, float]
) -> float:
    """
    Calculate the great-circle distance between two points on the Earth (in meters) using the Haversine formula.
    :param coord1: (latitude, longitude)
    :param coord2: (latitude, longitude)
    :return: distance in meters
    """
    r = 6371000.0  # Earth radius in meters
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def haversine_along_route(
    start_point: Tuple[float, float],
    end_point: Tuple[float, float],
    route: List[Tuple[float, float]]
) -> float:
    """
    Berechnet die Distanz entlang einer Route zwischen zwei Punkten (auch wenn diese nicht exakt auf der Route liegen).
    Die Route wird dabei segmentweise mit der Haversine-Formel ausgewertet.

    :param start_point: Startkoordinate (z. B. aktuelle Position)
    :param end_point: Endkoordinate (z. B. Ampelposition)
    :param route: Liste der Wegpunkte der Route
    :return: Entfernung in Metern entlang der Route
    """
    if not route or len(route) < 2:
        return 0.0

    # Nächstes Segment zum Startpunkt finden
    min_start_dist = float('inf')
    start_index = 0
    for i in range(len(route) - 1):
        dist = haversine(start_point, route[i])
        if dist < min_start_dist:
            min_start_dist = dist
            start_index = i

    # Nächstes Segment zum Endpunkt finden
    min_end_dist = float('inf')
    end_index = 0
    for i in range(len(route) - 1):
        dist = haversine(end_point, route[i])
        if dist < min_end_dist:
            min_end_dist = dist
            end_index = i

    # Sicherstellen, dass start_index vor end_index liegt
    if start_index > end_index:
        start_index, end_index = end_index, start_index
        start_point, end_point = end_point, start_point

    # 1. Startpunkt bis Segmentstart
    total_distance = haversine(start_point, route[start_index])

    # 2. Volle Segmente dazwischen
    for i in range(start_index, end_index):
        total_distance += haversine(route[i], route[i + 1])

    # 3. Letztes Segmentende bis Endpunkt
    total_distance += haversine(route[end_index], end_point)

    return total_distance

