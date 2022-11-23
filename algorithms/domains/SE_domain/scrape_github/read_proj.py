import os 
import sys

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# add the parent parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# add the parent parent parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
# add the parent parent parent parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

import json
from SE_domain.se_domain import *
from best_first_search.astar import *

PROJ_PATH = "projects.json"


class ProjReader:
    def __init__(self, proj_path):
        self.proj_path = proj_path
        self.projects = []
        self.read()

    def read(self):
        # read the json file
        with open(self.proj_path, 'r') as f:
            self.projects = json.load(f)

    def get_projects(self):
        return self.projects

class ProjParser:
    def __init__(self, project):
        self.project = project
        self.parsed_projects = []
        self.modules = []
        self.classes = []
        self.attributes = []
        self.parse()

    def parse(self):
        for proj in self.project:
            for attr in proj:
                class_1, class_2 = attr.split('->')
                module_1 = class_1.split('.')[0]
                module_2 = class_2.split('.')[0]
                class_1 = class_1.split('.')[1]
                class_2 = class_2.split('.')[1]
                if module_1 not in list(map(lambda x : x.name, self.modules)):
                    self.modules.append(Module(module_1, []))
                if module_2 not in list(map(lambda x : x.name, self.modules)):
                    self.modules.append(Module(module_2, []))

                # find module_1 in list of modules
                module_1 = list(filter(lambda x : x.name == module_1, self.modules))[0]
                module_2 = list(filter(lambda x : x.name == module_2, self.modules))[0]
                if class_1 not in list(map(lambda x : x.name, self.classes)):
                    self.classes.append(Class(class_1, module_1))
                if class_2 not in list(map(lambda x : x.name, self.classes)):
                    self.classes.append(Class(class_2, module_2))
                
                # find class_1 and class_2 in the list of classes
                class_1 = list(filter(lambda x : x.name == class_1, self.classes))[0]
                class_2 = list(filter(lambda x : x.name == class_2, self.classes))[0]
                
                self.attributes.append(Attribute('a', class_1, class_2))
                
                if class_1 not in module_1.classes:
                    module_1.classes.append(class_1)
                if class_2 not in module_2.classes:
                    module_2.classes.append(class_2)
                    # if m.name == module_2 and class_2 not in m.classes:
                        # m.classes.append(class_2)
        self.parsed_projects.append([self.classes, self.attributes, len(self.modules)])

    def get_parsed_project(self):
        return self.parsed_projects

if __name__ == "__main__":
    proj_reader = ProjReader(PROJ_PATH)
    print(proj_reader.get_projects())
    proj_parser = ProjParser(proj_reader.get_projects()[1].values())
    parsed_project = proj_parser.get_parsed_project()
    print(parsed_project[0])
    se = SEDomain(parsed_project[0], parsed_project[0], heuristic='zero', aggression=1)

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