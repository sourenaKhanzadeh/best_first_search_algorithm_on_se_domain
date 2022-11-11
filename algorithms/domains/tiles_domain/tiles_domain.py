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
            if next_state  is not None:
                yield action, next_state
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

class State:
    def __init__(self, name, cells=None, parent = None, g = 0):
        self.name = name
        self.g = g
        self.parent = parent
        self.cell = cells

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
    
    def __lt__(self, other):
        return self.g < other.g

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
    def __init__(self, width, height, init, goals, cost_type='unit'):
        self.size = width * height
        self.width = width
        self.height = height
        self.init = State(str(init), cells=init)
        self.goals = State(str(goals[0]), cells=goals[0])
        self.actions = [Action('up'), Action('down'), Action('left'), Action('right')]
        # self.states = [i for i in range(self.size)]
        # self.states = self.permutate_list(self.states)
        # self.states = [State(str(state), cells=self.find_zero(state), parent=None, g=0) for state in self.states]
        self.states = [self.init]

        self.transition_relation = self._transition_relation
        self.heuristic = self.heuristic
        self.cost_function = self.cost_function
        self.goal_test = lambda s: s == self.goals

        self.cost_type = cost_type
        
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
        
        return True, self.apply_action(state, action)[1] if self.apply_action(state, action) else None

    def cost_function(self, state, action):
        """
        Return the cost of applying |action| in |state| to reach |next_state|.
        """
        return state.g + self.apply_action(state, action)[0]

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
        index = self.find_zero(state)
        if index >= self.width:
            return self.swap(state, index - self.width)
        return None

    def move_down(self, state):
        """
        Move the empty tile down.
        """
        index = self.find_zero(state)
        if index < self.size - self.width:
            return self.swap(state, index + self.width)
        return None

    def move_left(self, state):
        """
        Move the empty tile left.
        """
        index = self.find_zero(state)
        if index % self.width != 0:
            return self.swap(state, index - 1)
        return None

    def move_right(self, state):
        """
        Move the empty tile right.
        """
        index = self.find_zero(state)
        if index % self.width != self.width - 1:
            return self.swap(state, index + 1)
        return None
    
    def swap(self, state, new_state):
        """
        Swap the empty tile with the tile at |new_state|.
        """
        temp = new_state
        new_state = state.cell[:]
        index = self.find_zero(new_state)
        new_state[self.find_zero(state)], new_state[temp] = new_state[temp], new_state[self.find_zero(state)]
        if self.cost_type == 'unit':
            return 1, State(str(new_state), cells=new_state)
        elif self.cost_type == 'inverse':
            return 1/new_state[index], State(str(new_state), cells=new_state)
        elif self.cost_type == 'heavy':
            return new_state[index], State(str(new_state), cells=new_state)
        return 1, State(str(new_state), cells=new_state)
    
    def find_zero(self, state: State):
        """
        Find the index of the empty tile.
        """
        if type(state) == State:
            for i in range(len(state.cell)):
                if state.cell[i] == 0:
                    return i
        else:
            for i in range(len(state)):
                if state[i] == 0:
                    return i
        return None
    
    def find_other(self, state: State, i):
        """
        Find the index of the empty tile.
        """
        for j in range(len(state.cell)):
            if state.cell[j] == i:
                return j
        return None

    def __str__(self):
        return 'TilePuzzle({}, {}, {})'.format(self.size, self.init, self.goals)
    
    def __repr__(self):
        return self.__str__()
    
    def to_transition_system(self):
        return TransitionSystem(self.states, self.actions, self.transition_relation, self.init, self.goals)

    def heuristic(self, state):
        """
        Return the heuristic value of |state|.
        """
        return self.manhattan_distance(state)
    
    def manhattan_distance(self, state):
        """
        Return the manhattan distance of |state|.
        """
        distance = 0
        for i in range(len(state.cell)):
            if state.cell[i] != 0:
                distance += abs(i % self.width - self.find_other(self.goals, state.cell[i]) % self.width) + abs(i // self.width - self.find_other(self.goals, state.cell[i]) // self.width)
        return distance

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