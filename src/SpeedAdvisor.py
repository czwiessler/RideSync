from typing import Tuple, List
from datetime import timedelta

from utils import haversine
from TrafficLight import TrafficLight


class SpeedAdvisor:
    """
    Ermittelt die optimale Geschwindigkeit, um eine bestimmte Grünphase einer Ampel zu erreichen.
    """

    def __init__(self):
        """
        Initialisiert den SpeedAdvisor.
        """
        pass

    def choose_best_phase_and_speed(
        self,
        current_position: Tuple[float, float],
        next_light: TrafficLight,
        green_starts: List[timedelta],
        now: timedelta,
        preferred_speed: float,
        min_speed: float,
        max_speed: float
    ) -> Tuple[timedelta, float, float]:
        """
        Wählt die beste erreichbare Phase, prüft zuerst die aktuelle Phase.

        Gibt zurück:
        - Verzögerung bis Beginn der gewählten Grünphase (0 für aktuelle Grünphase)
        - Empfohlene Geschwindigkeit (m/s)
        """
        # Entfernung zur Ampel (in Metern)
        distance = haversine(current_position, next_light.get_location())

        # 1. Prüfe aktuelle Phase
        phase, remaining = next_light.get_phase(now)
        if phase == 'green' and remaining.total_seconds() > 0:
            max_time = remaining.total_seconds()

            # Wie lange bräuchte man mit preferred_speed?
            time_with_preferred = distance / preferred_speed

            if time_with_preferred <= max_time:
                # preferred_speed reicht aus – perfekt!
                return timedelta(seconds=0), preferred_speed, distance
            else:
                # Prüfe, ob man überhaupt noch rechtzeitig ankommen kann
                time_with_max_speed = distance / max_speed
                if time_with_max_speed <= max_time:
                    # Mit max_speed gerade noch erreichbar
                    speed_required = distance / max_time
                    return timedelta(seconds=0), max(min_speed, min(speed_required, max_speed)), distance
                # → Ansonsten: aktuelle Grünphase nicht mehr erreichbar – weiter mit zukünftigen Phasen


        # 2. Sonst prüfe kommende Grünphasen
        candidates: List[Tuple[float, timedelta, float]] = []  # (Abweichung, delay, speed_required)
        for delay in green_starts:
            if delay.total_seconds() <= 0:
                continue
            speed_required = distance / delay.total_seconds()
            deviation = abs(speed_required - preferred_speed)
            candidates.append((deviation, delay, speed_required))

        if not candidates:
            # Keine kommenden Phasen: Behalte preferred_speed
            return timedelta(seconds=0), preferred_speed, distance

        # Wähle Phase mit geringster Abweichung
        _, best_delay, best_speed = min(candidates, key=lambda x: x[0])
        # Auf min/max begrenzen
        chosen_speed = max(min_speed, min(best_speed, max_speed))
        return best_delay, chosen_speed, distance

