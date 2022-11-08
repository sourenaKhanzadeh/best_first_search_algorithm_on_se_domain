class Node:
    def __init__(self, val, parent = None, g=0, h=0):
        self.val = str(val)
        self.parent = parent
        self.g = g
        self.h = h

    def __str__(self):
        return self.val

    def __repr__(self):
        return self.val

    def __eq__(self, other):
        return self.val == other.val

    def __hash__(self):
        return hash(self.val)
    
    def __lt__(self, other):
        return self.g <= other.g


class Graph():
    def __init__(self, V=[], E=[]):
        self.V = V
        self.E = E
        self.goal_state = None
        self.start_state = None

    def transition(self, state, action, next_state):
        for i,j in self.E:
            if ((i == state and j == next_state)): #or (i == next_state and j == state)): # bi-directional graph - directions don't matter
                return True
        return False

    def transition_system(self,n=0,m=0):
        return TransitionSystem(
            states=self.V,
            actions=[Action("traverse_edge")],
            transition_relation=lambda state, action, next_state: self.transition(state, action, next_state),
            init=self.start_state,
            goals=[self.goal_state]
        )

    def goal_test(self, state):
        return state == self.goal_state

    def heuristic(self,n=0,m=0):
        return 0

    def cost_function(self, state, action):
        return state.g + 1

    def __repr__(self):
        return "V: " + str(self.V) +"\n" + "E: " + str(self.E)

    def __str__(self):
        return "V: " + str(self.V) +"\n" + "E: " + str(self.E)
class Action(object):
    """An action in a transition system."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

class TransitionSystem(object):
    """A transition system is a tuple (S, A, T, s0, G) where:
    - S is a set of states
    - A is a set of actions
    - T : S x A x S -> {0, 1} is a transition relation
    - s0 is the initial state
    - G is a set of goal states
    """
    def __init__(self, states, actions, transition_relation, init, goals):
        self.states = states
        self.actions = actions
        self.transition_relation = transition_relation
        self.init = init
        self.goals = goals

    def successors(self, state):
        """Return a list of (action, next_state) pairs reachable from |state|."""

        s = [(action, next_state)
             for action in self.actions
             for next_state in self.states
             if self.transition_relation(state, action, next_state)]
        # print(s)
        return s

    def is_goal(self, state):
        """Return true if |state| is a goal state."""
        return state in self.goals

    def cost(self, state, action, next_state):
        """Return the cost of taking |action| from |state| to |next_state|."""
        return state.g + 1

    def heuristic(self, state):
        """Return the heuristic cost of |state|."""
        return 0

    def __str__(self):
        return 'TransitionSystem with %d states' % len(self.states)

    def __call__(self, *args, **kwds) :
        return self.successors(*args, **kwds)