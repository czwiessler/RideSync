#include "RoutePlanner.h"
#include <cmath>

std::vector<std::pair<float, float>> RoutePlanner::compute_route(
    const std::pair<float, float>& start,
    const std::pair<float, float>& end) {

    std::vector<std::pair<float, float>> route;

    // Einfache Linearisierung: 10 Zwischenpunkte auf gerader Linie
    const int steps = 10;
    float lat_step = (end.first - start.first) / steps;
    float lon_step = (end.second - start.second) / steps;

    for (int i = 0; i <= steps; ++i) {
        float lat = start.first + i * lat_step;
        float lon = start.second + i * lon_step;
        route.push_back({lat, lon});
    }

    return route;
}

// TODO
// Gibt 10 Wegpunkte zwischen start und end zurück.
// Perfekt für MVP oder Tests.
// Später kannst du es ersetzen durch:
// OSM mit OSRM
// Graphhopper (lokal oder API)
// Python-Skript, das GPX oder JSON schreibt (und du liest es in C++ ein)