import pygame
import sys
from pygame.locals import *
from pygame.color import *

pygame.init()

class Settings:
    def __init__(self, fps=60):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (255, 255, 255)
        self.fps = fps
        self.font = pygame.font.SysFont("Arial", 20)
        self.font_color = (0, 0, 0)
    
    def get_screen_size(self):
        return (self.screen_width, self.screen_height)
    
    def get_bg_color(self):
        return self.bg_color
    
    def get_fps(self):
        return self.fps
    
    def get_font(self):
        return self.font

    def get_font_color(self):
        return self.font_color

class NodeSM:
    def __init__(self, screen, text:str, x, y, cell_size=20):
        self.screen = screen
        self.x = x
        self.y = y
        self.text = text
        self.cell_size = cell_size
        self.width = self.cell_size
        self.height =self.cell_size
        self.color = (255, 0, 0)
    
    def draw(self):
        # draw the node as a circle depending on the cell size
        pygame.draw.circle(self.screen, self.color, (self.x * self.cell_size + self.cell_size // 2, self.y * self.cell_size + self.cell_size // 2), self.cell_size // 2, 1)
        # draw the text
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (self.x * self.cell_size + self.cell_size // 2, self.y * self.cell_size + self.cell_size // 2)
        self.screen.blit(text, text_rect)

class EdgeSM:
    def __init__(self, screen, node1, node2, val, cell_size=20):
        self.screen = screen
        self.node1 = node1
        self.node2 = node2
        self.cell_size = cell_size
        self.val = val
    
    def draw(self):
        # draw the edge as a line depending on the cell size
        if self.val == 0:
            pygame.draw.line(self.screen, (0 ,0, 0), (self.node1.x * self.cell_size + self.cell_size // 2, self.node1.y * self.cell_size + self.cell_size // 2), (self.node2.x * self.cell_size + self.cell_size // 2, self.node2.y * self.cell_size + self.cell_size // 2), 1)
        else:
            pygame.draw.line(self.screen, (255, 0, 0) , (self.node1.x * self.cell_size + self.cell_size // 2, self.node1.y * self.cell_size + self.cell_size // 2), (self.node2.x * self.cell_size + self.cell_size // 2, self.node2.y * self.cell_size + self.cell_size // 2), 3)



class GraphSM:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.nodes = []
        self.edges = []
        self.trail = []
        self.temp = []
        self.cell_size = 20
        self.width = self.settings.get_screen_size()[0] // self.cell_size
        self.height = self.settings.get_screen_size()[1] // self.cell_size
    
    def draw(self):
        for node in self.nodes:
            node.draw()
        for edge in self.edges:
            edge.draw()

    def add_node(self, text, x, y):
        self.nodes.append(NodeSM(self.screen, text, x, y, self.cell_size))
    
    def add_edge(self, node1, node2, val=0):
        self.edges.append(EdgeSM(self.screen, node1, node2, val, self.cell_size))
    
    def policy(self, action, node2):
        self.trail.append(node2)
        if action == "traverse_edge":
            self.traverse(node2)

    def traverse(self, node2):
        for edge in self.edges:
            if node2.parent is None:
                if edge.node1 == node2:
                    break
            else:
                if edge.node1 == node2.parent and edge.node2 == node2:
                    edge.val = 0

class Game:
    def __init__(self, settings):
        self.settings = settings
        self.screen = pygame.display.set_mode(self.settings.get_screen_size())
        self.clock = pygame.time.Clock()
        self.graph = GraphSM(self.screen, self.settings)
    
    def run(self):
        while True:
            self.clock.tick(self.settings.get_fps())
            self._check_events()
            self._update_screen()
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = x // self.graph.cell_size
                y = y // self.graph.cell_size
                if event.button == 1:
                    self.graph.add_node(f"{x}, {y}", x, y)
                elif event.button == 3:
                    for node in self.graph.nodes:
                        if node.x == x and node.y == y:
                            self.graph.add_edge(self.graph.nodes[-1], node)
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    for node in self.graph.trail:
                        for edge in self.graph.edges:
                            if node.parent is None:
                                break
                            if edge.node1 == node.parent and edge.node2 == node:
                                edge.val = 1
                                self.graph.trail.pop(0)
                                break
    def _update_screen(self):
        self.screen.fill(self.settings.get_bg_color())
        self.graph.draw()
        pygame.display.flip()
        