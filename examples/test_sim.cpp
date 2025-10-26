#include "../include/agent.h"
#include <iostream>

int main() {
    AgentManager manager(4); 
    manager.run(10);          
    for(auto r : manager.get_results()) {
        std::cout << "Agent reward: " << r << "\n";
    }
    return 0;
}
