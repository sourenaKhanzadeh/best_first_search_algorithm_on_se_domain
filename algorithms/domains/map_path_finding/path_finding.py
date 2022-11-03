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
        return [(action, next_state)
                for action in self.actions
                for next_state in self.states
                if self.transition_relation(state, action, next_state)]

    def is_goal(self, state):
        """Return true if |state| is a goal state."""
        return state in self.goals

    def cost(self, state, action, next_state):
        """Return the cost of taking |action| from |state| to |next_state|."""
        return 1

    def heuristic(self, state):
        """Return the heuristic cost of |state|."""
        return 0

    def __str__(self):
        return 'TransitionSystem with %d states' % len(self.states)
    
    def __call__(self, *args, **kwds) :
        return self.successors(*args, **kwds)

class State(object):
    """A state in a transition system."""
    def __init__(self, name, parent = None, g = 0, h = 0):
        self.name = name
        self.g = g
        self.h = h
        self.parent = parent

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

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

class Cell:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __str__(self):
        return f"({self.x}, {self.y}): {self.value}"

    def __repr__(self):
        return f"({self.x}, {self.y}): {self.value}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

class Grid(object):
    """A grid of cells."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell(x, y, 1) for y in range(height)]
                      for x in range(width)]

    def __getitem__(self, index):
        return self.cells[index[0]][index[1]]

    def __str__(self):
        return '\n'.join(' '.join(str(cell) for cell in row)
                         for row in self.cells)

class CostFunction(object):
    """A cost function maps (state, action, next_state) triples to costs."""
    def __call__(self, state, action, next_state):
        return 1

class Cost:
    def __init__(self, cost):
        self.cost = cost

    def __str__(self):
        return f"Cost: {self.cost}"

    def __repr__(self):
        return f"Cost: {self.cost}"

    def __eq__(self, other):
        return self.cost == other.cost

    def __hash__(self):
        return hash(self.cost)

class Heuristic(object):
    """A heuristic function maps states to costs."""
    def __call__(self, state):
        return 0

class Map:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal

        # create the transition system
        self.transition_system = self.create_transition_system()
        # set the start state
        self.start_state = self.transition_system.init
        # set the goal state
        self.goal_state = self.transition_system.goals[0]
        self.heuristic = self.create_heuristic()
        self.cost_function = self.create_cost_function()
        self.goal_test = self.transition_system.is_goal

    def create_transition_system(self):
        # create the transition system
        transition_system = TransitionSystem(
            states=self.create_states(),
            actions=self.create_actions(),
            transition_relation=self.create_transition_relation(),
            init=self.create_initial_state(),
            goals=self.create_goal_states()
        )

        # return the transition system
        return transition_system

    def create_states(self):
        # create the states
        states = [State(str(cell)) for row in self.grid.cells for cell in row]
        # make the parent attribute of each state a dictionary

        # return the states
        return states

    def create_actions(self):
        # create the actions
        actions = [Action('up'), Action('down'), Action('left'), Action('right')]

        # return the actions
        return actions
    
    def create_transition_relation(self):
        # create the transition relation
        transition_relation = lambda state, action, next_state: self.transition(state, action, next_state)

        # return the transition relation
        return transition_relation
    
    def create_initial_state(self):
        # create the initial state
        initial_state = State(str(self.start))

        # return the initial state
        return initial_state

    def create_goal_states(self):
        # create the goal states
        goal_states = [State(str(self.goal))]

        # return the goal states
        return goal_states

    def create_heuristic(self):
        # create a heuristic function
        heuristic = Heuristic()

        # return the heuristic function
        return heuristic

    def create_cost_function(self):
        # create a cost function
        cost_function = CostFunction()

        # return the cost function
        return cost_function
    
    def transition(self, state, action, next_state):
        # get the cell for the state
        cell = self.get_cell(state)
        # get the cell for the next state
        next_cell = self.get_cell(next_state)
        # check if the next cell is valid
        if self.is_valid_cell(next_cell):
            # check if the action is valid
            if self.is_valid_action(cell, action, state, next_state):
                # return true
                return True
        # return false
        return False
    
    def get_cell(self, state):
        # get the cell for the state
        cell = self.grid[int(state.name[1]), int(state.name[4])]
        # return the cell
        return cell
    
    def is_valid_cell(self, cell):
        # check if the cell is valid
        if cell.value == 1:
            # return true
            return True
        # return false
        return False

    def is_valid_action(self, cell, action, state, next_state):
        # check if the action is valid
        if action.name == 'up' and cell.y < self.grid.height - 1:

            # return true
            return True
        elif action.name == 'down' and cell.y > 0:
            # return true
            return True
        elif action.name == 'left' and cell.x > 0:
            # return true
            return True
        elif action.name == 'right' and cell.x < self.grid.width - 1:
            # return true
            return True
        # return false
        return False
    