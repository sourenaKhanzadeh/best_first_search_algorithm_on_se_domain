import sys
import os

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import the necessary packages
from generic_defs.search_engine import *
from algorithms.domains.tiles_domain.tiles_domain import *
from algorithms.best_first_search.astar import *
from algorithms.best_first_search.idastar import *
from algorithms.best_first_search.egreedy import *

def main():
    # create a tile puzzle
    tile_puzzle = TilePuzzle(3, init=[1, 5, 2, 0, 3, 6, 7, 8, 4], goals=[[1, 2, 3, 4, 5, 6, 7, 8, 0]])

    # create a search engine
    search_engine = EGBFS(1)
    # set the transition system
    search_engine.setTransitionSystem(tile_puzzle.to_transition_system())
    # set the heuristic
    search_engine.setHeuristic(tile_puzzle.heuristic)
    # set the cost function
    search_engine.setCostFunction(tile_puzzle.cost_function)

    # set the goal test
    search_engine.setGoalTest(tile_puzzle.goal_test)
    # set the start state
    search_engine.setStartState(tile_puzzle.init)
    # search
    path = search_engine.search(tile_puzzle.init, tile_puzzle.goals)
    # print the path
    print(path)
    # print(search_engine.statistics())
    print(search_engine.statistics())

if __name__ == "__main__":
    main()
