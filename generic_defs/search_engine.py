from abc import ABC, abstractclassmethod
import enum

class SearchStatus(enum.Enum):
    ACTIVE = 0
    READY = 1
    NOT_READY = 2
    TERMINATED = 3

class SearchEngine(ABC):
    """
    heuristic search engine base
    for A*
    """
    @abstractclassmethod
    def search(self, start, goal):
        pass

    @abstractclassmethod
    def heuristic(self, node):
        pass

    def __init__(self):
        self.status = SearchStatus.NOT_READY
        self.path = []
        self.visited = []
        self.cost = 0
        
    def statistics(self):
        return {
            "path": self.path,
            "visited": self.visited,
            "cost": self.cost,
            "status": self.status,
            "nodes_expanded": len(self.visited),
            "nodes_generated": len(self.visited) + len(self.open),
            "unique_nodes_generated": len(self.visited) + len(self.open) - len(self.closed),
            "max_nodes_in_memory": len(self.open) + len(self.closed),
        }

    def setTransitionSystem(self, transition_system):
        self.transition_system = transition_system
        self.status = SearchStatus.READY
    
    def setHeuristic(self, heuristic):
        self.heuristic = heuristic

    def setCostFunction(self, cost_function):
        self.cost_function = cost_function

    def setGoalTest(self, goal_test):
        self.goal_test = goal_test

    def setStartState(self, start_state):
        self.start_state = start_state

    
    def get_path(self):
        return self.path
    
    def get_visited(self):
        return self.visited
    
    def get_cost(self):
        return self.cost
    
    def get_status(self):
        return self.status

    


