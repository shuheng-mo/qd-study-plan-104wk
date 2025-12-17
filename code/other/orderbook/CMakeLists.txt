cmake_minimum_required(VERSION 3.10)
project(OrderBook)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置编译选项
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Release 模式下的优化选项
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG -march=native")
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")

# 包含头文件目录
include_directories(${PROJECT_SOURCE_DIR}/include)

# 基准测试可执行文件
add_executable(benchmark
    src/benchmark.cpp
)

# 如果有其他源文件，可以添加到这里
# add_executable(main
#     src/main.cpp
# )

# 打印编译信息
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ compiler: ${CMAKE_CXX_COMPILER}")
message(STATUS "C++ flags: ${CMAKE_CXX_FLAGS}")
message(STATUS "C++ flags (Release): ${CMAKE_CXX_FLAGS_RELEASE}")
message(STATUS "C++ flags (Debug): ${CMAKE_CXX_FLAGS_DEBUG}")
