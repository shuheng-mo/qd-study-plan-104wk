cmake_minimum_required(VERSION 3.20)
project(Week07_IO_FileManagement)

# 设置C++标准为C++20（需要std::format支持）
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 编译选项
if(MSVC)
    add_compile_options(/W4 /utf-8)
else()
    add_compile_options(-Wall -Wextra -pedantic)
endif()

# 包含头文件目录
include_directories(${CMAKE_SOURCE_DIR}/include)

# 添加可执行文件
add_executable(week07_demo
    src/main.cpp
)

# macOS可能需要链接filesystem库
if(APPLE)
    target_link_libraries(week07_demo PRIVATE)
elseif(UNIX)
    target_link_libraries(week07_demo PRIVATE)
endif()

# 输出构建信息
message(STATUS "Week 7 - C++ IO与文件管理")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
