# position_tracker.py
"""
Python-Übersetzung von PositionTracker (C++).
Holt aktuell GPS-Position im Mock-Modus.
"""

from typing import Tuple


class PositionTracker:
    @staticmethod
    def get_current_position() -> Tuple[float, float]:
        """
        Liefert die aktuelle GPS-Position.
        Aktuell im Mock-Modus: Beispielkoordinaten für den Kölner Dom.

        :return: Tuple[float, float] mit (latitude, longitude)
        """
        # === Mock-Modus ===
        latitude: float = 50.9375  # Beispiel: Köln Dom
        longitude: float = 6.9603
        return (latitude, longitude)

        # === Original TinyGPS++-Logik (später) ===
        # import gpsd
        # packet = gpsd.get_current()
        # if packet.mode >= 2:
        #     return (packet.lat, packet.lon)
        # else:
        #     raise RuntimeError("Ungültige GPS-Position")
