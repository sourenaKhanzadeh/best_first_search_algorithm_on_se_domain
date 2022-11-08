from generic_defs.search_engine import *
import sys



class IDAStar(SearchEngine):
    """
    IDA* algorithm
    """

    def __init__(self, w=1):
        self.w = w
        self.path = []
        self.actions = []
        self.visited = []
        self.open = []
        self.closed = []
        self.cost = 0
        self.number_of_expanded_nodes = 0
        self.status = SearchStatus.NOT_READY

    def heuristic(self, node):
        """
        heuristic
        :param node: node
        :return: heuristic value
        """
        self.heuristic(node)

    def search(self, start, goal):
        """
        search
        :param start: start state
        :param goal: goal state
        :param transition_system: transition system
        :param goal_test: goal test
        :param cost_function: cost function
        :param heuristic: heuristic
        :return: path, actions
        """
        self.status = SearchStatus.ACTIVE
        self.path, self.actions = self.idastar(start, goal, self.transition_system,self.goal_test, self.cost_function, self.heuristic)
        self.status = SearchStatus.TERMINATED
        return self.path, self.actions
    
    def idastar(self, start, goal, transition_system, goal_test, cost_function, heuristic):
        """
        idastar
        :param start: start state
        :param goal: goal state
        :param transition_system: transition system
        :param goal_test: goal test
        :param cost_function: cost function
        :param heuristic: heuristic
        :return: path, actions
        """
        threshold = heuristic(start)
        while True:
            t, path, actions = self.dls(start, goal, transition_system, goal_test, cost_function, heuristic, threshold)
            if t == 0:
                return path, actions
            if t == float('inf'):
                return None
            threshold = t

    def dls(self, current, goal, transition_system, goal_test, cost_function, heuristic, threshold):
        """
        dls
        :param current: current state
        :param goal: goal state
        :param transition_system: transition system
        :param goal_test: goal test
        :param cost_function: cost function
        :param heuristic: heuristic
        :param threshold: threshold
        :return: threshold, path, actions
        """
        self.number_of_expanded_nodes += 1
        f = current.g + self.w * heuristic(current)
        if f > threshold:
            return f, None, None
        if goal_test(current):
            return 0, [current], []
        min = float('inf')
        path = []
        actions = []
        for action, child in transition_system(current):
            child.g = cost_function(current, action)
            self.cost = child.g
            t, p, a = self.dls(child, goal, transition_system, goal_test, cost_function, heuristic, threshold)
            if t == 0:
                path = [current] + p
                actions = [action] + a
                return 0, path, actions
            if t < min:
                min = t
        return min, path, actions