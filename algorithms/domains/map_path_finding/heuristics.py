class Heuristic(object):
    """A heuristic function maps states to costs."""
    def __call__(self, state):
        return 0


class ManhattanHeuristic(Heuristic):
    def __init__(self, goalx, goaly):
        self.goalx = goalx
        self.goaly = goaly
    """A heuristic function maps states to costs."""
    def __call__(self, state):
        return abs(state.cell.x - self.goalx) + abs(state.cell.y - self.goaly)
