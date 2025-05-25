# destination_manager.py
"""
Verwaltet global gespeicherte Zielkoordinaten (Latitude, Longitude).
"""

from typing import Tuple


class DestinationManager:
    _destination: Tuple[float, float] = (0.0, 0.0)

    @classmethod
    def set_destination(cls, destination: Tuple[float, float]) -> None:
        """
        Setzt das Ziel (Breitengrad, Längengrad).

        :param destination: Tuple[float, float] mit (latitude, longitude)
        """
        cls._destination = destination

    @classmethod
    def get_destination(cls) -> Tuple[float, float]:
        """
        Gibt das aktuell gesetzte Ziel zurück.

        :return: Tuple[float, float] mit (latitude, longitude)
        """
        return cls._destination
