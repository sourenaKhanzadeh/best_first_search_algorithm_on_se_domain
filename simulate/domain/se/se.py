import pygame
from pygame.locals import *
from pygame.color import *

from algorithms.domains.SE_domain.se_domain import *
from algorithms.best_first_search.astar import *

pygame.init()

class ClassSE:
    """
    A cricle represents a state in the search space.
    """
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(self.x, self.y, radius * 2, radius * 2)
        self.color = color
        self.clicked = False
        self.number = 0

    def draw(self, win):
        """
        Draw a circle on the screen.
        """
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 1)
             

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked = True
            self.color = (255, 0 , 0)
        else:
            self.clicked = False

    def drag(self, pos):
        if self.clicked:
            self.x = pos[0]
            self.y = pos[1]
            self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

class ModuleSE:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.clicked = False
        self.classes = []

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, 1)
        for c in self.classes:
            c.draw(win)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked = True
            print("clicked")
        else:
            self.clicked = False
        
        for c in self.classes:
            c.click(pos)

    def drag(self, pos):
        # drag the module with the classes inside
        if self.clicked:
            self.x = pos[0]
            self.y = pos[1]
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            # let the classes inside move with the module
            for c in self.classes:
                # keep the relative position of the class
                c.x = pos[0] + c.x - self.x
                c.y = pos[1] + c.y - self.y
                c.rect = pygame.Rect(c.x, c.y, c.radius * 2, c.radius * 2)

class AttributeSE:
    def __init__(self, class1:ClassSE, class2:ClassSE):
        self.class1 = class1
        self.class2 = class2
        self.color = (0, 0, 0)
        self.clicked = False
        self.rect = pygame.Rect(self.class1.x, self.class1.y, self.class2.x, self.class2.y)

    def draw(self, win):
        pygame.draw.line(win, self.color, (self.class1.x, self.class1.y), (self.class2.x, self.class2.y), 1)

    def __str__(self) -> str:
        return f"({self.class1.number}, {self.class2.number})"
    
    def __repr__(self) -> str:
        return f"({self.class1.number}, {self.class2.number})"

class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.selected = None
        self.classes = []
        self.modules = []
        self.attributes = []

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not pygame.key.get_pressed()[pygame.K_LSHIFT] and not pygame.key.get_pressed()[pygame.K_LALT]:
                    for class1 in self.classes:
                        class1.click(event.pos)
                    for module in self.modules:
                        module.click(event.pos)
                # if button 1 and shift is pressed, create a new class
                if event.button == 1 and pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    for module in self.modules:
                        if module.rect.collidepoint(event.pos):
                            self.classes.append(ClassSE(event.pos[0], event.pos[1], 30, (0, 0, 0)))
                            module.classes.append(self.classes[-1])
                            self.classes[-1].number = len(self.classes) - 1
                # if button 1 and ctrl is pressed, create a new module
                if event.button == 1 and pygame.key.get_pressed()[pygame.K_LCTRL]:
                    self.modules.append(ModuleSE(event.pos[0], event.pos[1], 200, 250, (0, 0, 255)))
                # if button 1 and alt is pressed, create a new attribute
                if event.button == 1 and pygame.key.get_pressed()[pygame.K_LALT]:
                    for class1 in self.classes:
                        if class1.color == (255, 0, 0):
                            for class2 in self.classes:
                                if class2.color == (255, 0, 0):
                                    self.attributes.append(AttributeSE(class1, class2))
                                    class1.color = (0, 0, 0)
                                    class2.color = (0, 0, 0)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for class1 in self.classes:
                        class1.clicked = False
                    for module in self.modules:
                        module.clicked = False
                    for attribute in self.attributes:
                        attribute.clicked = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    pygame.quit()
                    quit()
                if event.key == pygame.K_RETURN:
                    modules = []
                    classes = []
                    for m in range(len(self.modules)):
                        modules.append(Module(str(m), []))
                    index = 0
                    for m in range(len(self.modules)):
                        for c in range(len(self.modules[m].classes)):
                            classes.append(Class(str(index), modules[m]))
                            modules[m].classes.append(classes[-1])
                            index += 1

                    attributes = []
                    print(self.attributes)
                    for a in range(len(self.attributes)):
                        attributes.append(Attribute('a', classes[self.attributes[a].class1.number], 
                        classes[self.attributes[a].class2.number]))

                    se = SEDomain([classes, attributes, len(modules)], [classes, [], len(modules)], heuristic="MaxCouplingCohesion", aggression=0.75)

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
                    print([classes, attributes, len(modules)])
                    path = search_engine.search(se.start_state, se.goal_state)
                    print(path)
                    # print the path
                    if path:
                        self.attributes.clear()
                        path, action = path
                        for p in path:
                            print(p)
                            self.attributes.append(AttributeSE(self.classes[classes.index(p.cell[1].class1)],
                            self.classes[classes.index(p.cell[1].class2)]))

    def update(self):
        for module in self.modules:
            module.drag(pygame.mouse.get_pos())
       
    def draw(self):
        self.win.fill((0xff, 0xff, 0xff))
        for module in self.modules:
            module.draw(self.win)
        for attribute in self.attributes:
            attribute.draw(self.win)
        pygame.display.update()