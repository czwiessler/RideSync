"""
Steuert die Hauptschleife: Position erfassen, Route planen,
Ampeln filtern, Geschwindigkeit berechnen und Events loggen.
"""
import sys
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
    choose_best_phase_and_speed,
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
        # Für Logging der Ampelpassage
        self.last_next_light: Optional[TrafficLight] = None

    def start_loop(self) -> None:
        """
        Startet die Endlosschleife, führt jede Sekunde ein Update durch.
        """
        duration = 0 ## delete if mock is removed
        old_route: List[Tuple[float, float]] = [] ## delete if mock is removed
        while True:
            old_route = self.update_cycle(duration, old_route) ## delete duration and old_route if mock is removed
            time.sleep(1)
            duration += 1

    def update_cycle(self, duration, old_route): ## delete duration and old_route if mock is removed
        """
        Ein Zyklus: Position, Route, Ampeln, Geschwindigkeit, Anweisung,
        plus Logging, wenn eine Ampel passiert wurde.
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
            # letzte Ampel loggen
            if self.last_next_light is not None:
                light = self.last_next_light
                pass_time = datetime.now()
                phase = light.get_next_green_phase(pass_time)
                loc = light.get_location()
                print(
                    "\n=== 🚦 Ampel passiert 🚦 ===\n"
                    f"Standort: {loc}\n"
                    f"Tatsächliche nächste Grünphase: {phase[0].strftime('%d.%m.%Y %H:%M:%S')} bis {phase[1].strftime('%d.%m.%Y %H:%M:%S')}\n"
                    f"Vorbeifahrtszeit: {pass_time.strftime('%d.%m.%Y %H:%M:%S')}\n"
                    "============================\n"
                )
                self.last_next_light = None
            print("Keine relevanten Ampeln auf der Route gefunden.")
            return old_route

        # 6. Nächste Ampel auswählen
        next_light: Optional[TrafficLight] = self.selector.get_next_traffic_light(
            current_position,
            traffic_lights
        )
        if next_light is None:
            print("Keine nächste Ampel ermittelt.")
            return old_route ## delete if mock is removed

        # 7. Prüfen, ob die vorherige Ampel passiert wurde
        if self.last_next_light and next_light.get_location() != self.last_next_light.get_location():
            light = self.last_next_light
            pass_time = datetime.now()
            phase = light.get_next_green_phase(pass_time)
            loc = light.get_location()
            print(
                "\n=== 🚦 Ampel passiert 🚦 ===\n"
                f"Standort: {loc}\n"
                f"Tatsächliche nächste Grünphase: {phase[0].strftime('%d.%m.%Y %H:%M:%S')} bis {phase[1].strftime('%d.%m.%Y %H:%M:%S')}\n"
                f"Vorbeifahrtszeit: {pass_time.strftime('%d.%m.%Y %H:%M:%S')}\n"
                "============================\n"
            )

        # 7. Nächste Grünphase abrufen (für Logging, falls später benötigt)
        now = datetime.now()
        #green_window: Phase = next_light.get_next_green_phase(now)
        # print the next green phase
        #print(f"Nächste Grünphase: {green_window[0]} bis {green_window[1]}")

        # 8. Optimale Phase und Geschwindigkeit bestimmen
        phase, v_opt = choose_best_phase_and_speed(
            current_position,
            next_light,
            next_light.green_phases
        )
        # Gewählte Phase für Geschwindigkeit
        chosen_phase = phase

        # 9. Aktuelle Geschwindigkeit messen
        v_actual: float = get_current_speed()

        # 10. Differenz berechnen
        v_diff: float = calculate_speed_diff(v_opt, v_actual)

        # 11. In Anweisung übersetzen und ausgeben
        instruction: str = translate_to_instruction(v_diff)
        print(
             #f"Gewählte Phase: {phase}, "
              f"Nächste Ampel: {next_light.get_location()}, "
              f"Gewählte Grünphase: {chosen_phase[0].strftime('%H:%M:%S')}–{chosen_phase[1].strftime('%H:%M:%S')}, "
              #f"Aktuelle Geschwindigkeit: {v_actual:.2f} m/s, "
              f"Zielspeed: {v_opt:.2f} m/s → {instruction}, "
              #f"Aktuelle Position: {current_position}, "
              )

        # 12. Für die nächste Iteration merken
        self.last_next_light = next_light
        return old_route ## delete if mock is removed
