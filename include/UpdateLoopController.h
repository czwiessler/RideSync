#ifndef UPDATE_LOOP_CONTROLLER_H
#define UPDATE_LOOP_CONTROLLER_H

#include <vector>
#include <string>
#include <utility>

#include "TrafficLight.h"
#include "TrafficLightFetcher.h"

class UpdateLoopController {
public:
    // Konstruktor mit Übergabe des geladenen TrafficLightFetcher
    UpdateLoopController(const TrafficLightFetcher& fetcher);

    void start_loop();
    void update_cycle();

private:
    TrafficLightFetcher fetcher_; // interner Cache aller bekannten Ampeln

    TrafficLight get_next_traffic_light(const std::pair<float, float>& pos,
                                        const std::vector<TrafficLight>& lights);
};

#endif // UPDATE_LOOP_CONTROLLER_H
