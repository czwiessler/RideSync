#include "TrafficLight.h"

TrafficLight::TrafficLight(float lat, float lon, const std::vector<Phase>& phases)
    : latitude(lat), longitude(lon), green_phases(phases) {}

std::pair<float, float> TrafficLight::get_location() const {
    return {latitude, longitude};
}

TrafficLight::Phase TrafficLight::get_next_green_phase(TimePoint current_time) const {
    for (const auto& phase : green_phases) {
        if (current_time < phase.second) {
            return phase;
        }
    }

    // Falls keine gültige Grünphase gefunden: erste Phase am nächsten Tag (z. B. zyklisch)
    if (!green_phases.empty()) {
        auto next = green_phases[0];
        auto duration = std::chrono::hours(24);
        return {next.first + duration, next.second + duration};
    }

    // Default-Dummy (keine Phase bekannt)
    auto now = std::chrono::system_clock::now();
    return {now, now};
}
