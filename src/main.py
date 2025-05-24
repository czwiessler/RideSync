# src/main.py
"""
Hauptskript für den Grünen-Welle-Assistenten.
"""
import sys
from DestinationManager import DestinationManager
from TrafficLightFetcher import TrafficLightFetcher
from UpdateLoopController import UpdateLoopController


def main():
    print("Grüne-Welle-Assistent startet...")

    # === Ziel setzen ===
    try:
        user_input = input("Bitte Zielkoordinaten eingeben (Latitude Longitude): ")
        lat_str, lon_str = user_input.strip().split()
        lat, lon = float(lat_str), float(lon_str)
    except (ValueError, IndexError):
        print("Ungültige Eingabe. Standardziel wird verwendet.", file=sys.stderr)
        lat, lon = 50.948270, 6.932673  # Standard: Köln Dom

    DestinationManager.set_destination((lat, lon))
    print(f"Ziel gesetzt: {lat}, {lon}")

    # TrafficLightFetcher vorbereiten
    fetcher = TrafficLightFetcher()
    if not fetcher.load_from_json("traffic_light.json"):
        print("Konnte traffic_light.json nicht laden.", file=sys.stderr)
        sys.exit(1)

    # === Hauptkontrollschleife starten ===
    controller = UpdateLoopController(fetcher)
    controller.start_loop()


if __name__ == "__main__":
    main()
