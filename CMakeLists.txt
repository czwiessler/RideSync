cmake_minimum_required(VERSION 3.23)
project(RideSync)

set(CMAKE_CXX_STANDARD 17)

# Include-Pfade für Header-Dateien
include_directories(
        ${CMAKE_SOURCE_DIR}/include
        ${CMAKE_SOURCE_DIR}/external/json
        ${CMAKE_SOURCE_DIR}/external/TinyGPS++
)

# Source-Dateien (aus dem src-Verzeichnis + main.cpp)
file(GLOB_RECURSE SOURCES
        src/*.cpp
        main.cpp
)

add_executable(RideSync ${SOURCES})

# Falls TinyGPS++ eine eigene .cpp Datei hat, kannst du sie so einbinden:
# add_library(TinyGPSPlus external/TinyGPS++/TinyGPS++.cpp)
# target_link_libraries(RideSync TinyGPSPlus)
