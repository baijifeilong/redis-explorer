cmake_minimum_required(VERSION 3.15)
project(RedisExplorer)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_VERBOSE_MAKEFILE ON)
set(CMAKE_PREFIX_PATH C:/Qt/5.12.6/mingw73_32)

find_package(Qt5Widgets)
add_executable(RedisExplorer main.cpp)
target_link_libraries(RedisExplorer Qt5::Widgets)