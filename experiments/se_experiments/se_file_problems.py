import sys
import os

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# add the parent parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# import the necessary packages
from generic_defs.search_engine import *
from algorithms.domains.SE_domain.se_domain import *
from algorithms.best_first_search.astar import *
from experiments.se_experiments.se_files.create_se_probs import *

PROBS_FILE = "se_files/se.probs"
MIN_NUM_OF_MODULES = 2
MAX_NUM_OF_MODULES = 3
MAX_NUM_OF_CLASSES = 4
NUM_OF_PROBS = 100

SOL_FILE = "se_files/se_sol.txt"


def main():
    se_probs = CreateSeProbs(min_modules=MIN_NUM_OF_MODULES, max_modules=MAX_NUM_OF_MODULES, max_classes=MAX_NUM_OF_CLASSES, num_of_probs=NUM_OF_PROBS)

    se_probs.create_probs()
    se_probs.write_probs_to_file(PROBS_FILE)  # writes problems in file

    # se_probs = [#SeProblemInstance.string_to_instance("2;[(0, 1), (1, 0), (2, 0), (3, 0)];[(3, 0), (2, 0), (3, 2), (0, 1), (2, 1), (0, 3), (0, 2), (3, 1), (1, 0)]"),
    #             SeProblemInstance.string_to_instance("2;[(0, 1), (1, 0), (2, 1), (3, 0)];[(1, 2), (3, 0), (0, 2), (3, 2), (1, 0), (2, 3), (3, 1), (2, 1)]")]

    se_domains = [SeProblemInstanceToSeDomainMapper.map(prob, heuristic='zero', aggression=1) for prob in se_probs.probs]

    sol_stats = []

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

        sol_stats.append(search_engine.statistics())

        # print the path
        print(path)
        print(search_engine.statistics())

    with open(SOL_FILE, "w") as sol_file:
        for stats in sol_stats:
            sol_file.write(str(stats))


if __name__ == "__main__":
    main()
