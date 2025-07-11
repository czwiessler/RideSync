# src/main.py
"""
Hauptskript für den Grünen-Welle-Assistenten.
"""
import sys
from DestinationManager import DestinationManager
from TrafficLightFetcher import TrafficLightFetcher
from UpdateLoopController import UpdateLoopController
from Cyclist import Cyclist
from Speedometer import Speedometer


def main():
    print("Grüne-Welle-Assistent startet...")

    # === Startposition setzen ===
    try:
        user_input = "u"#input("Bitte Startkoordinaten eingeben (Latitude Longitude): ")
        lat_str, lon_str = user_input.strip().split()
        lat_start, lon_start = float(lat_str), float(lon_str)
    except (ValueError, IndexError):
        print("Ungültige Eingabe. Standardstartposition wird verwendet.", file=sys.stderr)
        lat_start, lon_start = 50.948172, 6.932064

    # === Ziel setzen ===
    try:
        user_input = "u"#input("Bitte Zielkoordinaten eingeben (Latitude Longitude): ")
        lat_str, lon_str = user_input.strip().split()
        lat_end, lon_end = float(lat_str), float(lon_str)
    except (ValueError, IndexError):
        print("Ungültige Eingabe. Standardziel wird verwendet.", file=sys.stderr)
        lat_end, lon_end = 50.939174, 6.925188 #50.944464, 6.928108

    DestinationManager.set_destination((lat_end, lon_end))
    print(f"Ziel gesetzt: {lat_end}, {lon_end}")

    # TrafficLightFetcher vorbereiten
    fetcher = TrafficLightFetcher()
    if not fetcher.load_from_json("src/traffic_lights_venloer_bis_aachener.json"):
        print("Konnte traffic_lights_venloer_bis_aachener.json nicht laden.", file=sys.stderr)
        sys.exit(1)

    speedometer = Speedometer(2.1)
    cyclist = Cyclist(speedometer)

    # === Hauptkontrollschleife starten ===
    controller = UpdateLoopController(fetcher, cyclist)
    controller.start_loop()


if __name__ == "__main__":
    main()
