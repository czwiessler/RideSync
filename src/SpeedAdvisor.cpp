#include "SpeedAdvisor.h"
#include <cmath>
#include <iostream>
#include <algorithm>

constexpr float MAX_SPEED = 10.0f; // Max 10 m/s (ca. 36 km/h)
constexpr float MIN_SPEED = 1.0f;  // Min 1 m/s (ca. 3.6 km/h)

// Haversine für Entfernung
float haversine_distance(float lat1, float lon1, float lat2, float lon2) {
    const float R = 6371000.0f;
    float dLat = (lat2 - lat1) * M_PI / 180.0f;
    float dLon = (lon2 - lon1) * M_PI / 180.0f;
    float a = std::sin(dLat/2) * std::sin(dLat/2) +
              std::cos(lat1 * M_PI / 180.0f) * std::cos(lat2 * M_PI / 180.0f) *
              std::sin(dLon/2) * std::sin(dLon/2);
    float c = 2 * std::atan2(std::sqrt(a), std::sqrt(1-a));
    return R * c;
}

float SpeedAdvisor::compute_optimal_speed(const std::pair<float, float>& current_position,
                                          const TrafficLight& light,
                                          const Phase& green_phase) {
    auto now = std::chrono::system_clock::now();
    auto start_time = green_phase.first;
    auto end_time = green_phase.second;

    float distance_m = haversine_distance(
        current_position.first, current_position.second,
        light.get_location().first, light.get_location().second
    );

    // Zielzeitfenster
    auto time_until_start = std::chrono::duration_cast<std::chrono::seconds>(start_time - now).count();
    auto time_until_end = std::chrono::duration_cast<std::chrono::seconds>(end_time - now).count();

    if (time_until_end <= 0) return MAX_SPEED; // Grün vorbei → Vollgas oder warten

    float v_min = distance_m / std::max(float(time_until_end), 1.0f);
    float v_max = distance_m / std::max(float(time_until_start), 1.0f);

    // Optimal: Mitte zwischen v_min und v_max, aber im erlaubten Bereich
    float v_opt = (v_min + v_max) / 2.0f;
    v_opt = std::clamp(v_opt, MIN_SPEED, MAX_SPEED);
    return v_opt;
}

float SpeedAdvisor::get_current_speed() {
    // TODO: Tachomodul integrieren (GPIO-Impulse zählen)
    // MVP: Dummy-Wert für Test
    return 5.0f; // 5 m/s ≈ 18 km/h
}

float SpeedAdvisor::calculate_speed_diff(float target_speed, float current_speed) {
    return target_speed - current_speed;
}

std::string SpeedAdvisor::translate_to_instruction(float speed_diff) {
    if (std::abs(speed_diff) < 0.5f) {
        return "Halte Geschwindigkeit";
    } else if (speed_diff > 0.5f) {
        return "Beschleunigen";
    } else {
        return "Verlangsamen";
    }
}
