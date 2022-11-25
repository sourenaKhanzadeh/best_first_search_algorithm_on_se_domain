import sys
import os

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# add the parent parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# import the necessary packages
from experiments.se_experiments.se_experiment_utils import *

PROBS_FILE = "se_files/se.probs"
SOL_FILE = "se_files/se_sol.txt"

MIN_NUM_OF_MODULES = 1
MAX_NUM_OF_MODULES = 3
MIN_NUM_OF_CLASSES = 10
MAX_NUM_OF_CLASSES = 10
NUM_OF_PROBS = 200

heuristicc = ["zero", "coupling", "cohesion", "AddCouplingCohesion", "MaxCouplingCohesion"]


def main():
    se_probs = CreateSeProbs(min_modules=MIN_NUM_OF_MODULES,
                             max_modules=MAX_NUM_OF_MODULES,
                             min_classes=MIN_NUM_OF_CLASSES,
                             max_classes=MAX_NUM_OF_CLASSES,
                             num_of_probs=NUM_OF_PROBS)

    se_probs.create_probs()
    se_probs.write_probs_to_file(PROBS_FILE)  # writes problems in file

    solutions = run_experiment(se_probs.probs, print_paths=True, print_stats=True)

    write_sol_to_file(SOL_FILE, solutions["sol_paths"], indices=[1])



if __name__ == "__main__":
    main()
