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
            phases: List[Phase] = [
                (now + timedelta(seconds=10), now + timedelta(seconds=20)),
                (now + timedelta(seconds=70), now + timedelta(seconds=80)),
            ]
            tl = TrafficLight(float(lat), float(lon), phases)
            self._all_traffic_lights.append(tl)

        return True

    def get_relevant_traffic_lights(
        self, route: List[Tuple[float, float]]
    ) -> List[TrafficLight]:
        """
        Gibt alle Ampeln zurück, die maximal 30 Meter von irgendeinem Punkt der Route entfernt sind.

        :param route: Liste von Wegpunkten (lat, lon)
        :return: Liste relevanter TrafficLight-Objekte
        """
        relevant: List[TrafficLight] = []
        for light in self._all_traffic_lights:
            lat_l, lon_l = light.get_location()
            for lat_p, lon_p in route:
                if self.haversine_distance(lat_l, lon_l, lat_p, lon_p) < 30.0:
                    relevant.append(light)
                    break
        return relevant
