cmake_minimum_required(VERSION 3.15)
project(QuantTeam_v2 VERSION 2.0 LANGUAGES CXX)

# C++20 标准
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 编译选项
if(MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -pedantic)
endif()

# 头文件目录
include_directories(${PROJECT_SOURCE_DIR}/include)

# 可执行文件
add_executable(QuantTeam_v2
    src/main.cpp
)

# 输出目录
set_target_properties(QuantTeam_v2 PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin
)

# 安装
install(TARGETS QuantTeam_v2
    RUNTIME DESTINATION bin
)
