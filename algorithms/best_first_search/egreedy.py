from generic_defs.search_engine import *
import heapq
import random

class GBFS(SearchEngine):
    """
    Greedy Best First Search algorithm
    """

    def __init__(self, w=1):
        super().__init__()
        self.open = []
        self.closed = []
        self.w = w

    def search(self, start, goal):
        # tie breaking
        heapq.heappush(self.open, (self.heuristic(start), start))
        self.closed = []
        while self.open:
            # if tie breaking get the one with lower g cost
            current = heapq.heappop(self.open)[1]
            self.closed.append(current)
            self.number_of_expanded_nodes += 1
            if self.goal_test(current):
                self.path = self.reconstruct_path(current)
                self.actions = self.reconstruct_path_actions(current)
                self.visited = self.closed
                self.cost = current.g
                self.status = SearchStatus.TERMINATED
                return self.path, self.actions
            for action, child in self.transition_system(current):
                current_cost = self.cost_function(current, action)
                # if child in self.closed:
                    # continue
                if child in [x[1] for x in self.open]:
                    if child.g <= current_cost:
                        continue
                elif child in self.closed:
                    if child.g <= current_cost:
                        continue
                    heapq.heappush(self.open, (self.heuristic(child), self.closed.pop(self.closed.index(child))))
                # if child not in the heap
                # if child not in [x[1] for x in self.open]:
                child.parent = current
                child.action = action
                child.g = self.cost_function(current, action)
                heapq.heappush(self.open, (self.heuristic(child), child))
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

class EGBFS(GBFS):
    """
    Epsilon Greedy Best First Search algorithm
    """

    def __init__(self, w=1, epsilon=0.1):
        super().__init__(w)
        self.epsilon = epsilon

    def search(self, start, goal):
        self.open = [start]
        self.closed = []
        while self.open:
            current = self.open.pop(0)
            self.closed.append(current)
            self.number_of_expanded_nodes += 1
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
            
            # put the current fscore in the heap
            heapq.heapify(self.open)
            # get the lowest fscore from the heap
            self.open = heapq.nsmallest(len(self.open), self.open, key=lambda x: (self.w * self.heuristic(x)))
            # epsilon greedy randomization
            if random.random() < self.epsilon:
                self.open = random.sample(self.open, len(self.open))
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



class DecayBestEX(GBFS):
    """
    DecayBestEX Best First Search Algorithm
    """

    def __init__(self, w=1, epsilon=0.1, decay_rate=0.05):
        super().__init__(w)
        self.epsilon = epsilon
        self.decay_rate = (1 - decay_rate)
        

    def search(self, start, goal):
        self.open = [start]
        # print(self.heuristic(self.open[0]))
        self.closed = []
        while self.open:
            current = self.open.pop(0)
            self.closed.append(current)
            self.number_of_expanded_nodes += 1
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
            
            # put the current fscore in the heap
            heapq.heapify(self.open)

            # get the lowest fscore from the heap
            self.open = heapq.nsmallest(len(self.open), self.open, key=lambda x: (self.w * self.heuristic(x)))
            # epsilon greedy randomization
            if random.random() < self.epsilon:
                self.open = random.sample(self.open, len(self.open))
                #decay epsilon
                self.epsilon *= self.decay_rate
                # print(f"epsilon value: {self.epsilon}, decay value: {self.decay_rate}")
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


        
class AdaptiveBestEX(GBFS):
    """
    Adaptive Exploration Greedy Best First Search Algorithm
    """

    def __init__(self, w=1):
        super().__init__(w)

        

    def search(self, start, goal):
        self.open = [start]
        h_start = self.heuristic(start)

        self.closed = []
        while self.open:
            current = self.open.pop(0)

            self.closed.append(current)


            self.number_of_expanded_nodes += 1
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

            
            # put the current fscore in the heap
            heapq.heapify(self.open)

            # get the lowest fscore from the heap
            self.open = heapq.nsmallest(len(self.open), self.open, key=lambda x: (self.w * self.heuristic(x)))
            h_top = self.heuristic(current)
            self.epsilon = (h_top / h_start)/4
            # print(self.epsilon)
            # print(self.epsilon, h_start, h_top)

            # epsilon greedy randomization
            if random.random() < self.epsilon:
                self.open = random.sample(self.open, len(self.open))

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