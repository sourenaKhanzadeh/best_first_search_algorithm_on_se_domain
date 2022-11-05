from generic_defs.search_engine import *


class AStar(SearchEngine):

    def __init__(self, w=1):
        super().__init__()
        self.open = []
        self.closed = []
        self.w = w

    def search(self, start, goal):
        self.open = [start]
        self.closed = []
        while self.open:
            current = self.open.pop(0)
            self.closed.append(current)
            if self.goal_test(current):
                self.path = self.reconstruct_path(current)
                self.actions = self.reconstruct_path_actions(current)
                self.visited = self.closed
                self.cost = current.g
                self.status = SearchStatus.TERMINATED
                return self.path, self.actions
            for action, child in self.transition_system(current):
                if child in self.closed:
                    continue
                if child not in self.open:
                    child.parent = current
                    child.action = action
                    child.g = self.cost_function(current, action)
                    self.open.append(child)
                else:
                    if child.g < current.g:
                        self.open.remove(child)
                        child.parent = current
                        child.action = action
                        child.g = self.cost_function(current, action)
                        self.open.append(child)
            self.open.sort(key=lambda x: x.g + self.w * self.heuristic(x))
        self.status = SearchStatus.TERMINATED
        return None

    def heuristic(self, node):
        self.heuristic(node)

    def reconstruct_path(self, current):
        path = []
        while current.parent:
            path.append(current)
            current = current.parent

        path.append(current)
        return path[::-1]
    
    def reconstruct_path_actions(self, current):
        path = []
        while current.parent:
            path.append(current.action)
            current = current.parent
        return path[::-1]

    def setTransitionSystem(self, transition_system):
        super().setTransitionSystem(transition_system)
        self.open = []
        self.closed = []

    def setHeuristic(self, heuristic):
        super().setHeuristic(heuristic)
        self.open = []
        self.closed = []

    def setCostFunction(self, cost_function):
        super().setCostFunction(cost_function)
        self.open = []
        self.closed = []

    def setGoalTest(self, goal_test):
        super().setGoalTest(goal_test)
        self.open = []
        self.closed = []

    def setStartState(self, start_state):
        super().setStartState(start_state)
        self.open = []
        self.closed = []