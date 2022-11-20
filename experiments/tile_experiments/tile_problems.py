import sys
import os

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# add the parent parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# import the necessary packages
from generic_defs.search_engine import *
from algorithms.domains.tiles_domain.tiles_domain import *
from algorithms.best_first_search.astar import *
from algorithms.best_first_search.idastar import *
from algorithms.best_first_search.egreedy import *


def read_probs():
    # read the problems from the file
    with open('tile_files/3x4_puzzle.probs', 'r') as f:
        # read the lines
        lines = f.readlines()
        # create a list of problems
        problems = []
        # iterate over the lines
        for line in lines:
            # split the line
            split_line = line.split()

            init = [int(x) for x in split_line]
            # create a tile puzzle
            tile_puzzle = TilePuzzle(3, 4, init=init, goals=[[1, 2, 3, 4, 5,6, 7, 8, 9, 10, 11, 0]], cost_type='unit')
            # add the tile puzzle to the list
            problems.append(tile_puzzle)
        # return the problems
        return problems


def main():
    # create a tile puzzle
    # tile_puzzle = TilePuzzle(3, 4, init=[4, 0, 9, 7, 6, 5, 1, 3, 2, 11, 10, 8], goals=[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]], cost_type='unit')
    # tile_puzzle = TilePuzzle(3, 4, init=[11, 7, 10, 5, 8, 3, 2, 1, 4, 0, 6, 9], goals=[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]], cost_type='unit')
    tile_puzzles = read_probs()

    for tile_puzzle in tile_puzzles:
        # create a search engine
        search_engine = GBFS(1)
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
        __stat = search_engine.statistics()

        print(__stat['cost'], __stat['nodes_expanded'], __stat['nodes_generated'])

if __name__ == "__main__":
    main()