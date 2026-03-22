cmake_minimum_required(VERSION 3.15)
project(SortedListDemo)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Build type" FORCE)
endif()

set(CMAKE_CXX_FLAGS_RELEASE "-O3" CACHE STRING "Release flags" FORCE)

add_executable(sortedlist src/main.cpp)

target_include_directories(
    sortedlist PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)

