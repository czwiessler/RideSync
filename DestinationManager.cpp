#include "DestinationManager.h"

// Initialisierung des statischen Members
std::pair<float, float> DestinationManager::destination_ = {0.0f, 0.0f};

void DestinationManager::set_destination(const std::pair<float, float>& destination) {
    destination_ = destination;
}

std::pair<float, float> DestinationManager::get_destination() {
    return destination_;
}
