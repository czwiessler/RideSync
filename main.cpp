#include <iostream>
#include "DestinationManager.h"
#include "UpdateLoopController.h"

int main() {
    std::cout << "Grüne-Welle-Assistent startet...\n";

    // === Ziel setzen ===
    float lat = 0.0f;
    float lon = 0.0f;

    std::cout << "Bitte Zielkoordinaten eingeben (Latitude Longitude): ";
    std::cin >> lat >> lon;

    if (std::cin.fail()) {
        std::cerr << "Ungültige Eingabe. Standardziel wird verwendet.\n";
        lat = 50.948270f;  // z. B. Köln Dom
        lon = 6.932673f;
    }

    DestinationManager::set_destination({lat, lon});
    std::cout << "Ziel gesetzt: " << lat << ", " << lon << "\n";

    // TrafficLightFetcher vorbereiten
    TrafficLightFetcher fetcher;
if (!fetcher.load_from_json("C:/Users/Christian.Zwiessler/CLionProjects/RideSync/traffic_light.json")) {
        std::cerr << "Konnte traffic_light.json nicht laden.\n";
        return 1;
    }

    // === Hauptkontrollschleife starten ===
    UpdateLoopController controller(fetcher);
    controller.start_loop();

    return 0;
}
