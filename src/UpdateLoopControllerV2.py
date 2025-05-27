import sys
import time
from typing import List, Tuple, Optional
from datetime import datetime

import matplotlib.pyplot as plt
from route_visualizer import plot_route

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
    def __init__(self, tl_fetcher: TrafficLightFetcher) -> None:
        self.tl_fetcher = tl_fetcher
        self.tl_selector = TrafficLightSelector()
        self.last_next_light: Optional[TrafficLight] = None

        # Interaktiver Matplotlib-Modus für Live-Updates
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(6, 8))

    def start_loop(self) -> None:
        duration = 0
        old_route: List[Tuple[float, float]] = []
        while True:
            old_route = self.update_cycle(duration, old_route)
            plt.pause(0.1)  # Zeit für Matplotlib-Update
            time.sleep(1)
            duration += 1

    def update_cycle(self, duration, old_route):
        current_position: Tuple[float, float] = PositionTracker.get_current_position()
        current_position = (50.948172, 6.932064)

        #nur damit die plot achsen sich nicht immer ändern
        conserved_start_point_for_plausible_plotting = current_position

        if duration == 0:
            destination: Tuple[float, float] = DestinationManager.get_destination()
            old_route: List[Tuple[float, float]] = compute_route(current_position, destination)
            self.tl_selector.set_route(old_route)

        tracker = PositionTracker()
        current_position = tracker.get_current_position_mock(old_route, duration)

        destination = DestinationManager.get_destination()
        route = compute_route(current_position, destination)
        old_route = route
        self.tl_selector.set_route(route)

        traffic_lights: List[TrafficLight] = self.tl_fetcher.get_relevant_traffic_lights(route)
        if not traffic_lights:
            self.ax.cla()
            self.ax.set_title("Keine relevanten Ampeln gefunden")
            return old_route

        next_light = self.tl_selector.get_next_traffic_light(current_position, traffic_lights)
        if next_light is None:
            self.ax.cla()
            self.ax.set_title("Keine nächste Ampel ermittelt")
            return old_route

        phase, v_opt = choose_best_phase_and_speed(
            current_position,
            next_light,
            next_light.green_phases
        )

        v_actual = get_current_speed()
        v_diff = calculate_speed_diff(v_opt, v_actual)
        instruction = translate_to_instruction(v_diff)

        # === Visualisierung ===
        self.ax.cla()  # vorherigen Plot löschen

        # Ampelpositionen extrahieren
        traffic_coords = [tl.get_location() for tl in traffic_lights]

        # Plot aktualisieren
        plot_route(
            route=route,
            current_pos=current_position,
            destination=destination,
            traffic_lights=traffic_coords,
            conserved_start_point_for_plausible_plotting=conserved_start_point_for_plausible_plotting,
        )

        # Geschwindigkeitsanweisung als Text anzeigen
        self.ax.text(
            0.01, 0.99,
            f"{instruction}\nZielspeed: {v_opt:.2f} m/s",
            transform=self.ax.transAxes,
            fontsize=12,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
        )

        self.last_next_light = next_light
        return old_route
