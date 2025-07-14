# traffic_light_fetcher.py
"""
Lädt Ampeldaten aus einer GeoJSON-Datei und liefert relevante Ampeln entlang einer Route.
"""
from typing import List, Tuple
#from datetime import datetime #nur zum messen
import json
from datetime import timedelta

from TrafficLight import TrafficLight#, Phase


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

        #gemessene werte für strecke innere kanalstr, erste ampel venloer bis letzte ampel aachener
        mock_configs = {
            "venloer/4279001084": (57, 53, 0), #venloer
            "vogelsanger/2107720091": (65, 45, 6), #vogelsanger
            "weinsberg/2603639844": (70, 40, 60), #weinsberg
            # "hollar/8546960460": (90, 20, 32),  # hollar
            # "aachener/750549269": (55, 55, 65), #aachener
        }

        # Erstelle die Ampel Objekte
        for feature in data.get('features', []):
            geom = feature.get('geometry', {})
            coords = geom.get('coordinates', [])
            if len(coords) < 2:
                continue
            lon, lat = coords[0], coords[1]
            id_ = feature.get("id", "unknown")

            tl = TrafficLight(id_, float(lat), float(lon))

            if id_ in mock_configs:
                grn, red, off = mock_configs[id_]
                tl.green_duration = timedelta(seconds=grn)
                tl.red_duration = timedelta(seconds=red)
                tl.offset = timedelta(seconds=off)
                tl.mock_initialized = True

            self._all_traffic_lights.append(tl)

        return True

    def get_relevant_traffic_lights(
            self,
            route: List[Tuple[float, float]],
            buffer: float = 2.0
    ) -> List[TrafficLight]:
        """
        Gibt alle Ampeln zurück, die maximal `buffer` Meter links und rechts entlang
        der Route (als Polyline) liegen, sortiert nach ihrem Auftreten entlang der Route.
        """
        #start_time = datetime.now() #nur zum messen

        relevant = []
        if not route:
            return []

        from math import radians, cos, sqrt

        R = 6371000.0  # Erdradius in Metern

        # --- Bounding Box vorbereiten (ca. 50–100m Sicherheitsabstand je nach Buffer) ---
        margin_deg = buffer / 111111.0  # grob 1° ~ 111 km → in Grad umrechnen
        lat_vals = [lat for lat, _ in route]
        lon_vals = [lon for _, lon in route]
        lat_min = min(lat_vals) - margin_deg
        lat_max = max(lat_vals) + margin_deg
        lon_min = min(lon_vals) - margin_deg
        lon_max = max(lon_vals) + margin_deg

        def is_within_bbox(lat: float, lon: float) -> bool:
            return lat_min <= lat <= lat_max and lon_min <= lon <= lon_max

        def proj_and_distance(
                lat_p: float, lon_p: float,
                lat1: float, lon1: float,
                lat2: float, lon2: float
        ) -> Tuple[float, float]:
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

        # --- Nur relevante Ampeln in BBox prüfen ---
        for light in self._all_traffic_lights:
            lat_l, lon_l = light.get_location()

            # Skip if not in bounding box
            if not is_within_bbox(lat_l, lon_l):
                continue

            best = None
            for idx, ((lat1, lon1), (lat2, lon2)) in enumerate(zip(route, route[1:])):
                t, d = proj_and_distance(lat_l, lon_l, lat1, lon1, lat2, lon2)
                if d <= buffer:
                    if best is None or (idx, t) < best:
                        best = (idx, t)
            if best is not None:
                relevant.append((light, best[0], best[1]))

        relevant.sort(key=lambda item: (item[1], item[2]))

        print('relevante Ampeln:')
        for i, (light, segment, t_val) in enumerate(relevant):
            print(f"Ampel Nr. {i}: {light.get_id()}, Segment: {segment}, t: {t_val}")

        # duration = datetime.now() - start_time #nur zum messen
        # print(f"[Timing] get_relevant_traffic_lights dauerte {duration.total_seconds() * 1000:.2f} ms") #nur zum messen

        return [item[0] for item in relevant]



