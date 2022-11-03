
class Grid:
    """
    Make a grid of nxm
    """
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.grid = [[0 for i in range(m)] for j in range(n)]

    def __str__(self):
        return str(self.grid)

    def set(self, i, j, value):
        self.grid[i][j] = value

    def get(self, i, j):
        return self.grid[i][j]

    def get_neighbours(self, i, j):
        neighbours = []
        if i > 0:
            neighbours.append((i - 1, j))
        if i < self.n - 1:
            neighbours.append((i + 1, j))
        if j > 0:
            neighbours.append((i, j - 1))
        if j < self.m - 1:
            neighbours.append((i, j + 1))
        return neighbours

    def get_neighbours_with_cost(self, i, j):
        neighbours = []
        if i > 0:
            neighbours.append((i - 1, j, self.grid[i - 1][j]))
        if i < self.n - 1:
            neighbours.append((i + 1, j, self.grid[i + 1][j]))
        if j > 0:
            neighbours.append((i, j - 1, self.grid[i][j - 1]))
        if j < self.m - 1:
            neighbours.append((i, j + 1, self.grid[i][j + 1]))
        return neighbours

    def get_neighbours_with_cost_and_heuristic(self, i, j, goal):
        neighbours = []
        if i > 0:
            neighbours.append((i - 1, j, self.grid[i- 1][j], abs(i - 1 - goal[0]) + abs(j - goal[1])))
        if i < self.n - 1:
            neighbours.append((i + 1, j, self.grid[i + 1][j], abs(i + 1 - goal[0]) + abs(j - goal[1])))
        if j > 0:
            neighbours.append((i, j - 1, self.grid[i][j - 1], abs(i - goal[0]) + abs(j - 1 - goal[1])))
        if j < self.m - 1:
            neighbours.append((i, j + 1, self.grid[i][j + 1], abs(i - goal[0]) + abs(j + 1 - goal[1])))
        return neighbours

class ManhattanHeuristic:
    """
    Manhattan heuristic
    """
    def __init__(self, goal):
        self.goal = goal

    def __call__(self, node):
        return abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])


class SetGoalTest:
    """
    Goal test
    """
    def __init__(self, goal):
        self.goal = goal

    def __call__(self, node):
        return node == self.goal

class Map:
    """
    Map class
    """
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.transition_system = self.get_neighbours_with_cost_and_heuristic
        self.heuristic = ManhattanHeuristic(self.goal)
        self.cost_function = self.get_cost
        self.goal_test = SetGoalTest(self.goal)
        self.start_state = self.start
        self.goal_state = self.goal

    def get_start(self):
        return self.start

    def get_goal(self):
        return self.goal

    def get_grid(self):
        return self.grid

    def get_neighbours(self, node):
        return self.grid.get_neighbours(node[0], node[1])

    def get_neighbours_with_cost(self, node):
        return self.grid.get_neighbours_with_cost(node[0], node[1])

    def get_neighbours_with_cost_and_heuristic(self, node):
        return self.grid.get_neighbours_with_cost_and_heuristic(node[0], node[1], self.goal)

    def get_cost(self, node):
        return self.grid.get(node[0], node[1])

