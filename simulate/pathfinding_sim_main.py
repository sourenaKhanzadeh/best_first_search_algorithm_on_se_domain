import sys
import os

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# add parent of the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from domain.pathfinding.simulate_pathfinding import *
from algorithms.domains.map_path_finding.path_finding import *
from algorithms.best_first_search.astar import *


if __name__ == "__main__":
    s = Simulate(Settings(fps=30))
    # create a grid
    grid = Grid(20, 20)
    # grid[8, 9].value = 0
    walls = []
    # create walls
    # for i in range(0, 5):
        # walls.append(Wall(s.screen, i, 0))
        # walls.append(Wall(s.screen, i, 19))
        # grid[i, 0].value = 0
        # grid[i, 19].value = 0

    walls.append(Wall(s.screen, 3, 0))
    walls.append(Wall(s.screen, 0, 1))
    walls.append(Wall(s.screen, 0, 2))
    walls.append(Wall(s.screen, 0, 3))
    grid[3, 0].value = 0
    grid[0, 1].value = 0
    grid[0, 2].value = 0
    grid[0, 3].value = 0

    s.awake(GridSM(s.settings, s.screen, walls=walls, start=(0, 0), goal=(9, 9)))
    # create a map
    map = Map(grid, start=Cell(0, 0, 1), goal=Cell(9, 9, 1))
    # create a search engine
    search_engine = AStar(1)
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
    path, action = search_engine.search(map.start_state, map.goal_state)
    
    for a in action:
        assert type(s.scene[0]) == GridSM, "scene[0] is not a GridSM"
        s.scene[0].path.policy(a)
    for state in search_engine.visited:
        s.scene[0].path.visited(state.cell.x, state.cell.y)
    # print the path
    s.run()    