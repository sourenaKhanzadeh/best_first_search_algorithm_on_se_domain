import os
import sys

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# add the parent parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# import the necessary packages
from experiments.se_experiments.se_experiment_utils import *

PROBS_FILE = "se_files/se.probs"
SOL_FILE = "se_files/se_sol.txt"

MIN_NUM_OF_MODULES = 3
MAX_NUM_OF_MODULES = 3
MIN_NUM_OF_CLASSES = 10
MAX_NUM_OF_CLASSES = 10
NUM_OF_PROBS = 100

sol_files = ["se_files/heuristic_experiments/se_sol_" + heuristic.value + ".txt" for heuristic in Heuristic]


def main():

    se_probs = CreateSeProbs(min_modules=MIN_NUM_OF_MODULES,
                             max_modules=MAX_NUM_OF_MODULES,
                             min_classes=MIN_NUM_OF_CLASSES,
                             max_classes=MAX_NUM_OF_CLASSES,
                             num_of_probs=NUM_OF_PROBS)

    se_probs.create_probs()
    se_probs.write_probs_to_file(PROBS_FILE)  # writes problems in file

    for i, heuristic in enumerate(Heuristic):
        solutions = run_experiment(se_probs.probs, heuristic=heuristic.value)

        write_sol_to_file(sol_files[i], solutions["sol_paths"], indices=[1])


if __name__ == "__main__":
    main()
