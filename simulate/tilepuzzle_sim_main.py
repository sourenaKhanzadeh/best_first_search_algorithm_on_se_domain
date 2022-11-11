import os
import sys

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# add parent of the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# import the necessary packages
from algorithms.domains.tiles_domain.tiles_domain import *
from algorithms.best_first_search.astar import *
from domain.tilepuzzle.simulate_tilepuzzle import *


if __name__ == "__main__":
    # create a tile puzzle
    tile_puzzle = TilePuzzle(3, 3, init=[1, 5, 2, 0, 3, 6, 7, 8, 4], goals=[[1, 2, 3, 4, 5, 6, 7, 8, 0]])

    # create a search engine
    search_engine = AStar(1)
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
    path, action = search_engine.search(tile_puzzle.init, tile_puzzle.goals)

    game = Game(Settings(fps=30))
    game.TileSM_puzzle.init_TileSMs(tile_puzzle.init.cell)

    for a in action:
        game.TileSM_puzzle.getActions(a.name)

    game.run()