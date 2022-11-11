# Simulations

# Domain

## Pathfinding
```python
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
    
    # Add walls like this
    walls.append(Wall(s.screen, 3, 0))
    walls.append(Wall(s.screen, 0, 1))
    walls.append(Wall(s.screen, 0, 2))
    walls.append(Wall(s.screen, 0, 3))
    grid[3, 0].value = 0
    grid[0, 1].value = 0
    grid[0, 2].value = 0
    grid[0, 3].value = 0
    
    # add the GridSM Object
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
    # Run the simulation
    s.run()    
```

## Tile Puzzle
```python
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
```

## Graphs

```python
if __name__ == "__main__":
    # nothing else is required
    game = Game(Settings())
    game.run()
```
