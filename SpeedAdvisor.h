#pragma once

#include <string>
#include <utility>
#include <chrono>
#include "TrafficLight.h"

class SpeedAdvisor {
public:
    using TimePoint = std::chrono::system_clock::time_point;
    using Phase = std::pair<TimePoint, TimePoint>;

    // Berechne optimale Geschwindigkeit (m/s), um grün zu erreichen
    static float compute_optimal_speed(const std::pair<float, float>& current_position,
                                       const TrafficLight& light,
                                       const Phase& green_phase);

    // Hole aktuelle Geschwindigkeit (z. B. aus Sensor oder Dummy)
    static float get_current_speed();

    // Berechne Differenz: Zielgeschwindigkeit – Istgeschwindigkeit
    static float calculate_speed_diff(float target_speed, float current_speed);

    // Übersetze Differenz in visuelle/verbale Anweisung
    static std::string translate_to_instruction(float speed_diff);
};
