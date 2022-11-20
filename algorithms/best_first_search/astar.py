from generic_defs.search_engine import *
import heapq

class AStar(SearchEngine):

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
                    heapq.heappush(self.open, (child.g + self.w * self.heuristic(child), self.closed.pop(self.closed.index(child))))
                # if child not in the heap
                # if child not in [x[1] for x in self.open]:
                child.parent = current
                child.action = action
                child.g = self.cost_function(current, action)
                heapq.heappush(self.open, (child.g + self.w * self.heuristic(child), child))
                # if child not in self.open:
                    # child.parent = current
                    # child.action = action
                    # child.g = self.cost_function(current, action)
                    # add to open
                    # heapq.heappush(self.open, (child.g + self.w * self.heuristic(child), child))
                # else:
                #     if child.g < current.g:
                #         # remove child from heap
                #         self.open = [x for x in self.open if x[1] != child]
                #         child.parent = current
                #         child.action = action
                #         # child.g = self.cost_function(current, action)
                #         # add to open
                #         heapq.heappush(self.open, (child.g + self.w * self.heuristic(child), child))
            # if tie breaking then sort the heap by the g value
            # self.open = heapq.nsmallest(len(self.open), self.open, key=lambda x: (x[0]))
                
            # put the current fscore in the heap
            # heapq.heapify(self.open)
            # get the lowest fscore from the heap
            # self.open = heapq.nsmallest(len(self.open), self.open, key=lambda x: (x.g + self.w * self.heuristic(x), x.g))
            # self.open.sort(key=lambda x: x.g + self.w * self.heuristic(x))
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