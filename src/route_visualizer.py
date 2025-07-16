from datetime import timedelta
from typing import List

import contextily as ctx
import matplotlib.pyplot as plt
from pyproj import Transformer

from TrafficLight import TrafficLight

# Transformer von WGS84 (lat/lon) nach Web Mercator (EPSG:3857)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)


def plot_route(
    route,
    current_pos=None,
    v_actual=None,
    distance_to_next_tl=None,
    destination=None,
    traffic_lights: List[TrafficLight] = None,
    conserved_start_point_for_plausible_plotting=None,
    duration: timedelta = None
):
    if not route:
        print("Keine Route zum Plotten übergeben.")
        return

    # Originalkoordinaten extrahieren
    lats, lons = zip(*route)
    # In Web Mercator transformieren
    xs, ys = transformer.transform(lons, lats)

    fig, ax = plt.subplots(figsize=(6, 8))

    # Basemap aus OpenStreetMap
    ax.set_aspect('equal')
    # Setze Extent auf den Routenbereich
    margin = 100  # Meter Rand
    x_min, x_max = min(xs) - margin, max(xs) + margin
    y_min, y_max = min(ys) - margin, max(ys) + margin
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

    # Route als Polyline
    ax.plot(xs, ys, marker='o', linestyle='-', linewidth=2, label="Route")

    # Startpunkt: blaues Quadrat
    if conserved_start_point_for_plausible_plotting:
        sx, sy = transformer.transform(
            conserved_start_point_for_plausible_plotting[1],
            conserved_start_point_for_plausible_plotting[0]
        )
        ax.plot(sx, sy, marker='s', color='blue', markersize=8, label="Start")

    # Ampeln mit Phase
    if traffic_lights and duration is not None:
        now = duration
        for tl in traffic_lights:
            if not tl.mock_initialized:
                continue
            lat, lon = tl.get_location()
            tx, ty = transformer.transform(lon, lat)
            phase, remaining_td = tl.get_phase(now)
            remaining = int(remaining_td.total_seconds())
            color = 'green' if phase == 'green' else 'red'
            ax.plot(tx, ty, marker='o', markersize=14, color=color)
            ax.text(
                tx + 10, ty + 10,
                f"{remaining}s",
                fontsize=10,
                color=color,
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1.0)
            )

    # Aktuelle Position
    if current_pos:
        px, py = transformer.transform(current_pos[1], current_pos[0])
        ax.plot(px, py, 'go', label="Aktuelle Position")
        if v_actual is not None:
            ax.text(
                px + 10, py + 10,
                f"{v_actual:.2f} m/s",
                fontsize=10,
                color='green',
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1.0)
            )

    # Ziel
    if destination:
        dx, dy = transformer.transform(destination[1], destination[0])
        ax.plot(dx, dy, 'ro', label="Ziel")

    # Duration und Entfernung
    if duration is not None:
        ax.text(
            0.01, 0.01,
            f"Zeit: {duration.seconds}s",
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment='bottom',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
        )
    if distance_to_next_tl is not None:
        ax.text(
            0.99, 0.01,
            f"Entfernung zur nächsten Ampel:\n{distance_to_next_tl:.1f} m",
            transform=ax.transAxes,
            fontsize=11,
            verticalalignment='bottom',
            horizontalalignment='right',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
        )

    ax.set_title("Visualisierung der Route")
    ax.set_xlabel("Web Mercator X")
    ax.set_ylabel("Web Mercator Y")
    ax.legend()
    plt.tight_layout()
    plt.show()
