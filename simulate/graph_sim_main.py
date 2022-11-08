import os
import sys

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# add parent of the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from algorithms.domains.graph_path_finding.graph_path_finding import *
from algorithms.best_first_search.astar import *
from domain.graphs.simulate_graph import *

if __name__ == "__main__":
    
    # # print(len(vertices))
    # g = Graph(nodes, vertices)

    # g.start_state = nodes[0]
    # g.goal_state = nodes[5]

    # search_engine = AStar()
    # # set the transition system
    # search_engine.setTransitionSystem(g.transition_system())
    # # set the heuristic
    # search_engine.setHeuristic(g.heuristic)
    # # set the cost function
    # search_engine.setCostFunction(g.cost_function)

    # # set the goal test
    # search_engine.setGoalTest(g.goal_test)
    # # set the start state
    # search_engine.setStartState(g.start_state)
    # # search
    # path, action = search_engine.search(g.start_state, g.goal_state)

    game = Game(Settings())
    # for node, pos in zip(nodes, positions):
    #     node.x = pos[0]
    #     node.y = pos[1]
    #     game.graph.add_node(node.val, pos[0], pos[1])

    # for vertex in vertices:
    #     game.graph.add_edge(vertex[0], vertex[1])
    
    # for p in path:
    #     game.graph.policy("traverse_edge", p)
    game.run()