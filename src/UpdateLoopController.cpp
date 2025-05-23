#include "UpdateLoopController.h"

#include <iostream>
#include <vector>
#include <thread>
#include <chrono>
#include <ctime>

#include "PositionTracker.h"
#include "DestinationManager.h"
#include "RoutePlanner.h"
#include "SpeedAdvisor.h"
// #include "LEDController.h"

UpdateLoopController::UpdateLoopController(const TrafficLightFetcher& fetcher)
    : fetcher_(fetcher) {}

void UpdateLoopController::start_loop() {
    while (true) {
        update_cycle();
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

void UpdateLoopController::update_cycle() {
    // 1. Aktuelle Position holen
    auto current_position = PositionTracker::get_current_position();
    // set dummy current position
    current_position = {50.937720f, 6.924954f}; // Köln Dom
    // 2. Zielposition abrufen
    auto destination = DestinationManager::get_destination();

    // 3. Route berechnen
    auto route = RoutePlanner::compute_route(current_position, destination);

    // 4. Relevante Ampeln auf der Route ziehen
    auto traffic_lights = fetcher_.get_relevant_traffic_lights(route);

    if (traffic_lights.empty()) {
        std::cout << "Keine relevanten Ampeln auf der Route gefunden.\n";
        return;
    }

    // 5. Nächste Ampel bestimmen
    TrafficLight next_light = get_next_traffic_light(current_position, traffic_lights);

    // 6. Nächste Grünphase abrufen (Simulation / Zeitmodell)
    auto now = std::chrono::system_clock::now();
    auto green_window = next_light.get_next_green_phase(now);

    // 7. Optimale Geschwindigkeit berechnen
    float v_opt = SpeedAdvisor::compute_optimal_speed(current_position, next_light, green_window);

    // 8. Aktuelle Geschwindigkeit messen
    float v_actual = SpeedAdvisor::get_current_speed();

    // 9. Differenz berechnen
    float v_diff = SpeedAdvisor::calculate_speed_diff(v_opt, v_actual);

    // 10. In Signal übersetzen
    std::string instruction = SpeedAdvisor::translate_to_instruction(v_diff);

    // 11. Signal anzeigen
    // LEDController::output(instruction);

    std::cout << "V_optimal=" << v_opt << " | V_actual=" << v_actual
              << " -> " << instruction << std::endl;
}

TrafficLight UpdateLoopController::get_next_traffic_light(
    const std::pair<float, float>& pos,
    const std::vector<TrafficLight>& lights) {

    // Einfachste Version: wähle erste Ampel
    return lights[0];

    // TODO: bessere Auswahl basierend auf Entfernung & Richtung
}
