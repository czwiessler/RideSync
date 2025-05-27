# src/main.py
"""
Hauptskript für den Grünen-Welle-Assistenten.
"""
import sys
from DestinationManager import DestinationManager
from TrafficLightFetcher import TrafficLightFetcher
from UpdateLoopController import UpdateLoopController
from src.PositionTracker import PositionTracker


def main():
    print("Grüne-Welle-Assistent startet...")

    # === Ziel setzen ===
    try:
        user_input = "u"#input("Bitte Zielkoordinaten eingeben (Latitude Longitude): ")
        lat_str, lon_str = user_input.strip().split()
        lat, lon = float(lat_str), float(lon_str)
    except (ValueError, IndexError):
        print("Ungültige Eingabe. Standardziel wird verwendet.", file=sys.stderr)
        lat, lon = 50.939174, 6.925188 #50.944464, 6.928108

    DestinationManager.set_destination((lat, lon))
    print(f"Ziel gesetzt: {lat}, {lon}")

    print(f"Aktuelle Position: {PositionTracker.get_current_position()}") #TODO fertig schreiben)

    # TrafficLightFetcher vorbereiten
    fetcher = TrafficLightFetcher()
    if not fetcher.load_from_json("src/traffic_light.json"):
        print("Konnte traffic_light.json nicht laden.", file=sys.stderr)
        sys.exit(1)

    # === Hauptkontrollschleife starten ===
    controller = UpdateLoopController(fetcher)
    controller.start_loop()


if __name__ == "__main__":
    main()
