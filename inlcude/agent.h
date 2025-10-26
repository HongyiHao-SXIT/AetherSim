#pragma once
#include "env.h"
#include <vector>
#include <thread>
#include <mutex>

class AgentManager {
    std::vector<SimpleEnv> envs;
    std::vector<int> results;
    std::mutex mtx;

public:
    AgentManager(int n_agents) : envs(n_agents), results(n_agents,0) {}

    void run(int steps) {
        std::vector<std::thread> threads;
        for(size_t i=0; i<envs.size(); ++i) {
            threads.emplace_back([this, i, steps]() {
                for(int t=0; t<steps; ++t) {
                    int action = rand() % 2;
                    int reward = envs[i].step(action);
                    std::lock_guard<std::mutex> lock(mtx);
                    results[i] += reward;
                }
            });
        }
        for(auto &th : threads) th.join();
    }

    const std::vector<int>& get_results() const { return results; }
    void reset() { 
        for(auto &e: envs) e.reset();
        std::fill(results.begin(), results.end(), 0);
    }
};
