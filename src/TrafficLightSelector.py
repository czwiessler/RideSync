from typing import Tuple, List, Optional
import math
from TrafficLight import TrafficLight

class TrafficLightSelector:
    """
    Wählt die nächste Ampel entlang einer vorgegebenen Route basierend auf der aktuellen Position aus.
    """
    def __init__(self):
        self.route: List[Tuple[float, float]] = []
        self._cum_distances: List[float] = []

    def set_route(self, route: List[Tuple[float, float]]) -> None:
        """
        Legt die aktuelle Route fest und berechnet die akkumulierten Distanzen für Wegpunkte.
        :param route: Liste von GPS-Koordinaten der Route in Fahrtrichtung.
        """
        self.route = route
        self._compute_cumulative_distances()

    def _haversine(self, a: Tuple[float, float], b: Tuple[float, float]) -> float:
        """
        Berechnet die euklidische Distanz zwischen zwei Punkten.
        Bei echten GPS-Daten kann hier später auf einen geodätischen Ansatz umgestellt werden.
        """
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def _compute_cumulative_distances(self) -> None:
        """
        Erzeugt eine Liste, in der jeder Eintrag die Distanz ab Routenanfang bis zu diesem Waypoint ist.
        """
        self._cum_distances = [0.0]
        for a, b in zip(self.route, self.route[1:]):
            dist = self._haversine(a, b)
            self._cum_distances.append(self._cum_distances[-1] + dist)

    def _distance_along_route(self, point: Tuple[float, float]) -> float:
        """
        Findet auf welchem Segment der Punkt am nächsten liegt, projiziert ihn darauf
        und gibt die Strecke ab Start bis zum Projektionspunkt zurück.
        """
        best_dist = float('inf')
        best_along = 0.0

        for i, (a, b) in enumerate(zip(self.route, self.route[1:])):
            dx, dy = b[0] - a[0], b[1] - a[1]
            seg_len2 = dx * dx + dy * dy
            if seg_len2 == 0:
                continue

            # Projektion von point auf AB
            t = ((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / seg_len2
            t_clamped = max(0.0, min(1.0, t))
            proj = (a[0] + t_clamped * dx, a[1] + t_clamped * dy)

            d = self._haversine(point, proj)
            if d < best_dist:
                best_dist = d
                best_along = self._cum_distances[i] + math.sqrt(seg_len2) * t_clamped

        return best_along

    def get_next_traffic_light(
        self,
        current_pos: Tuple[float, float],
        lights: List[TrafficLight]
    ) -> Optional[TrafficLight]:
        """
        Gibt die erste Ampel zurück, deren Distanz entlang der Route größer
        ist als die der aktuellen Position.
        :param current_pos: Aktuelle GPS-Position
        :param lights: Sortierte Liste relevanter TrafficLight-Objekte
        :return: Nächste Ampel oder None, falls keine vorhanden
        """
        if not self.route or not lights:
            return None

        pos_dist = self._distance_along_route(current_pos)
        for light in lights:
            # Verwende get_location() statt direkten Zugriff auf Attribute
            light_loc = light.get_location()
            light_dist = self._distance_along_route(light_loc)
            if light_dist > pos_dist:
                return light

        # Alle Ampeln passiert -> letzte zurückgeben
        return lights[-1]