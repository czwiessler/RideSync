#pragma once
#include <vector>
#include <tuple>
#include <string>
#include "TrafficLight.h" // 🟢 NUR diese Klasse verwenden

using std::string;
using std::tuple;
using std::vector;


class TrafficLightFetcher {
private:
    vector<TrafficLight> allTrafficLights;

    double haversine_distance(double lat1, double lon1, double lat2, double lon2) const;

public:
    bool load_from_json(const string& filename);
    std::vector<TrafficLight> get_relevant_traffic_lights(const std::vector<std::pair<float, float>>& route) const;
};
