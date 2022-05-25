import numpy as np
import pygame, sys
from pygame.locals import *
from life import GAME
from colors import *

pygame.init()

# globals
FPS = 10
SIDE = 20 # length of cell side including border
WIDE = 4  # width of cell border
DIMS = (1200, 750)

FramePerSec = pygame.time.Clock()
surface = pygame.display.set_mode(DIMS, pygame.RESIZABLE)

pygame.display.set_caption("Game of Life")

class Cells(GAME):
    def __init__(self, surface, dims):
        super().__init__()
        self.surface = surface
        self.side, self.wide = dims
        self.color = [WHITE,RANDOM]
        self.simulate = False

    def draw(self, pos, fpos, colorBit):
        self.liveCells[pos]=False
        self.liveCells.pop(pos)
        if colorBit:
            self.liveCells[pos]=True
        pygame.draw.rect(self.surface, self.color[colorBit], (fpos + self.wide, (self.side - self.wide,) * 2))

    def msky(self):
        click = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if not self.simulate and (click[0] or click[2]):
            pos = np.array(pygame.mouse.get_pos())
            pos //= self.side
            self.draw(tuple(pos), pos * self.side, (not click[2]) | click[0])
        if keys[pygame.K_LSHIFT]:
            if   keys[pygame.K_a]: self.simulate = True
            elif keys[pygame.K_s]: self.simulate = False

    def next_day(self):
        then = set(self.liveCells)
        self.next_epoch()
        now = set(self.liveCells)

        for cell in then - now:
            self.draw(cell, np.array(cell) * self.side, 0)
        for cell in now - then:
            self.draw(cell, np.array(cell) * self.side, 1)

# class Button:
#     def __init__(self) -> None:
#         pass

def grid(surface, world, dims):
    surface.fill(WHITE)
    x,y = surface.get_size()
    side, wide = dims
    for i in range(0, y, side): # horizontal lines
        pygame.draw.line(surface, BLACK, (0,i),(x,i), width = wide)
    for i in range(0, x, side): # vertical lines
        pygame.draw.line(surface, BLACK, (i,0),(i,y), width = wide)
    for cell in world.liveCells.copy():
        world.draw(cell, np.array(cell) * SIDE, 1)

world = Cells(surface, (SIDE, WIDE))
grid(surface, world, (SIDE, WIDE))

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print(world.liveCells)
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            simState, world.simulate = world.simulate, False
            grid(surface, world, (SIDE, WIDE))
            world.simulate = simState
            del simState

    if world.simulate: world.next_day()
    world.msky()
    FramePerSec.tick(FPS)

# the map function should draw the entire map again and again
# and according to the window width and height

# make Button class for multiple buttons
# make a colors.py file
# add git