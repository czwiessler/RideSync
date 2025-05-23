#include "PositionTracker.h"
//#include <TinyGPS++.h>   // Vorübergehend deaktiviert

// extern TinyGPSPlus gps; // wird vorerst nicht verwendet

std::pair<float, float> PositionTracker::get_current_position() {
    // === Mock-Modus ===
    float latitude = 50.9375f;  // Beispiel: Köln Dom
    float longitude = 6.9603f;
    return {latitude, longitude};

    /*
    // === Original TinyGPS++ Code ===
    if (gps.location.isValid()) {
        float latitude = gps.location.lat();
        float longitude = gps.location.lng();
        return {latitude, longitude};
    } else {
        throw std::runtime_error("Ungültige GPS-Position");
    }
    */
}
