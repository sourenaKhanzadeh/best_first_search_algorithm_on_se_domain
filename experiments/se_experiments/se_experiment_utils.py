import os
import sys

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# add the parent parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# import the necessary packages
from enum import Enum
from algorithms.best_first_search.astar import *
from experiments.se_experiments.se_files.create_se_probs import *

PROBS_FILE = "se_files/se.probs"
SOL_FILE = "se_files/se_sol.txt"


class Heuristic(Enum):
    ZERO = "zero"
    COUPLING = "coupling"
    COHESION = "cohesion"
    AddCouplingCohesion = "AddCouplingCohesion"
    MaxCouplingCohesion = "MaxCouplingCohesion"


def write_sol_to_file(filename, list_to_write, indices=[]):
    with open(filename, "w+") as f:
        for obj_to_write in list_to_write:
            if len(indices) == 0:
                to_write = obj_to_write
            else:
                to_write = ""
                for i in indices:
                    to_write += str(obj_to_write[i]) + ","
                to_write = to_write[:-1]
            f.write(to_write + '\n')


def run_experiment(probs, heuristic=Heuristic.ZERO, print_paths=False, print_stats=False):

    se_domains = [SeProblemInstanceToSeDomainMapper.map(prob, heuristic=heuristic, aggression=1) for prob in probs]

    to_return = {"sol_paths": [], "sol_stats": []}

    for se_domain in se_domains:
        search_engine = AStar()
        # set the transition syxstem
        search_engine.setTransitionSystem(se_domain.transition_system)
        # set the heuristic
        search_engine.setHeuristic(se_domain.heuristic)
        # set the cost function
        search_engine.setCostFunction(se_domain.cost_function)

        # set the goal test
        search_engine.setGoalTest(se_domain.goal_test)
        # set the start state
        search_engine.setStartState(se_domain.start_state)
        # search
        path = search_engine.search(se_domain.start_state, se_domain.goal_state)

        to_return["sol_stats"].append(search_engine.statistics())
        to_return["sol_paths"].append(path)

        # print the path
        if print_paths:
            print(path)
        if print_stats:
            print(search_engine.statistics())
    return to_return
