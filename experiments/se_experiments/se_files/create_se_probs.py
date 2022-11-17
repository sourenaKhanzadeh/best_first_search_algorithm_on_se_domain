import os
import sys
from random import choice
from random import randint

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import the necessary packages
from algorithms.domains.SE_domain.se_domain import *

PROBS_FILE = "se.probs"
MAX_NUM_OF_MODULES = 2
MAX_NUM_OF_CLASSES = 6
NUM_OF_PROBS = 100


class SeProblemInstance:
    def __init__(self, num_of_modules, classes, start_state_links):
        self.num_of_modules = num_of_modules
        self.classes = classes # [(c, m)] class c in module m
        self.start_state_links = start_state_links # [(i, j)] class i is linked with class j

    def __str__(self):
        return str(self.num_of_modules) + ";" + str(self.classes) + ";" + str(self.start_state_links)

    @classmethod
    def string_to_instance(cls, str_instance: str):
        lis = str_instance.strip().split(';')
        return SeProblemInstance(eval(lis[0]), eval(lis[1]), eval(lis[2]))


# TODO: Implement mapper in future to map back to domain and run A*
class SeProblemInstanceToSeDomainMapper:
    @classmethod
    def map(cls, se_problem_instance: SeProblemInstance) -> SEDomain:
        pass


class CreateSeProbs:
    def __init__(self, max_modules, max_classes, num_of_probs=100, min_modules=1, min_classes=1):
        self.min_classes = min_classes
        self.min_modules = min_modules
        self.max_modules = max_modules
        self.max_classes = max_classes
        self.num_of_probs = num_of_probs
        self.probs = [] # [SeProblemInstance]

    def _get_random_num_of_modules(self):
        return [randint(self.min_modules, self.max_modules) for _ in range(self.num_of_probs)]

    def _get_random_classes(self, num_of_modules):
        return [(i, randint(0, num_of_modules)) for i in range(randint(self.min_classes, self.max_classes))]

    def _get_random_links(self, num_of_classes):
        links = []
        total_num_of_links_possible = num_of_classes * (num_of_classes-1)
        for i in range(randint(0, total_num_of_links_possible)):
            random_link_from_class = randint(0, num_of_classes+1)
            random_link_to_class = choice(list(range(0, random_link_from_class)) + list(range(random_link_from_class, num_of_classes+1)))
            link = (random_link_from_class, random_link_to_class)
            while link in links:
                random_link_from_class = randint(0, num_of_classes+1)
                random_link_to_class = choice(list(range(0, random_link_from_class)) + list(range(random_link_from_class, num_of_classes+1)))
                link = (random_link_from_class, random_link_to_class)
            # append a unique link
            links.append(link)
        return links

    def _get_classes_with_stratified_modules(self):
        pass

    def _create_probs_with_more_intra_links(self):
        pass

    def _create_probs_with_more_inter_links(self):
        pass

    def create_probs(self, assign_to_modules_equally=False, more_intra_links=False, more_inter_links=False):
        modules = self._get_random_num_of_modules()
        classes = [self._get_random_classes(num_of_modules) for num_of_modules in modules]
        links = [self._get_random_links(len(classes[i])) for i in range(len(classes))]

        for i in range(self.num_of_probs):
            self.probs.append(SeProblemInstance(modules[i], classes[i], links[i]))

        # # TODO: add functionality for assign_to_modules_equally=False, more_intra_links=False, more_inter_links=False
        # if assign_to_modules_equally:
        #     classes = self._get_classes_with_stratified_modules()
        # else:
        #     classes =

    def write_probs_to_file(self, filename):
        with open(filename, 'w') as probs_file:
            for prob in self.probs:
                probs_file.write(str(prob) + '\n')


if __name__ == "__main__":
    se_probs = CreateSeProbs(max_modules=MAX_NUM_OF_MODULES, max_classes=MAX_NUM_OF_CLASSES, num_of_probs=NUM_OF_PROBS)

    se_probs.create_probs()
    se_probs.write_probs_to_file(PROBS_FILE)
