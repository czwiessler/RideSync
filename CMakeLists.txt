cmake_minimum_required(VERSION 3.23)
project(RideSync)

set(CMAKE_CXX_STANDARD 17)

add_executable(RideSync
        main.cpp
        DestinationManager.cpp
        TrafficLight.cpp
        TrafficLightFetcher.cpp
        UpdateLoopController.cpp
        SpeedAdvisor.cpp
        RoutePlanner.cpp
        PositionTracker.cpp

)

# LEDController.cpp

#include_directories(${CMAKE_SOURCE_DIR}/external/TinyGPS++)
#external/TinyGPS++/TinyGPS++.cpp
