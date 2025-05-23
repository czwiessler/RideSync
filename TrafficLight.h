#pragma once

#include <vector>
#include <tuple>
#include <chrono>

class TrafficLight {
public:
    using TimePoint = std::chrono::system_clock::time_point;
    using Phase = std::pair<TimePoint, TimePoint>;

private:
    float latitude;
    float longitude;
    std::vector<Phase> green_phases;

public:
    TrafficLight(float lat, float lon, const std::vector<Phase>& phases);

    std::pair<float, float> get_location() const;
    Phase get_next_green_phase(TimePoint current_time) const;
};
