# update_loop_controller.py
"""
Python-Übersetzung des C++ UpdateLoopController.
Steuert die Hauptschleife: Position erfassen, Route planen, Ampeln filtern, Geschwindigkeit berechnen.
"""
import time
from typing import List, Tuple
from datetime import datetime

from PositionTracker import PositionTracker
from DestinationManager import DestinationManager
from RoutePlanner import compute_route
from TrafficLightFetcher import TrafficLightFetcher
from SpeedAdvisor import (
    compute_optimal_speed,
    get_current_speed,
    calculate_speed_diff,
    translate_to_instruction,
)
from TrafficLight import TrafficLight, Phase


class UpdateLoopController:
    def __init__(self, fetcher: TrafficLightFetcher) -> None:
        """
        Initialisiert den Controller mit einem TrafficLightFetcher.
        :param fetcher: Instanz von TrafficLightFetcher mit geladenen Ampeln
        """
        self.fetcher = fetcher

    def start_loop(self) -> None:
        """
        Startet die Endlosschleife, führt jede Sekunde ein Update durch.
        """
        while True:
            self.update_cycle()
            time.sleep(1)

    def update_cycle(self) -> None:
        """
        Ein Zyklus: Position, Route, Ampeln, Geschwindigkeit, Anweisung.
        """
        # 1. Aktuelle Position holen (Mock)
        current_position: Tuple[float, float] = PositionTracker.get_current_position()
        # Setze Dummy-Position (optional override)
        current_position = (50.937720, 6.924954)  # Köln Dom

        # 2. Ziel abrufen
        destination: Tuple[float, float] = DestinationManager.get_destination()

        # 3. Route berechnen
        route: List[Tuple[float, float]] = compute_route(current_position, destination)

        # 4. Relevante Ampeln filtern
        traffic_lights: List[TrafficLight] = self.fetcher.get_relevant_traffic_lights(route)

        if not traffic_lights:
            print("Keine relevanten Ampeln auf der Route gefunden.")
            return

        # 5. Nächste Ampel auswählen
        next_light: TrafficLight = self.get_next_traffic_light(current_position, traffic_lights)

        # 6. Nächste Grünphase abrufen
        now = datetime.now()
        green_window: Phase = next_light.get_next_green_phase(now)

        # 7. Optimale Geschwindigkeit berechnen
        v_opt: float = compute_optimal_speed(current_position, next_light, green_window)

        # 8. Aktuelle Geschwindigkeit messen
        v_actual: float = get_current_speed()

        # 9. Differenz berechnen
        v_diff: float = calculate_speed_diff(v_opt, v_actual)

        # 10. In Anweisung übersetzen
        instruction: str = translate_to_instruction(v_diff)

        # 11. Ausgabe
        print(f"V_optimal={v_opt:.2f} m/s | V_actual={v_actual:.2f} m/s -> {instruction}")

    def get_next_traffic_light(
        self,
        pos: Tuple[float, float],
        lights: List[TrafficLight]
    ) -> TrafficLight:
        """
        Wählt die erste Ampel aus der Liste (MVP).
        TODO: Bessere Auswahl nach Entfernung/Richtung.

        :param pos: Aktuelle Position
        :param lights: Liste relevanter Ampeln
        :return: Gewählte TrafficLight-Instanz
        """
        return lights[0]
