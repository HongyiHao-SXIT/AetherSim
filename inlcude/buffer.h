#pragma once
#include <vector>
#include <tuple>

class ReplayBuffer {
    size_t max_size;
    std::vector<std::tuple<int,int,int>> buffer;
    size_t index = 0;

public:
    ReplayBuffer(size_t size) : max_size(size), buffer(size) {}

    void add(int state, int action, int reward) {
        buffer[index] = std::make_tuple(state, action, reward);
        index = (index + 1) % max_size;
    }

    std::vector<std::tuple<int,int,int>> sample() const {
        return buffer;
    }
};
