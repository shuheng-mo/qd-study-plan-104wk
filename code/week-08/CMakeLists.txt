cmake_minimum_required(VERSION 3.20)
project(Week08_ExceptionHandling)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 编译选项
if(MSVC)
    add_compile_options(/W4 /std:c++20)
else()
    add_compile_options(-Wall -Wextra -pedantic -std=c++20)
endif()

# 包含目录
include_directories(${CMAKE_SOURCE_DIR}/include)

# 可执行文件
add_executable(week08_demo
    src/main.cpp
)

# 链接线程库
find_package(Threads REQUIRED)
target_link_libraries(week08_demo PRIVATE Threads::Threads)

# 设置输出目录
set_target_properties(week08_demo PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

# 打印配置信息
message(STATUS "Week 08 - Exception Handling")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
