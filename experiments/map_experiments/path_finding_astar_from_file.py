import sys
import os

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# add parent of the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# import the necessary packages
from generic_defs.search_engine import *
from algorithms.domains.map_path_finding.path_finding import *
from algorithms.best_first_search.astar import *

# For empty grid
# MAP_FILE = "./map_files/empty_grid.map"
# PROBS_FILE = "./map_files/empty_grid.probs"

MAP_FILE = "./map_files/starcraft_bgh.map"
PROBS_FILE = "./map_files/starcraft_bgh.probs"


def map_reader(grid_map):
    new_map = []
    for l in grid_map:
        new_map_line = []
        for i in l:
            if  i == '.':
                new_map_line.append(1)
            # elif i == '|':
            #     new_map_line.append(0)
            else:
                new_map_line.append(0)
        new_map.append(new_map_line)
    return new_map


def read_map_file():
    with open(MAP_FILE, 'r') as filehandle:
        all_lines = filehandle.readlines()
        height = all_lines[0].replace('height', '').strip()
        width = all_lines[1].replace('width', '').strip()
        grid_map = [i.strip() for i in all_lines[3:]]

    return int(height), int(width), map_reader(grid_map)


def read_probs_file():
    experiments = []
    with open(PROBS_FILE, 'r') as filehandle:
        for line in filehandle:
            int_line = []
            for i in line.strip().split():
                int_line.append(int(i))
            experiments.append(int_line)

    return experiments


def initiate_grid_from_map():
    h, w, grid_map = read_map_file()
    grid = Grid(h, w)
    for i in range(h):
        for j in range(w):
            grid[j, i].value = grid_map[i][j]
    return grid


def main():
    grid = initiate_grid_from_map()
    experiments = read_probs_file()

    for experiment in experiments:
        # print(experiment[0], experiment[1])
        # print(grid[experiment[0], experiment[1]])
        grid_map = Map(
            grid,
            start=grid[experiment[0], experiment[1]],
            goal=grid[experiment[2], experiment[3]],
            heuristic= 'manhattan'
        )
        search_engine = AStar(1)
        # set the transition system
        search_engine.setTransitionSystem(grid_map.transition_system)
        # set the heuristic
        search_engine.setHeuristic(grid_map.heuristic)
        # set the cost function
        search_engine.setCostFunction(grid_map.cost_function)

        # set the goal test
        search_engine.setGoalTest(grid_map.goal_test)
        # set the start state
        search_engine.setStartState(grid_map.start_state)
        # search
        path = search_engine.search(grid_map.start_state, grid_map.goal_state)
        # print the path
        # print(grid_map.grid)
        # print(path)
        statistics_s = search_engine.statistics()
        print(statistics_s["cost"], statistics_s["nodes_expanded"])
    # grid[8, 9].value = 0
    # # create a map
    # map = Map(grid, start=Cell(0, 0, 1), goal=Cell(9, 9, 1))
    # # create a search engine
    # search_engine = AStar(1)
    # # set the transition system
    # search_engine.setTransitionSystem(map.transition_system)
    # # set the heuristic
    # search_engine.setHeuristic(map.heuristic)
    # # set the cost function
    # search_engine.setCostFunction(map.cost_function)
    #
    # # set the goal test
    # search_engine.setGoalTest(map.goal_test)
    # # set the start state
    # search_engine.setStartState(map.start_state)
    # # search
    # path = search_engine.search(map.start_state, map.goal_state)
    # # print the path
    # print(path)
    # print(search_engine.statistics())


if __name__ == "__main__":
    main()
