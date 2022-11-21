import sys
import os

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import the necessary packages
from generic_defs.search_engine import *
from algorithms.domains.SE_domain.se_domain import *
from algorithms.best_first_search.astar import *
from experiments.se_experiments.se_files.create_se_probs import *

PROBS_FILE = "se_files/se.probs"
MAX_NUM_OF_MODULES = 2
MAX_NUM_OF_CLASSES = 6
NUM_OF_PROBS = 1

SOL_FILE = "se_files/se_sol.txt"


def main():
    se_probs = CreateSeProbs(max_modules=MAX_NUM_OF_MODULES, max_classes=MAX_NUM_OF_CLASSES, num_of_probs=NUM_OF_PROBS)

    se_probs.create_probs()
    se_probs.write_probs_to_file(PROBS_FILE)  # writes problems in file

    se_domains = [SeProblemInstanceToSeDomainMapper.map(prob) for prob in se_probs.probs]

    sol_paths = []

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

        sol_paths.append(path)

        # print the path
        print(path)
        print(search_engine.statistics())

    with open(SOL_FILE, "w") as sol_file:
        for path in sol_paths:
            sol_file.write(path)


if __name__ == "__main__":
    main()
