import sys
import os

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import the necessary packages
from generic_defs.search_engine import *
from algorithms.domains.map_path_finding.path_finding import *
from algorithms.best_first_search.astar import *
from algorithms.best_first_search.egreedy import *

def main():
    # create a grid
    grid = Grid(10, 10)
    # grid[8, 9].value = 0
    # create a map
    map = Map(grid, start=Cell(0, 0, 1), goal=Cell(9, 9, 1))
    # create a search engine
    search_engine = EGBFS(1)
    # set the transition system
    search_engine.setTransitionSystem(map.transition_system)
    # set the heuristic
    search_engine.setHeuristic(map.heuristic)
    # set the cost function
    search_engine.setCostFunction(map.cost_function)

    # set the goal test
    search_engine.setGoalTest(map.goal_test)
    # set the start state
    search_engine.setStartState(map.start_state)
    # search
    path = search_engine.search(map.start_state, map.goal_state)
    # print the path
    print(path)
    print(search_engine.statistics())


if __name__ == "__main__":
    main()
