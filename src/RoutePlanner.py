# route_planner.py
"""
Nutzt die OpenRouteService API, um eine echte Route zu holen.
"""

import os
import requests
from typing import List, Tuple

#ORS_API_KEY = os.getenv("ORS_API_KEY")
ORS_API_KEY = "5b3ce3597851110001cf624845c31aefb65f430fbd3184463a7b9edb"
ORS_BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

def compute_route(start: Tuple[float, float], end: Tuple[float, float]) -> List[Tuple[float, float]]:
    """
    Ruft die ORS-API auf und gibt eine Liste von (lat, lon)-Punkten zurück.
    :param start: (lat, lon)
    :param end:   (lat, lon)
    :return: Liste von Wegpunkten
    """
    if ORS_API_KEY is None:
        raise RuntimeError("OpenRouteService API key nicht gesetzt in ORS_API_KEY")

    # OpenRouteService erwartet lon,lat
    start_str = f"{start[1]},{start[0]}"
    end_str   = f"{end[1]},{end[0]}"

    params = {
        "api_key": ORS_API_KEY,
        "start":   start_str,
        "end":     end_str
    }
    try:
        resp = requests.get(ORS_BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Fehler beim ORS-Request: {e}")

    data = resp.json()

    #printe das json in lesbarer form
    import json
    print(json.dumps(data, indent=2))


    # GeoJSON FeatureCollection → erstes Feature → geometry.coordinates
    coords: List[List[float]] = data["features"][0]["geometry"]["coordinates"]
    # Umwandeln in List[Tuple[lat, lon]]
    route: List[Tuple[float, float]] = [(lat, lon) for lon, lat in coords]
    return route
