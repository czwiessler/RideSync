import matplotlib.pyplot as plt
from typing import List
from TrafficLight import TrafficLight
from datetime import timedelta

def plot_route(
        route,
        current_pos=None,
        destination=None,
        traffic_lights: List[TrafficLight]=None,
        conserved_start_point_for_plausible_plotting=None,
        duration: timedelta=None):

    if not route:
        print("Keine Route zum Plotten übergeben.")
        return

    lats, lons = zip(*route)

    plt.figure(figsize=(6, 8))
    plt.plot(lons, lats, marker='o', linestyle='-', linewidth=2, label="Route")

    # Startpunkt: blauer 's'-Marker
    if conserved_start_point_for_plausible_plotting:
        plt.plot(
            conserved_start_point_for_plausible_plotting[1],
            conserved_start_point_for_plausible_plotting[0],
            marker='s',
            color='blue',
            markersize=8,
            label="Start"
        )


    if traffic_lights and duration is not None:
        now = duration
        for tl in traffic_lights:
            if not tl.mock_initialized:
                continue  # Ampel wurde noch nicht konfiguriert

            lat, lon = tl.get_location()
            phase, remaining_td = tl.get_phase(now)
            remaining = int(remaining_td.seconds)

            color = 'green' if phase == 'green' else 'red'
            plt.plot(lon, lat, marker='o', markersize=14, color=color)

            # Restzeit als Text neben der Ampel
            plt.text(
                lon + 0.0001, lat + 0.0001,
                f"{remaining}s",
                fontsize=10,
                color=color,
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1.0)
            )


    # Aktuelle Position: grün
    if current_pos:
        plt.plot(current_pos[1], current_pos[0], 'go', label="Aktuelle Position")

    # Ziel: rot
    if destination:
        plt.plot(destination[1], destination[0], 'ro', label="Ziel")

    if duration is not None:
        plt.text(
            0.01, 0.01,
            f"Zeit: {duration}s",
            transform=plt.gca().transAxes,
            fontsize=12,
            verticalalignment='bottom',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
        )

    plt.title("Visualisierung der Route")
    plt.xlabel("Längengrad (x)")
    plt.ylabel("Breitengrad (y)")
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.tight_layout()
    plt.show()

# # Beispielaufruf:
# route = [
#     (50.93802, 6.925029),
#     (50.938858, 6.925349),
#     (50.939669, 6.925645),
#     (50.939919, 6.925739),
#     (50.941446, 6.926293),
#     (50.942107, 6.926531),
#     (50.942628, 6.926753),
#     (50.942879, 6.926919),
#     (50.944136, 6.927853),
#     (50.944464, 6.928107),
# ]
#
# traffic_lights = [
#     (50.9396246, 6.9256272),
#     (50.9425, 6.9267)
# ]
#
# current_position = (50.9395, 6.9256)
# destination = (50.944464, 6.928107)
#
# plot_route(route, current_pos=current_position, destination=destination, traffic_lights=traffic_lights)
