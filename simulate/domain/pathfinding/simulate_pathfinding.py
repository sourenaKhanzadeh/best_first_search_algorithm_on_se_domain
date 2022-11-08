import pygame
from pygame.locals import *
from pygame.color import *
import sys

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

class Wall:
    def __init__(self, screen, x, y, cell_size=20):
        self.screen = screen
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.width = self.cell_size
        self.height =self.cell_size
    
    def draw(self):
        # draw the wall depending on the cell size
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x * self.cell_size, self.y * self.cell_size, self.width, self.height))
class Path:
    def __init__(self, screen, x, y, width, height, cell_size):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.trail = []
        self.temp = []
        self.node_expanded = []
        self.cell_size = cell_size
    
    def draw(self):
        for i in self.node_expanded:
            # make the node expanded depending on the cell size
            # make the node expnasion lower opacity
            rect = pygame.Surface((self.cell_size, self.cell_size))
            rect.set_alpha(50)
            rect.fill((255, 0, 0))
            self.screen.blit(rect, (i[0] * self.cell_size, i[1] * self.cell_size))
            # pygame.draw.rect(self.screen, (255, 0, 0), (i[0] * self.cell_size, i[1] * self.cell_size, self.width, self.height))
        for i in self.trail:
            pygame.draw.rect(self.screen, (0, 0, 255), (i[0], i[1], self.width, self.height))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, self.width, self.height))
        
    def animate(self):
        if self.trail:
            self.trail.pop(0)
        else:
            self.trail = self.temp[:]

    def policy(self, action):
        self.trail.append((self.x, self.y))
        self.temp = self.trail[:]
        if action.name == 'up':
            self.y -= self.height
        elif action.name == 'down':
            self.y += self.height
        elif action.name == 'left':
            self.x -= self.width
        elif action.name == 'right':
            self.x += self.width

    def visited(self, x, y):
        self.node_expanded.append((x, y))

class GridSM:
    def __init__(self, settings, screen, walls, cell_size=20, start=None, goal=None):
        self.settings = settings
        self.screen = screen
        self.cell_size = cell_size
        self.grid_width = self.settings.screen_width // self.cell_size
        self.grid_height = self.settings.screen_height // self.cell_size
        self.grid = []
        self.start = start
        self.goal = goal
        self.walls = walls
        self.start_set = False if start == None else True
        self.goal_set = False if goal == None else True
        self.path = Path(self.screen, self.start[0] * self.cell_size, self.start[1] * self.cell_size, self.cell_size, self.cell_size, self.cell_size)
        self.make_grid()
    
    def make_grid(self):
        for i in range(self.grid_width):
            self.grid.append([])
            for j in range(self.grid_height):
                self.grid[i].append(0)
    
    def draw_grid(self):
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                pygame.draw.rect(self.screen, (0, 0, 0), (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size), 1)
    
    def draw_start(self):
        if self.start:
            pygame.draw.rect(self.screen, (0, 255, 0), (self.start[0] * self.cell_size, self.start[1] * self.cell_size, self.cell_size, self.cell_size))
    
    def draw_goal(self):
        if self.goal:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.goal[0] * self.cell_size, self.goal[1] * self.cell_size, self.cell_size, self.cell_size))
    
    def draw_wall(self):
        for wall in self.walls:
            wall.draw()

    def draw(self):
        self.draw_grid()
        self.draw_start()
        self.draw_goal()
        self.draw_wall()
    
    def get_cell(self, x, y):
        return self.grid[x][y]
    
    def set_cell(self, x, y, value):
        self.grid[x][y] = value
    
    def set_start(self, x, y):
        if self.start_set:
            self.grid[self.start[0]][self.start[1]] = 0
        self.start = (x, y)
        self.start_set = True
        self.grid[x][y] = 1
    
    def set_goal(self, x, y):
        if self.goal_set:
            self.grid[self.goal[0]][self.goal[1]] = 0
        self.goal = (x, y)
        self.goal_set = True
        self.grid[x][y] = 2
    
    def get_start(self):
        return self.start

    def update(self):
        self.draw()
        self.path.draw()
        self.path.animate()

class Simulate:
    def __init__(self, settings):
        self.settings = settings
        self.screen = pygame.display.set_mode(self.settings.get_screen_size())
        self.clock = pygame.time.Clock()
        self.font = self.settings.get_font()
        self.font_color = self.settings.get_font_color()

        self.scene = []


    def awake(self, gameObj):
        self.scene.append(gameObj)

    def run(self):
        while True:
            self.clock.tick(self.settings.get_fps())
            self.screen.fill(self.settings.get_bg_color())
            self.handle_events()
            pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        for gameObj in self.scene:
            gameObj.update()
    
    def __getitem__(self, index):
        return self.scene[index]
