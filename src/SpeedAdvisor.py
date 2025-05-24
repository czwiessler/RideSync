# speed_advisor.py
"""
Python-Übersetzung der C++-Klasse SpeedAdvisor.
Berechnet optimale Geschwindigkeit für die nächste Grünphase und gibt Anweisungen.
"""

from typing import Tuple
import math
import datetime


# Konstanten (m/s)
MAX_SPEED = 10.0  # ca. 36 km/h
MIN_SPEED = 1.0   # ca. 3.6 km/h

TimePoint = datetime.datetime
Phase = Tuple[TimePoint, TimePoint]


def haversine_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Berechnet die Entfernung (Meter) zwischen zwei Koordinaten via Haversine-Formel.
    """
    R = 6371000.0  # Erdradius in Metern
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) ** 2 + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def compute_optimal_speed(
    current_position: Tuple[float, float],
    light: 'TrafficLight',
    green_phase: Phase
) -> float:
    """
    Berechnet die optimale Geschwindigkeit (m/s), um die nächste Grünphase zu erreichen.

    :param current_position: Tuple (lat, lon)
    :param light: TrafficLight-Objekt
    :param green_phase: Tuple (start_time, end_time)
    :return: Optimale Geschwindigkeit in m/s
    """
    now = datetime.datetime.now()
    start_time, end_time = green_phase

    distance_m = haversine_distance(
        current_position[0], current_position[1],
        *light.get_location()
    )

    time_until_start = (start_time - now).total_seconds()
    time_until_end = (end_time - now).total_seconds()

    if time_until_end <= 0:
        return MAX_SPEED  # Grün vorbei → Vollgas

    v_min = distance_m / max(time_until_end, 1.0)
    v_max = distance_m / max(time_until_start, 1.0)

    v_opt = (v_min + v_max) / 2.0
    v_opt = max(min(v_opt, MAX_SPEED), MIN_SPEED)
    return v_opt


def get_current_speed() -> float:
    """
    Holt die aktuelle Geschwindigkeit (Mock).

    :return: Geschwindigkeit in m/s
    """
    # TODO: Tachomodul integrieren
    return 5.0  # 5 m/s ≈ 18 km/h


def calculate_speed_diff(target_speed: float, current_speed: float) -> float:
    """
    Berechnet die Differenz: Zielgeschwindigkeit – Istgeschwindigkeit.

    :return: Differenz in m/s
    """
    return target_speed - current_speed


def translate_to_instruction(speed_diff: float) -> str:
    """
    Übersetzt die Geschwindigkeitsdifferenz in eine Anweisung.

    :return: "Halte Geschwindigkeit", "Beschleunigen" oder "Verlangsamen"
    """
    if abs(speed_diff) < 0.5:
        return "Halte Geschwindigkeit"
    elif speed_diff > 0.5:
        return "Beschleunigen"
    else:
        return "Verlangsamen"
