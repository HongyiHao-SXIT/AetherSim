#pragma once

class SimpleEnv {
    int state;
public:
    SimpleEnv() : state(0) {}
    int step(int action) { state += action; return state; }
    void reset() { state = 0; }
    int get_state() const { return state; }
};
