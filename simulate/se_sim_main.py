import os
import sys

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# add the parent parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# import the necessary packages
from algorithms.best_first_search.astar import *
from algorithms.domains.SE_domain.se_domain import *
from domain.se.se import *

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()