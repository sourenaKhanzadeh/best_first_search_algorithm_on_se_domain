import copy
import random

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
                yield action, State(str(self.transition_relation(state, action)[1]),
                cell=self.transition_relation(state, action)[1], 
                g=self.transition_relation(state, action)[0])
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
    def __init__(self, nodes, edges, outer_edges):
        self.nodes = nodes
        self.edges = edges
        self.outer_edges = outer_edges

    def __str__(self):
        return 'Graph({}, {})'.format(self.nodes, self.edges)

    def __repr__(self):
        return self.__str__()

class Modules:
    def __init__(self, graphs):
        self.graphs = graphs

    def __str__(self):
        return 'Modules({})'.format(self.graphs)

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

class State:
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
    def __iter__(self):
        return self.cell.__iter__()

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
    def __init__(self, modules, start_state, goal_state): 
        self.modules = modules
        self.start_state = State(str(start_state), cell=start_state)
        self.goal_state = State(str(goal_state), cell=goal_state)
        self.transition_system = self.create_transition_system()
        self.heuristic = self.heuristic
        self.cost_function = CostFunction(self.get_action_cost)
        self.goal_test = self.goal_test

    def __str__(self):
        return 'SE_Domain({}, {})'.format(self.transition_system, self.modules)

    def __repr__(self):
        return self.__str__()
    
    def create_transition_system(self):
        """
        Create a transition system for the graph
        """
        states = self.modules
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
            return self.delete_intra_edge(state)
        elif action == Action("delete inter edge"):
            return self.delete_inter_edge(state)
        elif action == Action("add intra edge"):
            return self.add_intra_edge(state)
        elif action == Action("add inter edge"):
            return self.add_inter_edge(state)
        else:
            return None
    
    def delete_intra_edge(self, state):
        """
        Delete an intra edge
        """
        cost = 1
        new_state = copy.deepcopy(state)
        # get a random intra edge
        for graph in new_state.cell:
            if len(graph.edges) > 0:
                edge = random.choice(graph.edges)
                graph.edges.remove(edge)
                return cost, new_state
        return None, None

    def delete_inter_edge(self, state):
        """
        Delete an inter edge
        """
        cost = 1
        new_state = copy.deepcopy(state)
        for graph in new_state:
            if len(graph.outer_edges) > 0:
                edge = random.choice(graph.outer_edges)
                graph.outer_edges.remove(edge)
                return cost, new_state
        return None, None

    def add_intra_edge(self, state):
        """
        Add an intra edge
        """
        cost = 1
        new_state = copy.deepcopy(state)
        for graph in new_state:
            if len(graph.nodes) > 1:
                node1 = random.choice(graph.nodes)
                node2 = random.choice(graph.nodes)
                if node1 != node2:
                    edge = Edge(node1, node2, 1)
                    graph.edges.append(edge)
                    return cost, new_state
        return None, None

    def add_inter_edge(self, state):
        """
        Add an inter edge
        """
        cost = 1
        new_state = copy.deepcopy(state)
        for graph in new_state:
            if len(graph.nodes) > 1:
                node1 = random.choice(graph.nodes)
                node2 = random.choice(graph.nodes)
                if node1 != node2:
                    edge = Edge(node1, node2, 1)
                    graph.outer_edges.append(edge)
                    return cost, new_state
        return None, None

    def heuristic(self, state):
        """
        Return the heuristic value of a state
        """
        return 0
    
    def goal_test(self, state):
        return self.is_goal(state)

    def get_action_cost(self, state, action):
        """
        Return g cost of action
        """
        return self.transition_system.transition_relation(state, action)[0]

    def is_goal(self, state):
        return state == self.transition_system.goals
    
    def __call__(self, *args, **kwds) :
        return self.successors(*args, **kwds)