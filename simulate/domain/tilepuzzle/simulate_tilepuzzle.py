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

class TileSM:
    def __init__(self, screen, name, x, y, width, height, cell_size, color=(0, 0, 0)):
        self.screen = screen
        self.x = x
        self.y = y
        self.name = name
        self.width = width
        self.height = height
        self.color = color
        self.cell_size = cell_size
        self.font = pygame.font.SysFont("Arial", 20)
        self.font_color = (0, 0, 0)
    
    def draw(self):
        # draw the TileSM depending on the cell size
        pygame.draw.rect(self.screen, self.color, (self.x * self.cell_size, self.y * self.cell_size, self.width, self.height))
        # draw the number in the TileSM
        text = self.font.render(str(self.name), True, self.font_color)
        text_rect = text.get_rect()
        text_rect.center = (self.x * self.cell_size + self.width / 2, self.y * self.cell_size + self.height / 2)
        self.screen.blit(text, text_rect)

class TileSMPuzzleSM:
    def __init__(self, screen, settings, intial_state=None):
        self.screen = screen
        self.settings = settings
        self.cell_size = 100
        self.width = 3
        self.height = 3
        self.TileSMs = []
        self.empty_TileSM = None
        self.font = pygame.font.SysFont("Arial", 20)
        self.font_color = (0, 0, 0)
        self.trail = []
    
    def init_TileSMs(self, intial_state=None):
        # initialize the TileSMs
        if intial_state is None:
            intial_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for i in range(self.width):
            for j in range(self.height):
                if intial_state[i + j * self.width] == 0:
                    self.empty_TileSM = TileSM(self.screen, 0, i, j, self.cell_size, self.cell_size, self.cell_size, (0, 0, 0))
                else:
                    self.TileSMs.append(TileSM(self.screen, intial_state[i + j * self.width],i, j, self.cell_size, self.cell_size, self.cell_size, (0xff, 0xff, 0xff)))
    
    def check_goal_state(self, goal_state):
        # check if the current state is the goal state
        for TileSM in self.TileSMs:
            if TileSM.name != goal_state[TileSM.x + TileSM.y * self.width]:
                return False
        return True

    def draw(self):
        # draw the TileSMs
        for TileSM in self.TileSMs:
            TileSM.draw()
        self.empty_TileSM.draw()
    
    def getActions(self, action):
        self.trail.append(action)

    def policy(self, action):
        # move the empty TileSM
        if action == "up":
            for TileSM in self.TileSMs:
                if self.empty_TileSM.x == TileSM.x and self.empty_TileSM.y - 1 == TileSM.y:
                    self.swap(self.empty_TileSM, TileSM)
                    break
        elif action == "down":
            for TileSM in self.TileSMs:
                if self.empty_TileSM.x == TileSM.x and self.empty_TileSM.y + 1 == TileSM.y:
                    self.swap(self.empty_TileSM, TileSM)
                    break
        elif action == "left":
            for TileSM in self.TileSMs:
                if self.empty_TileSM.x - 1 == TileSM.x and self.empty_TileSM.y == TileSM.y:
                    self.swap(self.empty_TileSM, TileSM)
                    break
        elif action == "right":
            for TileSM in self.TileSMs:
                if self.empty_TileSM.x + 1 == TileSM.x and self.empty_TileSM.y == TileSM.y:
                    self.swap(self.empty_TileSM, TileSM)
                    break

    def swap(self, TileSM1, TileSM2):
        # swap the position of two TileSMs
        temp = TileSM1.x
        TileSM1.x = TileSM2.x
        TileSM2.x = temp
        temp = TileSM1.y
        TileSM1.y = TileSM2.y
        TileSM2.y = temp

class Game:
    def __init__(self, settings):
        self.settings = settings
        self.screen = pygame.display.set_mode(self.settings.get_screen_size())
        self.TileSM_puzzle = TileSMPuzzleSM(self.screen, self.settings)
        self.clock = pygame.time.Clock()
    
    def run(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(self.settings.get_fps())
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.TileSM_puzzle.policy("up")
                elif event.key == K_DOWN:
                    self.TileSM_puzzle.policy("down")
                elif event.key == K_LEFT:
                    self.TileSM_puzzle.policy("left")
                elif event.key == K_RIGHT:
                    self.TileSM_puzzle.policy("right")
                elif event.key == K_SPACE:
                    for trail in self.TileSM_puzzle.trail:
                        if not self.TileSM_puzzle.check_goal_state([0, 1, 2, 3, 4, 5, 6, 7, 8]):
                            self.TileSM_puzzle.policy(trail)
                        self.TileSM_puzzle.trail.pop(0)
                        break
    
    def _update_screen(self):
        self.screen.fill(self.settings.get_bg_color())
        self.TileSM_puzzle.draw()
        pygame.display.flip()