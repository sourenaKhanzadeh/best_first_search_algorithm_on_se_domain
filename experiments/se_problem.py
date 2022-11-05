import sys
import os

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import the necessary packages
from generic_defs.search_engine import *
from algorithms.domains.SE_domain.se_domain import *
from algorithms.best_first_search.astar import *

def main():
    
    nodes = []
    for i in range(6):
        nodes.append(Node(str(i), cell=i))

    vertices = [Edge(nodes[0], nodes[1], 1),Edge(nodes[0], nodes[2], 1),
    Edge(nodes[1], nodes[4], 1), Edge(nodes[2], nodes[3], 1), Edge(nodes[4], nodes[3], 1), 
    Edge(nodes[3], nodes[5], 1)]
    print(len(vertices))
    g = Graph(nodes, vertices)

    se = SEDomain(g, nodes[0], nodes[5])

    search_engine = AStar()
    # set the transition system
    search_engine.setTransitionSystem(se.transition_system)
    # set the heuristic
    search_engine.setHeuristic(se.heuristic)
    # set the cost function
    search_engine.setCostFunction(se.cost_function)

    # set the goal test
    search_engine.setGoalTest(se.goal_test)
    # set the start state
    search_engine.setStartState(se.start_state)
    # search
    path = search_engine.search(se.start_state, se.goal_state)
    # print the path
    print(path)
    print(search_engine.statistics())

if __name__ == "__main__":
    main()