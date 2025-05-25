# traffic_light_fetcher.py
"""
Python-Übersetzung der C++-Klasse TrafficLightFetcher.
Lädt Ampeldaten aus einer GeoJSON-Datei und liefert relevante Ampeln entlang einer Route.
"""
from typing import List, Tuple
from datetime import datetime, timedelta
import json

from TrafficLight import TrafficLight, Phase


class TrafficLightFetcher:
    def __init__(self) -> None:
        """
        Initialisiert den Fetcher mit leerer Ampelliste.
        """
        self._all_traffic_lights: List[TrafficLight] = []

    def haversine_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        Berechnet die Entfernung (Meter) zwischen zwei Koordinaten via Haversine-Formel.
        """
        from math import radians, sin, cos, sqrt, atan2
        R = 6371000.0  # Erdradius in Metern
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def load_from_json(self, filename: str) -> bool:
        """
        Lädt Ampeln aus einer GeoJSON-Datei im Overpass-Format.

        :param filename: Pfad zur JSON-Datei
        :return: True, wenn Laden erfolgreich war, sonst False
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return False

        now = datetime.now()
        # Erzeuge simulierte Grünphasen für jede Ampel
        for feature in data.get('features', []):
            geom = feature.get('geometry', {})
            coords = geom.get('coordinates', [])
            if len(coords) < 2:
                continue
            lon, lat = coords[0], coords[1]

            # TODO: Hier sollten echte Grünphasen geladen werden, z.B. aus einem Attribut
            phases: List[Phase] = [
                (now + timedelta(seconds=10), now + timedelta(seconds=20)),
                (now + timedelta(seconds=70), now + timedelta(seconds=80)),
            ]
            ##########

            tl = TrafficLight(float(lat), float(lon), phases)
            self._all_traffic_lights.append(tl)

        return True

    def get_relevant_traffic_lights(
        self, route: List[Tuple[float, float]], buffer: float = 2.0
    ) -> List[TrafficLight]:
        """
        Gibt alle Ampeln zurück, die maximal `buffer` Meter links und rechts entlang
        der Route (als Polyline) liegen, sortiert nach ihrem Auftreten entlang der Route.

        :param route: Liste von Wegpunkten (lat, lon)
        :param buffer: Abstand in Metern zur Route
        :return: Liste relevanter TrafficLight-Objekte
        """
        relevant = []  # Liste von Tuplen (TrafficLight, segment_index, t)
        if not route:
            return []

        from math import radians, cos, sqrt
        R = 6371000.0  # Erdradius in Metern

        def proj_and_distance(
            lat_p: float, lon_p: float,
            lat1: float, lon1: float,
            lat2: float, lon2: float
        ) -> Tuple[float, float]:
            """
            Berechnet die Projektion t (0-1) und Distanz (Meter) eines Punktes auf ein Liniensegment
            via equirectangular Projektion.
            """
            mean_lat = radians((lat1 + lat2) / 2)
            x1 = radians(lon1) * R * cos(mean_lat)
            y1 = radians(lat1) * R
            x2 = radians(lon2) * R * cos(mean_lat)
            y2 = radians(lat2) * R
            xp = radians(lon_p) * R * cos(mean_lat)
            yp = radians(lat_p) * R

            dx = x2 - x1
            dy = y2 - y1
            if dx == 0 and dy == 0:
                return 0.0, sqrt((xp - x1) ** 2 + (yp - y1) ** 2)
            t = ((xp - x1) * dx + (yp - y1) * dy) / (dx * dx + dy * dy)
            t_clamped = max(0.0, min(1.0, t))
            proj_x = x1 + t_clamped * dx
            proj_y = y1 + t_clamped * dy
            dist = sqrt((xp - proj_x) ** 2 + (yp - proj_y) ** 2)
            return t_clamped, dist

        # Finde relevante Ampeln mit Segment-Index und t
        for light in self._all_traffic_lights:
            lat_l, lon_l = light.get_location()
            best = None  # (segment_idx, t)
            for idx, ((lat1, lon1), (lat2, lon2)) in enumerate(zip(route, route[1:])):
                t, d = proj_and_distance(lat_l, lon_l, lat1, lon1, lat2, lon2)
                if d <= buffer:
                    if best is None or (idx, t) < best:
                        best = (idx, t)
            if best is not None:
                relevant.append((light, best[0], best[1]))

        # Sortiere nach Segment-Index und t entlang des Segments
        relevant.sort(key=lambda item: (item[1], item[2]))

        # Extrahiere nur die TrafficLight-Objekte
        return [item[0] for item in relevant]


