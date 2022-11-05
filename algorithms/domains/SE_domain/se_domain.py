class TransitionSystem:
    def __init__(self, states, actions, transition_relation, init, goals):
        self.states = states
        self.actions = actions
        self.transition_relation = transition_relation
        self.init = init
        self.goals = goals

    def __str__(self):
        return 'TransitionSystem({}, {}, {}, {}, {})'.format(
            self.states, self.actions, self.transition_relation, self.init, self.goals)

    def __repr__(self):
        return self.__str__()
    
    def successors(self, state):
        """Return a list of (action, next_state) pairs reachable from |state|."""
        for action in self.actions:
            if self.transition_relation(state, action)[1]  is not None:
                yield action, self.transition_relation(state, action)[1]
            else:
                continue
    def get_action_cost(self, state, action):
        """
        Return g cost of action
        """
        return self.transition_relation(state, action)[0]

    def is_goal(self, state):
        return state in self.goals
    
    def __call__(self, *args, **kwds) :
        return self.successors(*args, **kwds)

class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def __str__(self):
        return 'Graph({}, {})'.format(self.nodes, self.edges)

    def __repr__(self):
        return self.__str__()
    
class Edge:
    def __init__(self, start, end, cost):
        self.start = start
        self.end = end
        self.cost = cost

    def __str__(self):
        return 'Edge({}, {}, {})'.format(self.start, self.end, self.cost)

    def __repr__(self):
        return self.__str__()

class Node:
    def __init__(self, name, cell=None, parent = None, g = 1):
        self.name = name
        self.g = g
        self.parent = parent
        self.cell = cell

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if type(other) == type(self):
            return self.name == other.name
        elif type(other) == list:
            return self.name == other
        else:
            return False

    def __hash__(self):
        return hash(self.name)

class Action:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if type(other) == type(self):
            return self.name == other.name
        elif type(other) == list:
            return self.name == other
        else:
            return False

    def __hash__(self):
        return hash(self.name)

class CostFunction:

    def __init__(self, cost):
        self.cost = cost

    def __str__(self):
        return 'CostFunction({})'.format(self.cost)

    def __repr__(self):
        return self.__str__()

    def __call__(self, *args, **kwds):
        return self.cost(*args, **kwds)

class SEDomain:
    def __init__(self, graph, start_state, goal_state): 
        self.graph = graph
        self.start_state = start_state
        self.goal_state = goal_state
        self.transition_system = self.create_transition_system()
        self.heuristic = self.heuristic
        self.cost_function = CostFunction(self.get_action_cost)
        self.goal_test = self.goal_test

    def __str__(self):
        return 'SE_Domain({}, {})'.format(self.transition_system, self.graph)

    def __repr__(self):
        return self.__str__()
    
    def create_transition_system(self):
        """
        Create a transition system for the graph
        """
        states = self.graph.nodes
        actions = [Action("delete intra edge"), Action("delete inter edge"), Action("add intra edge"), Action("add inter edge")]
        transition_relation = self.transition_relation
        init = self.start_state
        goals = self.goal_state
        return TransitionSystem(states, actions, transition_relation, init, goals)

    def transition_relation(self, state, action):
        """
        Return a tuple of (cost, next_state) for a given state and action
        """
        if action == Action("delete intra edge"):
            for edge in self.graph.edges:
                if edge.start == state and edge.end == state:
                    return (edge.cost, None)
        elif action == Action("delete inter edge"):
            for edge in self.graph.edges:
                if edge.start == state:
                    return (edge.cost, None)
        elif action == Action("add intra edge"):
            for edge in self.graph.edges:
                if edge.start == state and edge.end == state:
                    return (edge.cost, None)
        elif action == Action("add inter edge"):
            for edge in self.graph.edges:
                if edge.start == state:
                    return (edge.cost, None)
        return (0, None)

    def heuristic(self, state):
        """
        Return the heuristic value of a state
        """
        return 0
    
    def goal_test(self, state):
        return self.is_goal(state)

    def successors(self, state):
        """Return a list of (action, next_state) pairs reachable from |state|."""
        for action in self.transition_system.actions:
            if self.transition_system.transition_relation(state, action)[1]  is not None:
                yield action, self.transition_system.transition_relation(state, action)[1]
            else:
                continue
    def get_action_cost(self, state, action):
        """
        Return g cost of action
        """
        return self.transition_system.transition_relation(state, action)[0]

    def is_goal(self, state):
        return state == self.transition_system.goals
    
    def __call__(self, *args, **kwds) :
        return self.successors(*args, **kwds)