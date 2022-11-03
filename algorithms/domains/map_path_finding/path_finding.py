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
        return self.states

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
        # create a set of states
        states = set()
        # create a set of actions
        actions = set()
        # create a transition relation
        transition_relation = dict()

        # create a set of goal states
        goals = []
        # create a cost function
        cost_function = CostFunction()

        # create a heuristic function
        heuristic = Heuristic()

        # create a set of cells
        cells = set()
        # loop over the grid
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                # create a cell
                cell = self.grid[x, y]
                # add the cell to the set of cells
                cells.add(cell)
                # create a state
                state = State(f"({cell.x}, {cell.y})")
                # add the state to the set of states
                states.add(state)
                # create a goal state
                if cell.x == self.goal[0] and cell.y == self.goal[1]:
                    # add the state to the set of goal states
                    goals.append(state)
                # create a start state
                if cell.x == self.start[0] and cell.y == self.start[1]:
                    # set the initial state
                    init = state

                # create a set of actions
                action_set = set()
                # check if the cell is not a wall
                if cell.value != 0:
                    # check if the cell is not on the left edge
                    if cell.x > 0:
                        # create a left action
                        left_action = Action("left")
                        # add the left action to the set of actions
                        actions.add(left_action)
                        # add the left action to the set of actions
                        action_set.add(left_action)
                        # create a left state
                        left_state = State(f"({cell.x - 1}, {cell.y})", parent=state)
                        # add the left state to the
                        states.add(left_state)
                        # add the left state to the set of states
                        states.add(left_state)
                        # add the transition to the transition relation
                        transition_relation[(state, left_action, left_state)] = Cost(1)
                    # check if the cell is not on the right edge
                    if cell.x < self.grid.width - 1:
                        # create a right action
                        right_action = Action("right")
                        # add the right action to the set of actions
                        actions.add(right_action)
                        # add the right action to the set of actions
                        action_set.add(right_action)
                        # create a right state
                        right_state = State(f"({cell.x + 1}, {cell.y})", parent=state)
                        # add the right state to the set of states
                        states.add(right_state)
                        # add the transition to the transition relation
                        transition_relation[(state, right_action, right_state)] = Cost(1)
                    # check if the cell is not on the top edge
                    if cell.y > 0:
                        # create a up action
                        up_action = Action("up")
                        # add the up action to the set of actions
                        actions.add(up_action)
                        # add the up action to the set of actions
                        action_set.add(up_action)
                        # create a up state
                        up_state = State(f"({cell.x}, {cell.y - 1})", parent=state)
                        # add the up state to the set of states
                        states.add(up_state)
                        # add the transition to the transition relation
                        transition_relation[(state, up_action, up_state)] = Cost(1)
                    # check if the cell is not on the bottom edge
                    if cell.y < self.grid.height - 1:
                        # create a down action
                        down_action = Action("down")
                        # add the down action to the set of actions
                        actions.add(down_action)
                        # add the down action to the set of actions
                        action_set.add(down_action)
                        # create a down state
                        down_state = State(f"({cell.x}, {cell.y + 1})", parent=state)
                        # add the down state to the set of states
                        states.add(down_state)
                        # add the transition to the transition relation
                        transition_relation[(state, down_action, down_state)] = Cost(1)

                # add the action set to the transition relation
                transition_relation[state] = action_set

        # create a transition system
        transition_system = TransitionSystem(states, actions, transition_relation, init, goals)
        # return the transition system
        return transition_system

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