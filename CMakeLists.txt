cmake_minimum_required(VERSION 3.29)
project(testare_vtune)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")

add_executable(testare_vtune client.cpp)




add_custom_command(TARGET testare_vtune POST_BUILD
        # 🔄 Șterge directoarele de rezultate anterioare
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_BINARY_DIR}/vtune_results_/hotspots
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_BINARY_DIR}/vtune_results_/memory

        # 📁 Creează din nou directoarele goale
        COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_BINARY_DIR}/vtune_results_/hotspots
        COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_BINARY_DIR}/vtune_results_/memory

        # 🟥 Colectare HOTSPOTS cu redirecționare output
        COMMAND cmd /c "\"C:/Program Files (x86)/Intel/oneAPI/vtune/latest/bin64/vtune.exe\" -collect hotspots -result-dir ${CMAKE_CURRENT_BINARY_DIR}/vtune_results_/hotspots -- ${CMAKE_CURRENT_BINARY_DIR}/Debug/testare_vtune.exe >nul 2>nul"

        # 📊 Raport HOTSPOTS — output doar în fișier
        COMMAND cmd /c "\"C:/Program Files (x86)/Intel/oneAPI/vtune/latest/bin64/vtune.exe\" -report hotspots -result-dir ${CMAKE_CURRENT_BINARY_DIR}/vtune_results_/hotspots -report-output ${CMAKE_CURRENT_BINARY_DIR}/vtune_results_/hotspots_report.txt >nul 2>nul"

        COMMENT "Running VTune profiler (hotspots only) silently and saving report to file"
)



