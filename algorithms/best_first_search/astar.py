from generic_defs.search_engine import *


class AStar(SearchEngine):

    def __init__(self):
        super().__init__()
        self.open = []
        self.closed = []

    def search(self, start, goal):
        self.open = [start]
        self.closed = []
        while self.open:
            current = self.open.pop(0)
            self.closed.append(current)
            if self.goal_test(current):
                self.path = self.reconstruct_path(current)
                self.visited = self.closed + self.open
                self.cost = current.g
                self.status = SearchStatus.TERMINATED
                return self.path
            for child in self.transition_system(current):
                if child[1] in self.closed:
                    continue
                if child[1] not in self.open:
                    self.open.append(child[1])
                else:
                    if child[1].g < current.g:
                        self.open.remove(child[1])
                        self.open.append(child[1])
            self.open.sort(key=lambda x: x.g + x.h)
        self.status = SearchStatus.TERMINATED
        return None

    def heuristic(self, node):
        pass

    def reconstruct_path(self, current):
        path = []
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(current)
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