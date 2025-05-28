#UpdateLoopController.py

import sys
import time
from typing import List, Tuple, Optional
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from route_visualizer import plot_route

from PositionTracker import PositionTracker
from DestinationManager import DestinationManager
from RoutePlanner import compute_route
from TrafficLightFetcher import TrafficLightFetcher
from SpeedAdvisor import SpeedAdvisor
from TrafficLight import TrafficLight #, Phase
from TrafficLightSelector import TrafficLightSelector
from MockedCyclist import MockedCyclist
from utils import haversine_along_route


class UpdateLoopController:
    def __init__(self, tl_fetcher: TrafficLightFetcher) -> None:
        self.mocked_cyclist = MockedCyclist(start_position=(50.948172, 6.932064))
        self.tl_fetcher = tl_fetcher
        self.tl_selector = TrafficLightSelector()
        self.last_next_light: Optional[TrafficLight] = None

        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(6, 8))
        self.duration = timedelta(seconds=0)

    def start_loop(self) -> None:
        old_route: List[Tuple[float, float]] = []
        time_step = timedelta(seconds=1)
        while True:
            old_route = self.update_cycle(self.duration, time_step, old_route)
            plt.pause(0.1)
            time.sleep(time_step.seconds)
            self.duration += timedelta(seconds=1)

    def update_cycle(self, duration: timedelta, time_step: timedelta, old_route):
        current_position = (50.948172, 6.932064)

        #nur damit die plot achsen sich nicht immer ändern
        conserved_start_point_for_plausible_plotting = current_position


        if duration.seconds == 0:
            destination: Tuple[float, float] = DestinationManager.get_destination()
            old_route: List[Tuple[float, float]] = compute_route(current_position, destination)
            self.tl_selector.set_route(old_route)

        tracker = PositionTracker()
        current_position = tracker.get_current_position_mock(self.mocked_cyclist, old_route, time_elapsed=time_step)

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

        if not next_light.mock_initialized:
            print(f"\nNeue Ampel erkannt: {next_light.get_id()}")

            #########################
            # TODO unkommentieren, wenn phasen wieder in der eingabe gemockt werden sollen. (dann letzte zeile weg)
            # try:
            #     green = int(input("Grünphase in Sekunden (Default 10): ") or "10")
            #     red = int(input("Rotphase in Sekunden (Default 40): ") or "40")
            #     offset = int(input("Offset in Sekunden (Default 0): ") or "0")
            # except ValueError:
            #     print("Ungültige Eingabe, verwende Defaults.")
            #     green, red, offset = 10, 40, 0
            green, red, offset = 10, 20, 0
            ##########################

            next_light.green_duration = timedelta(seconds=green)
            next_light.red_duration = timedelta(seconds=red)
            next_light.offset = timedelta(seconds=offset)
            next_light.mock_initialized = True

        distance_to_next_tl = haversine_along_route(
            start_point=current_position,
            end_point=next_light.get_location(),
            route=route
        )


        v_actual = self.mocked_cyclist.get_current_speed()
        print(f"aktuelle Geschwindigkeit: {v_actual}")

        advisor = SpeedAdvisor()
        delay, v_opt = advisor.choose_best_phase_and_speed(
            current_position=current_position,
            next_light=next_light,
            green_starts=next_light.get_next_green_starts(duration),
            now=duration,
            preferred_speed=self.mocked_cyclist.preferred_speed,
            min_speed=self.mocked_cyclist.min_speed,
            max_speed=self.mocked_cyclist.max_speed
        )
        print(f"delay bis zur nächsten Grünphase: {delay}, optimale Geschwindigkeit: {v_opt}")

        # Berechne die Geschwindigkeitsdifferenz und übersetze sie in eine Anweisung
        def calculate_speed_diff(v_opt: float, v_actual: float) -> float:
            return v_opt - v_actual
        def translate_to_instruction(v_diff: float) -> str:
            if v_diff > 0:
                return f"Beschleunige um {v_diff:.2f} m/s, um die Ampel zu erreichen."
            elif v_diff < 0:
                return f"Reduziere die Geschwindigkeit um {-v_diff:.2f} m/s, um die Ampel nicht zu überfahren."
            else:
                return "Halte deine aktuelle Geschwindigkeit bei."

        instruction = translate_to_instruction(calculate_speed_diff(v_opt, v_actual))

        self.mocked_cyclist.choose_velocity(v_opt)

        self.ax.cla()

        plot_route(
            route=route,
            current_pos=current_position,
            v_actual=v_actual,
            distance_to_next_tl=distance_to_next_tl,
            destination=destination,
            traffic_lights=traffic_lights,
            conserved_start_point_for_plausible_plotting=conserved_start_point_for_plausible_plotting,
            duration=duration,
        )

        # self.ax.text(
        #     0.99, 0.01,  # unten rechts
        #     f"{instruction}\nZielspeed: {v_opt:.2f} m/s",
        #     transform=self.ax.transAxes,
        #     fontsize=12,
        #     verticalalignment='bottom',
        #     horizontalalignment='right',
        #     bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
        # )

        self.last_next_light = next_light
        return old_route
