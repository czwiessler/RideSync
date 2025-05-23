#ifndef ROUTE_PLANNER_H
#define ROUTE_PLANNER_H

#include <vector>
#include <utility> // std::pair

class RoutePlanner {
public:
    // Berechnet Route vom Start zum Ziel (z. B. über OSM / Mock)
    static std::vector<std::pair<float, float>> compute_route(
        const std::pair<float, float>& start,
        const std::pair<float, float>& end);
};

#endif // ROUTE_PLANNER_H
