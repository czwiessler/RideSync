# speed_advisor.py
"""
Berechnet optimale Geschwindigkeit für die nächste Grünphase und gibt Anweisungen.
"""

from typing import Tuple, List
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
    print(f"Ampel-Entfernung: {distance_m:.2f} m")
    print(f"Zeit bis Grünstart: {time_until_start:.2f} s")
    print(f"Zeit bis Grünende: {time_until_end:.2f} s")
    print(f"v_min: {v_min:.2f}, v_max: {v_max:.2f}, v_opt: {v_opt:.2f}")

    return v_opt


# Innerhalb speed_advisor.py

PREFERRED_SPEED = 6.0  # dein „optimaler“ Speed in m/s

def choose_best_phase_and_speed(
    current_position: Tuple[float, float],
    light: 'TrafficLight',
    green_phases: List[Phase],
    preferred_speed: float = PREFERRED_SPEED
) -> Tuple[Phase, float]:
    """
    Wählt aus allen kommenden Grünphasen diejenige aus, deren
    benötigte Geschwindigkeit am nächsten an preferred_speed liegt.
    Gibt (gewählte Phase, Zielgeschwindigkeit) zurück.
    """
    now = datetime.datetime.now()
    best_phase = None
    best_v = None
    best_cost = float('inf')

    dist = haversine_distance(
        current_position[0], current_position[1],
        *light.get_location()
    )

    for start, end in green_phases:
        # Phase schon vorbei?
        if now >= end:
            continue

        # 1) Entscheidung, auf welchen Zeitpunkt timen:
        if now < start:
            target_time = start + (end - start) / 2
        else:
            target_time = end

        t = max((target_time - now).total_seconds(), 1.0)
        v_req = dist / t

        # 2) Kostenfunktionen
        #   – Basis: Abstand zum Wunschwert
        cost = abs(v_req - preferred_speed)
        #   – Extra-Strafe, wenn gerade unplausibel schnell/langsam
        if v_req < MIN_SPEED or v_req > MAX_SPEED:
            cost += 1000.0

        # 3) Bester Kandidat?
        if cost < best_cost:
            best_cost = cost
            best_phase = (start, end)
            best_v = v_req

    # Falls keine Phase mehr, Vollgas
    if best_phase is None:
        return (now, now), MAX_SPEED

    # Begrenze Zielgeschwindigkeit auf erlaubte Range
    v_opt = max(min(best_v, MAX_SPEED), MIN_SPEED)
    return best_phase, v_opt





def get_current_speed() -> float:
    """
    Holt die aktuelle Geschwindigkeit (Mock).

    :return: Geschwindigkeit in m/s
    """
    # TODO: Tachomodul integrieren
    return 100.0  # 5 m/s ≈ 18 km/h


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
