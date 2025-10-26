cmake_minimum_required(VERSION 3.15)

find_package(pybind11 REQUIRED)

pybind11_add_module(auroralrl bindings.cpp)

target_include_directories(auroralrl PRIVATE ../include)
