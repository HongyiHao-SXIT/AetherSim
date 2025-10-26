#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../include/env.h"
#include "../include/agent.h"

namespace py = pybind11;

PYBIND11_MODULE(auroralrl, m) {
    py::class_<SimpleEnv>(m, "SimpleEnv")
        .def(py::init<>())
        .def("step", &SimpleEnv::step)
        .def("reset", &SimpleEnv::reset)
        .def("get_state", &SimpleEnv::get_state);

    py::class_<AgentManager>(m, "AgentManager")
        .def(py::init<int>())
        .def("run", &AgentManager::run)
        .def("get_results", &AgentManager::get_results)
        .def("reset", &AgentManager::reset);
}
