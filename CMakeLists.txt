cmake_minimum_required(VERSION 3.15)
project(AuroraRL)

set(CMAKE_CXX_STANDARD 17)

# include directories
include_directories(include)

# 添加可执行文件示例
add_executable(test_sim examples/test_sim.cpp src/env.cpp src/agent.cpp src/buffer.cpp)

# 添加 Python 子工程
add_subdirectory(python)
