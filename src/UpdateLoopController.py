"""
Python-Übersetzung des C++ UpdateLoopController.
Steuert die Hauptschleife: Position erfassen, Route planen, Ampeln filtern, Geschwindigkeit berechnen.
"""
import time
from typing import List, Tuple, Optional
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
from TrafficLightSelector import TrafficLightSelector


class UpdateLoopController:
    def __init__(self, fetcher: TrafficLightFetcher) -> None:
        """
        Initialisiert den Controller mit einem TrafficLightFetcher.
        :param fetcher: Instanz von TrafficLightFetcher mit geladenen Ampeln
        """
        self.fetcher = fetcher
        # Selector für nächste Ampel
        self.selector = TrafficLightSelector()

    def start_loop(self) -> None:
        """
        Startet die Endlosschleife, führt jede Sekunde ein Update durch.
        """
        duration = 0 ## delete if mock is removed
        old_route: List[Tuple[float, float]] = [] ## delete if mock is removed
        while True:
            old_route = self.update_cycle(duration, old_route) ## delete duration and old_route if mock is removed
            time.sleep(1)
            duration = duration + 1

    def update_cycle(self, duration, old_route): ## delete duration and old_route if mock is removed
        """
        Ein Zyklus: Position, Route, Ampeln, Geschwindigkeit, Anweisung.
        """
        # 1. Aktuelle Position holen
        current_position: Tuple[float, float] = PositionTracker.get_current_position()
        current_position = (50.938017, 6.925047)

        ###### MOCK START ## delete if mock is removed
        # current position mocker, drive to destination
        if duration == 0:
            destination: Tuple[float, float] = DestinationManager.get_destination()
            old_route: List[Tuple[float, float]] = compute_route(current_position, destination)
            self.selector.set_route(old_route)
        tracker = PositionTracker()
        current_position: Tuple[float, float] = tracker.get_current_position_mock(old_route, duration)
        #print(current_position)
        ##### MOCK ENDE

        # 2. Ziel abrufen
        destination: Tuple[float, float] = DestinationManager.get_destination()

        # 3. Route berechnen
        route: List[Tuple[float, float]] = compute_route(current_position, destination)

        ###### MOCK START ## delete if mock is removed
        old_route = route
        ###### MOCK ENDE

        # 4. Route im Selector setzen
        self.selector.set_route(route)

        # 5. Relevante Ampeln filtern
        traffic_lights: List[TrafficLight] = self.fetcher.get_relevant_traffic_lights(route)
        if not traffic_lights:
            print("Keine relevanten Ampeln auf der Route gefunden.")
            return

        # 6. Nächste Ampel auswählen
        next_light: Optional[TrafficLight] = self.selector.get_next_traffic_light(
            current_position,
            traffic_lights
        )

        if next_light is None:
            print("Keine nächste Ampel ermittelt.")
            return

        # 7. Nächste Grünphase abrufen
        now = datetime.now()
        green_window: Phase = next_light.get_next_green_phase(now)

        # 8. Optimale Geschwindigkeit berechnen
        v_opt: float = compute_optimal_speed(current_position, next_light, green_window)

        # 9. Aktuelle Geschwindigkeit messen
        v_actual: float = get_current_speed()

        # 10. Differenz berechnen
        v_diff: float = calculate_speed_diff(v_opt, v_actual)

        # 11. In Anweisung übersetzen und ausgeben
        instruction: str = translate_to_instruction(v_diff)
        print(f"V_optimal={v_opt:.2f} m/s | V_actual={v_actual:.2f} m/s -> {instruction}")

        return old_route ## delete if mock is removed
