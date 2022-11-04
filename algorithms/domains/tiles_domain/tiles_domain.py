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
    
    def is_goal(self, state):
        return state in self.goals
    
    def __call__(self, *args, **kwds) :
        return self.successors(*args, **kwds)

class State:
    def __init__(self, name, cell=None, parent = None, g = 0):
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
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class TilePuzzle:
    def __init__(self, size, init, goals):
        self.size = size
        self.init = State(str(init), cell=init)
        self.goals = State(str(goals[0]), cell=goals[0])
        self.actions = [Action('up'), Action('down'), Action('left'), Action('right')]
        self.states = [i for i in range(size * size)]
        self.states = self.permutate_list(self.states)
        self.states = [State(str(state), cell=state.index(0), parent=None, g=0) for state in self.states]
        
        self.transition_relation = self._transition_relation
        self.heuristic = self.heuristic
        self.cost_function = lambda s, a, s1: 1
        self.goal_test = lambda s: s == self.goals
        
    def _transition_relation(self, state, action):
        """
        Return true if |state|, |action|, and |next_state| form a valid transition.
        state: list of numbers
        action: Action
        next_state: list of numbers
        """
        # check if the action is valid
        if action not in self.actions:
            return False, None

        
        # check if the next state is reachable from the current state
        
        return True, self.apply_action(state, action)
    
    def apply_action(self, state, action):
        """
        Apply |action| to |state| and return the result.
        """
        if action == Action('up'):
            return self.move_up(state)
        elif action == Action('down'):
            return self.move_down(state)
        elif action == Action('left'):
            return self.move_left(state)
        elif action == Action('right'):
            return self.move_right(state)
        else:
            raise ValueError('Invalid action: {}'.format(action))
    
    def move_up(self, state):
        """
        Move the empty tile up.
        """
        if state.cell.index(0) < self.size:
            return None
        else:
            new_state = state.cell.index(0) - self.size
            return self.swap(state, new_state)

    def move_down(self, state):
        """
        Move the empty tile down.
        """
        if state.cell.index(0) >= (self.size * self.size) - self.size:
            return None
        else:
            new_state = state.cell.index(0) + self.size
            return self.swap(state, new_state)
    
    def move_left(self, state):
        """
        Move the empty tile left.
        """
        if state.cell.index(0) % self.size == 0:
            return None
        else:
            new_state = state.cell.index(0) - 1
            return self.swap(state, new_state)
    
    def move_right(self, state):
        """
        Move the empty tile right.
        """
        if state.cell.index(0) % self.size == self.size - 1:
            return None
        else:
            new_state = state.cell.index(0) + 1
            return self.swap(state, new_state)
    
    def swap(self, state, new_state):
        """
        Swap the empty tile with the tile at |new_state|.
        """
        temp = new_state
        new_state = state.cell[:]
        new_state[state.cell.index(0)], new_state[temp] = new_state[temp], new_state[state.cell.index(0)]
        new_state = State(str(new_state), cell=new_state)
        return new_state

    def __str__(self):
        return 'TilePuzzle({}, {}, {})'.format(self.size, self.init, self.goals)
    
    def __repr__(self):
        return self.__str__()
    
    def to_transition_system(self):
        return TransitionSystem(self.states, self.actions, self.transition_relation, self.init, self.goals)

    def heuristic(self, state):
        """
        Manhattan distance
        """
        return sum(abs(b % self.size - g % self.size) + abs(b // self.size - g // self.size) for b, g in ((state.cell.index(i), self.goals.cell.index(i)) for i in range(1, self.size * self.size)))
    
    def permutate_list(self, lst):
        """
        Permutate the list |lst| and return the result.
        """
        if len(lst) == 0:
            return []
        elif len(lst) == 1:
            return [lst]
        else:
            l = []
            for i in range(len(lst)):
                m = lst[i]
                rem_lst = lst[:i] + lst[i+1:]
                for p in self.permutate_list(rem_lst):
                    l.append([m] + p)
            return l