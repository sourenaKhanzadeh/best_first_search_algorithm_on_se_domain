from typing import List, Tuple, Dict, Set, Optional, Union
import itertools
from .heuristic import *
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
            cost, next_state = self.transition_relation(state, action)
            if next_state is not None and cost is not None:
                yield action, next_state
            else:
                continue
        
    def get_action_cost(self, state, action):
        """
        Return g cost of action
        """
        return state.g + 1

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
            return self.name == other.name and self.class1 == other.class1 and self.class2 == other.class2
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
    def __init__(self, start_state, goal_state, heuristic = 'h1', aggression = 1):
        self.start_state = State(str(start_state), cell=start_state)
        self.goal_state = State(str(goal_state), cell=goal_state)
        self.states = [self.start_state, self.goal_state] 
        self.transition_system = self.create_transition_system()
        self.heuristic = self.heuristic(self.states[0], heuristic)
        self.cost_function = CostFunction(self.get_action_cost)
        self.goal_test = self.goal_test
        self.delete_trail = []
        self.add_trail = []
        self.aggression = aggression
        self.total_goal = 0
        for c in self.goal_state.cell[0]:
            for c2 in self.goal_state.cell[0]:
                if c != c2 and c.module == c2.module:
                    self.total_goal += 1
    def __str__(self):
        return 'SE_Domain({}, {})'.format(self.transition_system, self.states)

    def __repr__(self):
        return self.__str__()
    
    def create_transition_system(self):
        """
        Create a transition system for the graph
        """
        self.states = self.create_states()
        # actions = [Action("delete intra edge"), Action("delete inter edge"), Action("add intra edge"), Action("add inter edge")]
        actions = [ Action("add intra edge"), Action("delete inter edge")]
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
        # remove random intra edge (cohesion)
        # check if there is an intra edge
        if len(cell[0]) == 0:
            return None, None
        
        for c in cell[1]:
            if c.class1.module == c.class2.module and c not in self.delete_trail:
                # delete intra edge
                new_cell = [cell[0], cell[1][:], cell[2]]
                new_cell[1].remove(c)
                self.delete_trail.append(c)
                new_state = State(str(new_cell), cell=new_cell)
                return state.g + 10, new_state
        return None, None

    def delete_inter_edge(self, state):
        """
        Delete an inter edge
        """
        # remove random inter edge (coupling) where it's not the only link between 2 modules.
        cell = state.cell
        # check if there is an intra edge
        if len(cell[0]) == 0:
            return None, None
        inter_edges = {}
        
        for c in cell[1]:
            if c.class1.module != c.class2.module:
                if inter_edges.get((c.class1.module, c.class2.module), None) is None:
                    inter_edges[(c.class1.module, c.class2.module)] = [c]
                else:
                    inter_edges[(c.class1.module, c.class2.module)].append(c)

        for i in inter_edges.values():
            if len(i) > 1:
                # delete inter edge
                for j in i:
                    if j not in self.delete_trail:
                        self.delete_trail.append(j)
                        new_cell = [cell[0], cell[1][:], cell[2]]
                        new_cell[1].remove(j)
                        new_state = State(str(new_cell), cell=new_cell)
                        return state.g + 1, new_state

        return None, None

                    
    def add_intra_edge(self, state):
        """
        Add an intra edge
        """
        cell = state.cell
        # if len(cell[1]) > len(self.goal_state.cell[1]):
            # return None, None

        # # check if there is an intra edge
        # for classes in cell[0]:
        #     for classes2 in cell[0]:
        #         if classes.module == classes2.module and classes != classes2:
        #             for attribute in cell[1]:
        #                 if type(attribute) == tuple and len(attribute) == 1:
        #                     attribute = attribute[0]
        #                 # classes and classes2 in the same module are checked for presence of link in attributes.
        #                 # If not exists, add
        #                 if not (attribute.class1 == classes and attribute.class2 == classes2) and Attribute("a", classes, classes2) not in cell[1]:
        #                     # and Attribute("a", classes2, classes) not in self.add_trail:
        #                     new_cell = [cell[0], cell[1][:], cell[2]]
        #                     new_cell[1].append(Attribute("a", classes, classes2))
        #                     # self.add_trail.append(Attribute("a", classes, classes2))
        #                     new_state = State(str(new_cell), cell=new_cell)
        #                     return state.g + 1, new_state
        
        to_append = None
        # add every batch of classes in the same module
        for classes in cell[0]:
            for classes2 in cell[0]:
                if classes.module == classes2.module and classes != classes2:
                    if Attribute("a", classes, classes2) in cell[1] and Attribute("a", classes2, classes) in cell[1]:
                        continue
                    if Attribute("a", classes, classes2) not in cell[1] and Attribute("a", classes2, classes) not in cell[1]:
                        new_cell = [cell[0], cell[1][:], cell[2]]
                        new_cell[1].append(Attribute("a", classes, classes2))
                        self.add_trail.append(Attribute("a", classes, classes2))
                        new_state = State(str(new_cell), cell=new_cell)
                        return state.g + 1, new_state
                    if Attribute("a", classes, classes2) not in cell[1]: # prioritize when A(c,c2) and A(c2,c) both don't exist in cell[1]
                        to_append = Attribute("a", classes, classes2)
                    if Attribute("a", classes2, classes) not in cell[1]:
                        to_append = Attribute("a", classes2, classes)

        if to_append is not None:
            new_cell = [cell[0], cell[1][:], cell[2]]
            new_cell[1].append(to_append)
            self.add_trail.append(to_append)
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
        if len(cell[1]) > len(self.goal_state.cell[1]):
            return None, None

        # for classes in cell[0]:
            # for classes2 in cell[0]:
                # if classes.module != classes2.module:
                    # for attribute in cell[1]:
                        # if attribute.class1 == classes and attribute.class2 == classes2:
                            # return None, None
                    # if Attribute("a", classes, classes2) not in self.add_trail:
                        # new_cell = [cell[0], cell[1][:], cell[2]]
                        # new_cell[1].append(Attribute("a", classes, classes2))
                        # new_state = State(str(new_cell), cell=new_cell)
                        # self.add_trail.append(Attribute("a", classes, classes2))
                        # return state.g + 10, new_state
        return None, None
        
    def create_states(self):
        """
        Create all possible states for the graph
        """
        states = []
        attributes = []

        # connect all classes with each other
        # sample all possible combinations of classes
        # remove enumerate to add 2-directional edges in state space
        for i, classes in enumerate(self.start_state.cell[0]):
            for classes2 in self.start_state.cell[0]:
                if classes != classes2:
                    attributes.append(Attribute("a", classes, classes2))
        # sample all possible combinations of attributes
        for j in range(2, len(self.start_state.cell[1])):
            for i in itertools.combinations(attributes, j):
                new_cell = [self.start_state.cell[0], [*i], self.start_state.cell[2]]
                new_state = State(str(new_cell), cell=new_cell)
                states.append(new_state)
        #
        # print("all: ", len(states))
        # make sure that the goal state is in the list of states
        return states

    def heuristic(self, state, type="zero"):
        """
        Return the heuristic value of a state
        """
        if type == "zero":
            return Heuristic(state)
        elif type == "coupling":
            return CouplingHeuristic(state.cell[0], state.cell[1], state.cell[2])
        elif type == "cohesion":
            return CohesionHeuristic(state.cell[0], state.cell[1], state.cell[2])
        elif type == "AddCouplingCohesion":
            return AddCouplingCohesionHeuristic(state.cell[0], state.cell[1], state.cell[2])
        elif type == "MaxCouplingCohesion":
            return MaxCouplingCohesionHeuristic(state.cell[0], state.cell[1], state.cell[2])

        return Heuristic(state)
    
    def goal_test(self, state):
        return self.is_goal(state)

    def get_action_cost(self, state, action):
        """
        Return g cost of action
        """
        if action == Action("add inter edge"):
            return state.g + 10
        elif action == Action("add intra edge"):
            return state.g + 1
        elif action == Action("delete inter edge"):
            return state.g + 10
        elif action == Action("delete intra edge"):
            return state.g + 1
    def is_goal(self, state):
        # for attr in state.cell[1]:
            # if attr not in self.goal_state.cell[1]:
                # return False
        # if len(self.goal_state.cell[1]) != len(state.cell[1]):
            # return False
        # for attr in self.goal_state.cell[1]:
            # if attr not in state.cell[1]:
                # return False
        # check if attributes of the state and goal state are the same
        # if len(self.goal_state.cell[1]) != len(state.cell[1]):
            # return False
        # for attr in self.goal_state.cell[1]:
            # if attr not in state.cell[1]:
                # return False
        connections = 0 # coupling
        for classes in state.cell[1]:
            if classes.class1 != classes.class2 and classes.class1.module != classes.class2.module:
                connections += 1

        if len(state.cell[1]) >  self.total_goal * self.aggression and connections == 1:
            return True
        return False
    
    def __call__(self, *args, **kwds) :
        return self.successors(*args, **kwds)