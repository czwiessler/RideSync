#ifndef POSITION_TRACKER_H
#define POSITION_TRACKER_H

#include <utility> // for std::pair

class PositionTracker {
public:
    // Holt aktuelle GPS-Position vom Arduino-GPS-Modul
    static std::pair<float, float> get_current_position();
};

#endif // POSITION_TRACKER_H
