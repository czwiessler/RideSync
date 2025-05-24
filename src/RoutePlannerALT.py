# route_planner.py
"""
Python-Übersetzung von RoutePlanner (C++).
Berechnet eine einfache, lineare Route in 10 Schritten.
"""

from typing import List, Tuple


def compute_route(start: Tuple[float, float], end: Tuple[float, float]) -> List[Tuple[float, float]]:
    """
    Berechnet eine Route zwischen start und end als Liste von Zwischenkoordinaten.
    Aktuell lineare Interpolation in 10 Schritten (MVP).

    :param start: Tuple[float, float] mit Start-Koordinaten (latitude, longitude)
    :param end: Tuple[float, float] mit Ziel-Koordinaten (latitude, longitude)
    :return: Liste von Tuple[float, float] mit den Wegpunkten
    """
    route: List[Tuple[float, float]] = []
    steps: int = 10
    lat_step: float = (end[0] - start[0]) / steps
    lon_step: float = (end[1] - start[1]) / steps

    for i in range(steps + 1):
        lat = start[0] + i * lat_step
        lon = start[1] + i * lon_step
        route.append((lat, lon))

    return route


