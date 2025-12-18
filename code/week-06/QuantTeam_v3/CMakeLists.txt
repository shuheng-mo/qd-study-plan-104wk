cmake_minimum_required(VERSION 3.14)
project(QuantTeam_v3 VERSION 1.0.0 LANGUAGES CXX)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 编译选项
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG -march=native -Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -Wall -Wextra -Wpedantic")

# 包含目录
include_directories(${PROJECT_SOURCE_DIR}/include)

# 源文件
set(SOURCES
    src/main.cpp
    src/Portfolio.cpp
)

# 可执行文件
add_executable(QuantTeam_v3 ${SOURCES})

# 测试可执行文件（可选）
add_executable(tests
    tests/test_all.cpp
    src/Portfolio.cpp
)

# 打印配置信息
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Compiler: ${CMAKE_CXX_COMPILER}")
message(STATUS "Compiler flags: ${CMAKE_CXX_FLAGS}")
message(STATUS "Compiler flags (Release): ${CMAKE_CXX_FLAGS_RELEASE}")
message(STATUS "Compiler flags (Debug): ${CMAKE_CXX_FLAGS_DEBUG}")
