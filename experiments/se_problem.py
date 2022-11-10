import sys
import os

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import the necessary packages
from generic_defs.search_engine import *
from algorithms.domains.SE_domain.se_domain import *
from algorithms.best_first_search.astar import *

def main():
    
    modules = [Module('0', []), Module('1', [])]
    classes = [Class('0', modules[0]), Class('1', modules[0]), Class('2', modules[0]),
               Class('3', modules[1]), Class('4', modules[1]), Class('5', modules[1])]
    for i in range(3):
        modules[0].classes.append(classes[i])
    for i in range(3, 6):
        modules[1].classes.append(classes[i])
    
    attributes = [Attribute('a', classes[0], classes[1]), Attribute('a', classes[0], classes[2]),
                  Attribute('a', classes[3], classes[2]), Attribute('a', classes[4], classes[5]),
                  Attribute('a', classes[3], classes[4]), Attribute('a', classes[5], classes[1])]
    goal_attributes = [Attribute('a', classes[0], classes[1]), Attribute('a', classes[0], classes[2]),
                    Attribute('a', classes[3], classes[2]), Attribute('a', classes[1], classes[2]),
                    Attribute('a', classes[5], classes[3]),
                    Attribute('a', classes[3], classes[4]), Attribute('a', classes[4], classes[5])]

    se = SEDomain([classes, attributes, len(modules)], [classes, goal_attributes, len(modules)], "h1")

    search_engine = AStar()
    # set the transition system
    search_engine.setTransitionSystem(se.transition_system)
    # set the heuristic
    search_engine.setHeuristic(se.heuristic)
    # set the cost function
    search_engine.setCostFunction(se.cost_function)

    # set the goal test
    search_engine.setGoalTest(se.goal_test)
    # set the start state
    search_engine.setStartState(se.start_state)
    # search
    path = search_engine.search(se.start_state, se.goal_state)
    # print the path
    print(path)
    print(search_engine.statistics())

if __name__ == "__main__":
    main()