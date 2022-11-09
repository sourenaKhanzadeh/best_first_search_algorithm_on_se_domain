from typing import List, Tuple, Dict, Set, Optional, Union
import itertools
from .heuristic import *


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
        return state[1] in self.goals[1]
    
    def __call__(self, *args, **kwds) :
        return self.successors(*args, **kwds)

class Class:
    def __init__(self, name, module):
        self.name = name
        self.module = module

    def __str__(self):
        return f"{self.name}"

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

class Module:
    def __init__(self, name, classes):
        self.name = name
        self.classes = classes

    def __str__(self):
        return f"{self.name}: {self.classes}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if type(other) == type(self):
            return self.name == other.name
        elif type(other) == list:
            return self.name == other
        else:
            return False

    def __hash__(self):
        return hash(self.name)

class Attribute:
    def __init__(self, name, class1, class2):
        self.name = name
        self.class1 = class1
        self.class2 = class2

    def __str__(self):
        return f"{self.class1} -> {self.class2}"

    def __repr__(self):
        return f"{self.class1} -> {self.class2}"

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
    def __init__(self, name, cell: List[Union[List[Class], List[Attribute], int]]=None, parent = None, g = 1):
        self.name = name
        self.g = g
        self.parent = parent
        self.cell = cell

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if type(other) == type(self):
            return self.name == other.name
        elif type(other) == list:
            return self.name == other
        else:
            return False
    def __lt__(self, other):
        return self.g < other.g

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
    def __init__(self, start_state, goal_state, heuristic = 'h1'):
        self.start_state = State(str(start_state), cell=start_state)
        self.goal_state = State(str(goal_state), cell=goal_state)
        self.states = [self.start_state, self.goal_state] 
        self.transition_system = self.create_transition_system()
        self.heuristic = self.heuristic(self.states[0], heuristic)
        self.cost_function = CostFunction(self.get_action_cost)
        self.goal_test = self.goal_test

    def __str__(self):
        return 'SE_Domain({}, {})'.format(self.transition_system, self.states)

    def __repr__(self):
        return self.__str__()
    
    def create_transition_system(self):
        """
        Create a transition system for the graph
        """
        self.states = self.create_states()
        actions = [Action("delete intra edge"), Action("delete inter edge"), Action("add intra edge"), Action("add inter edge")]
        transition_relation = self.transition_relation
        init = self.start_state
        goals = self.goal_state
        return TransitionSystem(self.states, actions, transition_relation, init, goals)

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
            return None, None
    
    def delete_intra_edge(self, state):
        """
        Delete an intra edge
        """
        cell = state.cell
        # check if there is an intra edge
        if len(cell[0]) == 0:
            return None, None
        
        for c in cell[1]:
            if c.class1.module == c.class2.module:
                # delete intra edge
                new_cell = [cell[0], cell[1][:], cell[2]]
                new_cell[1].remove(c)
                new_state = State(str(new_cell), cell=new_cell)
                return state.g + 1, new_state
        return None, None

    def delete_inter_edge(self, state):
        """
        Delete an inter edge
        """
        cell = state.cell
        # check if there is an intra edge
        if len(cell[0]) == 0:
            return None, None
        
        for c in cell[1]:
            if c.class1.module != c.class2.module:
                # delete intra edge
                new_cell = [cell[0], cell[1][:], cell[2]]
                new_cell[1].remove(c)
                new_state = State(str(new_cell), cell=new_cell)
                return state.g + 1, new_state
        return None, None

                    
    def add_intra_edge(self, state):
        """
        Add an intra edge
        """
        cell = state.cell
        
        # check if there is an intra edge
        for classes in cell[0]:
            for classes2 in cell[0]:
                if classes.module == classes2.module:
                    for attribute in cell[1]:
                        if attribute.class1 == classes and attribute.class2 == classes2:
                            return None, None
                    new_cell = [cell[0], cell[1][:], cell[2]]
                    new_cell[1].append(Attribute("a", classes, classes2))
                    new_state = State(str(new_cell), cell=new_cell)
                    return state.g + 1, new_state
        return None, None

    
    def add_inter_edge(self, state):
        """
        Add an inter edge
        """
        cell = state.cell
        # check if there is an inter edge
        if len(cell[1]) == 0:
            return None, None

        for classes in cell[0]:
            for classes2 in cell[0]:
                if classes.module != classes2.module:
                    for attribute in cell[1]:
                        if attribute.class1 == classes and attribute.class2 == classes2:
                            return None, None
                    new_cell = [cell[0], cell[1][:], cell[2]]
                    new_cell[1].append(Attribute("a", classes, classes2))
                    new_state = State(str(new_cell), cell=new_cell)
                    return state.g + 1, new_state
        return None, None
        
    def create_states(self):
        """
        Create all possible states for the graph
        """
        states = []
        attributes = []
        states.append(self.start_state)

        # connect all classes with each other
        # sample all possible combinations of classes
        for classes in self.start_state.cell[0]:
            for classes2 in self.start_state.cell[0]:
                attributes.append(Attribute("a", classes, classes2))
        # sample all possible combinations of attributes
        for j in range(1, len(self.start_state.cell[1])):
            for i in itertools.combinations(attributes, j):
                new_cell = [self.start_state.cell[0], [i], self.start_state.cell[2]]
                new_state = State(str(new_cell), cell=new_cell)
                states.append(new_state)
                        
        # make sure that the goal state is in the list of states
        return states

    def heuristic(self, state, type="h1"):
        """
        Return the heuristic value of a state
        """
        if type == "h1":
            return Heuristic(state)
        elif type == "h2":
            return CouplingHeuristic(state.cell[0], state.cell[1], state.cell[2])
        
        return Heuristic(state)
    
    def goal_test(self, state):
        return self.is_goal(state)

    def get_action_cost(self, state, action):
        """
        Return g cost of action
        """
        return self.transition_system.transition_relation(state, action)[0]

    def is_goal(self, state):
        for attr in state.cell[1]:
            if attr != self.goal_state.cell[1]:
                return False
        return True
    
    def __call__(self, *args, **kwds) :
        return self.successors(*args, **kwds)