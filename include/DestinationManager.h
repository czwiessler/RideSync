#ifndef DESTINATION_MANAGER_H
#define DESTINATION_MANAGER_H

#include <utility> // std::pair

class DestinationManager {
public:
    // Setzt das Ziel (Breitengrad, Längengrad)
    static void set_destination(const std::pair<float, float>& destination);

    // Gibt das gesetzte Ziel zurück
    static std::pair<float, float> get_destination();

private:
    // Interne Speicherung des Ziels
    static std::pair<float, float> destination_;
};

#endif // DESTINATION_MANAGER_H
