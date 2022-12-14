class Heuristic:
    def __init__(self, state):
        self.state = state

    """A heuristic function maps states to costs."""
    def __call__(self, state):
        return 0


class CouplingHeuristic:
    def __init__(self, coupling_goal):
        self.coupling_goal = coupling_goal

    def __call__(self, state):
        # # calculate difference between current number of inter edges and goal's number of inter edges (len(modules)*len(modules)-1)
        # sum_natural_numbers = lambda n: (n-1) * n / 2
        # # get outer module connections
        # total_outer_module_connections = sum_natural_numbers(len(self.modules))
        # get inter module connections
        connections = 0 
        for classes in state.cell[1]:
            if classes.class1 != classes.class2 and classes.class1.module != classes.class2.module:
                connections += 1

        return abs(self.coupling_goal - connections)


class CohesionHeuristic:
    def __init__(self, cohesion_goal):
        self.cohesion_goal = cohesion_goal

    def __call__(self, state):
        # # calculate difference between sum of current number of intra edges in all modules and
        # # goal's number of intra modules (sum for each module(len(m_classes)*(len(m_classes)-1))
        # goal_cohesion_links_count = 0
        #
        # for m in self.modules:
        #     goal_cohesion_links_count += len(m.classes)*(len(m.classes)-1)

        # get intra module connections
        connections = 0
        for edge in state.cell[1]:
            if edge.class1 != edge.class2 and edge.class1.module == edge.class2.module:
                connections += 1

        return -1 * abs(self.cohesion_goal - connections)


class AddCouplingCohesionHeuristic:
    def __init__(self, coupling_goal, cohesion_goal):
        self.coupling_goal = coupling_goal
        self.cohesion_goal = cohesion_goal

    def __call__(self, state):
        return CohesionHeuristic(self.cohesion_goal)(state) + CouplingHeuristic(self.coupling_goal)(state)


class MaxCouplingCohesionHeuristic:
    def __init__(self, coupling_goal, cohesion_goal):
        self.coupling_goal = coupling_goal
        self.cohesion_goal = cohesion_goal

    def __call__(self, state):
        return max(CohesionHeuristic(self.cohesion_goal)(state), CouplingHeuristic(self.coupling_goal)(state))