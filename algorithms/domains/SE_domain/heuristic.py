class Heuristic:
    def __init__(self, state):
        self.state = state

    """A heuristic function maps states to costs."""
    def __call__(self, state):
        return 0


class CouplingHeuristic:
    def __init__(self, classes, modules, attributes):
        self.classes = classes
        self.modules = modules
        self.attributes = attributes

    def __call__(self, state):
        sum_natural_numbers = lambda n: (n-1) * n / 2
        # get outer module connections
        total_outer_module_connections = sum_natural_numbers(len(self.modules))
        # get inner module connections
        connections = 0 
        for classes in state.cell[1]:
            if classes.class1 != classes.class2:
                connections += 1

        return total_outer_module_connections - connections