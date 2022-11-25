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
from algorithms.best_first_search.idastar import *
from algorithms.best_first_search.egreedy import *
from experiments.se_experiments.se_files.create_se_probs import *

import pandas as pd

PROBS_FILE = "se_files/se.probs"
MIN_NUM_OF_MODULES = 100
MAX_NUM_OF_MODULES = 1000
MAX_NUM_OF_CLASSES = 100000
NUM_OF_PROBS = 5

SOL_FILE = "se_files/se_sol.txt"
ALG_BENCHMARK_FILE = "se_alg_benchmark.csv"

AGGRESSIONS = [0.25, 0.5, 0.75, 1]

HEURISTICS = ["zero", "coupling", "cohesion", "AddCouplingCohesion", "MaxCouplingCohesion"]

__ALL__FILES__ = []


def test_algorithms(heuristic, aggression, file_name):
    algs = [AStar(), IDAStar(), GBFS()]

    se_probs = []

    with open(PROBS_FILE, "r") as probs_file:
        for line in probs_file:
            se_probs.append(SeProblemInstance.string_to_instance(line))
    
    se_domains = [SeProblemInstanceToSeDomainMapper.map(prob, heuristic=heuristic , aggression=aggression) for prob in se_probs]
    
    costs = dict()
    node_expansions = dict()

    for alg in algs:
        costs[alg.__class__.__name__] = []
        node_expansions[alg.__class__.__name__] = []
        for se_domain in se_domains:
            search_engine = alg
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

            costs[alg.__class__.__name__].append(search_engine.statistics()['cost'])
            node_expansions[alg.__class__.__name__].append(search_engine.statistics()['nodes_expanded'])

            # print the path
            print(path)
            print(search_engine.statistics())
    cost_data = pd.DataFrame(costs)
    node_expansions_data = pd.DataFrame(node_expansions)

    # append cost data to node expansions data as data 
    for alg in algs:
        node_expansions_data[alg.__class__.__name__ + "_cost"] = cost_data[alg.__class__.__name__]
    # change alg names to alg names + node expansions
    node_expansions_data.columns = [alg.__class__.__name__ + "_n_expansions" for alg in algs] + [alg.__class__.__name__ + "_cost" for alg in algs]
    data = node_expansions_data

    data.to_csv(file_name, index=False, header=True)

def main():
    se_probs = CreateSeProbs(min_modules=MIN_NUM_OF_MODULES, max_modules=MAX_NUM_OF_MODULES, max_classes=MAX_NUM_OF_CLASSES, num_of_probs=NUM_OF_PROBS)

    se_probs.create_probs()
    se_probs.write_probs_to_file(PROBS_FILE)  # writes problems in file

    # se_probs = [#SeProblemInstance.string_to_instance("2;[(0, 1), (1, 0), (2, 0), (3, 0)];[(3, 0), (2, 0), (3, 2), (0, 1), (2, 1), (0, 3), (0, 2), (3, 1), (1, 0)]"),
    #             SeProblemInstance.string_to_instance("2;[(0, 1), (1, 0), (2, 1), (3, 0)];[(1, 2), (3, 0), (0, 2), (3, 2), (1, 0), (2, 3), (3, 1), (2, 1)]")]

    se_domains = [SeProblemInstanceToSeDomainMapper.map(prob, heuristic='zero', aggression=1) for prob in se_probs.probs]

    sol_stats = []
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

        sol_stats.append(search_engine.statistics())
        sol_paths.append(path)

        # print the path
        print(path)
        print(search_engine.statistics())

    # with open(SOL_FILE, "w") as sol_file:
    #     for stats in sol_stats:
    #         sol_file.write(str(stats) + '\n')
    with open(SOL_FILE, "w") as sol_file:
        for path in sol_paths:
            sol_file.write(str(len(path[1])) + " : " + str(path[1]) + '\n')


if __name__ == "__main__":
    # main()
    for h in HEURISTICS:
        for aggression in AGGRESSIONS:
            __ALL__FILES__.append(f"se_files/{aggression}_{h}_" + ALG_BENCHMARK_FILE)
            test_algorithms(h, aggression, __ALL__FILES__[-1])

