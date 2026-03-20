cmake_minimum_required(VERSION 3.15)
project(SortedListDemo)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(sortedlist src/main.cpp)

target_include_directories(
    sortedlist PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)

