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

    def __str__(self):
        return 'TransitionSystem with %d states' % len(self.states)
    
    def __call__(self, *args, **kwds) :
        return self.successors(*args, **kwds)

class State(object):
    """A state in a transition system."""
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
        states = [State(str(cell), cell=cell) for row in self.grid.cells for cell in row]
        
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
        initial_state = State(str(self.start), cell=self.start)

        # return the initial state
        return initial_state

    def create_goal_states(self):
        # create the goal states
        goal_states = [State(str(self.goal), cell=self.goal)]

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
        # get the cell from the state
        cell = state.cell

        # get the next cell based on the action
        next_cell = self.get_next_cell(cell, action)

        # check if the next cell is valid
        if not self.is_valid_cell(next_cell):
            return False

        # check if the next cell is the wall
        if self.is_wall(next_cell):
            return False
            
        # check if the next cell is the goal
        if next_cell == self.goal:
            return True

        # check if the next cell is the same as the next state
        if next_cell == next_state.cell:
            return True

        # return false if the transition is not valid
        return False
    
    def get_next_cell(self, cell, action):
        # get the next cell based on the action
        if action == Action('up') and cell.y > 0:
            return self.grid[cell.x, cell.y - 1]
        elif action == Action('down') and cell.y < self.grid.height - 1:
            return self.grid[cell.x, cell.y + 1]
        elif action == Action('left') and cell.x > 0:
            return self.grid[cell.x - 1, cell.y]
        elif action == Action('right') and cell.x < self.grid.width - 1:
            return self.grid[cell.x + 1, cell.y]
        else:
            return cell

    def is_valid_cell(self, cell):
        # check if the cell is valid
        if cell.x >= 0 and cell.x < self.grid.width and cell.y >= 0 and cell.y < self.grid.height:
            # return True
            return True
        # return False
        return False

    def is_wall(self, cell):
        # check if the cell is a wall
        if cell.value == 0:
            # return True
            return True
        # return False
        return False

    def is_goal(self, cell):
        # check if the cell is the goal
        if cell.x == self.goal.x and cell.y == self.goal.y:
            # return True
            return True
        # return False
        return False

    