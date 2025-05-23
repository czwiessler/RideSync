#include "TrafficLightFetcher.h"
#include <fstream>
#include <cmath>
#include "external/json/json.hpp"

using json = nlohmann::json;
using std::ifstream;
using std::get;

double TrafficLightFetcher::haversine_distance(double lat1, double lon1, double lat2, double lon2) const {
    const double R = 6371e3; // Earth's radius in meters
    double dLat = (lat2 - lat1) * M_PI / 180.0;
    double dLon = (lon2 - lon1) * M_PI / 180.0;
    double a = std::sin(dLat/2) * std::sin(dLat/2) +
               std::cos(lat1 * M_PI / 180.0) * std::cos(lat2 * M_PI / 180.0) *
               std::sin(dLon/2) * std::sin(dLon/2);
    double c = 2 * std::atan2(std::sqrt(a), std::sqrt(1-a));
    return R * c;
}

bool TrafficLightFetcher::load_from_json(const string& filename) {
    ifstream file(filename);
    if (!file.is_open()) return false;

    json data;
    file >> data;

    for (const auto& feature : data["features"]) {
        auto coords = feature["geometry"]["coordinates"];
        double lon = coords[0];
        double lat = coords[1];
        // Beispiel-Grünphase: jede Ampel hat alle 60 Sekunden 10 Sekunden grün
        // TODO: traffic light phases are not yet implemented
        auto now = std::chrono::system_clock::now();
        std::vector<TrafficLight::Phase> phases = {
            {now + std::chrono::seconds(10), now + std::chrono::seconds(20)},
            {now + std::chrono::seconds(70), now + std::chrono::seconds(80)},
            // ggf. weitere simulierte Phasen
        };
        allTrafficLights.emplace_back(static_cast<float>(lat), static_cast<float>(lon), phases);
    }
    return true;
}

std::vector<TrafficLight> TrafficLightFetcher::get_relevant_traffic_lights(const std::vector<std::pair<float, float>>& route) const {
    std::vector<TrafficLight> relevant;

    for (const auto& light : allTrafficLights) {
        for (const auto& point : route) {
            double dist = haversine_distance(light.get_location().first, light.get_location().second,
                                             point.first, point.second);
            if (dist < 30.0) {
                relevant.push_back(light);
                break;
            }
        }
    }

    return relevant;
}
