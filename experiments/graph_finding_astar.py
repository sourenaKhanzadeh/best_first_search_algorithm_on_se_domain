import sys
import os

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import the necessary packages
from generic_defs.search_engine import *
from algorithms.domains.graph_path_finding.graph_path_finding import *
from algorithms.best_first_search.astar import *

def main():

    nodes = []
    for i in range(6):
        nodes.append(Node(i))

    vertices = [(nodes[0], nodes[1]),(nodes[0], nodes[2]),(nodes[1], nodes[4]),(nodes[2], nodes[3]),(nodes[4], nodes[3]),(nodes[3], nodes[5])]
    print(len(vertices))
    g = Graph(nodes, vertices)

    g.start_state = nodes[0]
    g.goal_state = nodes[5]

    search_engine = AStar()
    # set the transition system
    search_engine.setTransitionSystem(g.transition_system())
    # set the heuristic
    search_engine.setHeuristic(g.heuristic)
    # set the cost function
    search_engine.setCostFunction(g.cost_function)

    # set the goal test
    search_engine.setGoalTest(g.goal_test)
    # set the start state
    search_engine.setStartState(g.start_state)
    # search
    path = search_engine.search(g.start_state, g.goal_state)
    # print the path
    print(path)
    print(search_engine.statistics())


if __name__ == "__main__":
    main()
