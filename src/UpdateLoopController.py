#UpdateLoopController.py

import time
from datetime import datetime
from typing import List, Tuple, Optional
from datetime import timedelta

from PositionTracker import PositionTracker
from DestinationManager import DestinationManager
from RoutePlanner import compute_route
from TrafficLightFetcher import TrafficLightFetcher
from SpeedAdvisor import SpeedAdvisor
from TrafficLight import TrafficLight
from TrafficLightSelector import TrafficLightSelector
from Cyclist import Cyclist
from utils import haversine_along_route


class UpdateLoopController:
    def __init__(self, tl_fetcher: TrafficLightFetcher, cyclist:Cyclist) -> None:
        self.cyclist = cyclist
        self.tl_fetcher = tl_fetcher
        self.tl_selector = TrafficLightSelector()
        self.last_next_light: Optional[TrafficLight] = None
        self.updateTrigger = 0
        self.duration = timedelta(seconds=0)
        self.firstStart = True
        self.initTime = datetime.now()

    def start_loop(self) -> None:
        old_route: List[Tuple[float, float]] = []
        time_step = timedelta(seconds=1)
        print(f"Aktuelle Position: {self.cyclist.get_current_position()}")
        while True:
            old_route = self.update_cycle(self.duration, time_step, old_route)
            time.sleep(time_step.seconds)
            self.duration = datetime.now() - self.initTime# + timedelta(seconds=57)

    def update_cycle(self, duration: timedelta, time_step: timedelta, old_route):
        #TODO später entfernen: mock-zeile zum start der Testläufe
        while(self.cyclist.get_current_position()[0] == 0.0):
            time.sleep(5)
        if(self.firstStart):
            input("Press enter to continue")
            self.firstStart = False
            self.initTime = datetime.now()
            #duration = timedelta(seconds=60)
        current_position = self.cyclist.get_current_position()

        #nur damit die plot achsen sich nicht immer ändern
        conserved_start_point_for_plausible_plotting = current_position


        #if duration.seconds == 60 and current_position[0] != 0.0 and current_position[1] != 0.0:
        if duration.seconds == 0.0 and current_position[0] != 0.0 and current_position[1] != 0.0:
            destination: Tuple[float, float] = DestinationManager.get_destination()
            old_route: List[Tuple[float, float]] = compute_route(current_position, destination)
            self.tl_selector.set_route(old_route)
        
        destination = DestinationManager.get_destination()
        if(self.updateTrigger  >= 30):
            route = compute_route(current_position, destination)
            self.updateTrigger  = 0
            old_route = route
            self.tl_selector.set_route(route)
        else:
            route = old_route
        self.updateTrigger  = self.updateTrigger  + 1
        

        traffic_lights: List[TrafficLight] = self.tl_fetcher.get_relevant_traffic_lights(route)
        if not traffic_lights:
            return old_route

        next_light = self.tl_selector.get_next_traffic_light(current_position, traffic_lights)
        if next_light is None:
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


        v_actual = self.cyclist.get_current_speed()
        print(f"aktuelle Geschwindigkeit: {v_actual}")

        try:
            advisor = SpeedAdvisor()
            delay, v_opt, distance = advisor.choose_best_phase_and_speed(
                current_position=current_position,
                next_light=next_light,
                green_starts=next_light.get_next_green_starts(duration),
                now=duration,
                preferred_speed=self.cyclist.preferred_speed,
                min_speed=self.cyclist.min_speed,
                max_speed=self.cyclist.max_speed
            )
            print(f"delay: {delay}, v_opt: {v_opt}, distance: {distance}")
            self.cyclist.set_advicde_speed(v_opt * 3.6, distance)
            print(f"delay bis zur nächsten Grünphase: {delay}, optimale Geschwindigkeit: {v_opt * 3.6}")

            #DEBUG block start#####################################################################################
            # Berechne die Geschwindigkeitsdifferenz und übersetze sie in eine Anweisung
            def calculate_speed_diff(v_opt: float, v_actual: float) -> float:
                return v_opt - v_actual
            def translate_to_instruction(v_diff: float) -> str:
                if v_diff > 0.01: # kleine Toleranz, um Rundungsfehler zu vermeiden
                    return f"Beschleunige um {v_diff * 3.6 :.2f} km/h, um die Ampel zu erreichen."
                elif v_diff < -0.01: # kleine Toleranz, um Rundungsfehler zu vermeiden
                    return f"Reduziere die Geschwindigkeit um {-v_diff * 3.6:.2f} km/h, um die Ampel nicht zu überfahren."
                else:
                    return "Halte deine aktuelle Geschwindigkeit bei."

            print(translate_to_instruction(calculate_speed_diff(v_opt, v_actual)))
        # DEBUG block ende#####################################################################################
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Skipped one cycle")

        # plot_route(
        #     route=route,
        #     current_pos=current_position,
        #     v_actual=v_actual,
        #     distance_to_next_tl=distance_to_next_tl,
        #     destination=destination,
        #     traffic_lights=traffic_lights,
        #     conserved_start_point_for_plausible_plotting=conserved_start_point_for_plausible_plotting,
        #     duration=duration,
        # )

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
