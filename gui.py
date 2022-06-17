import sys

import numpy as np
import pygame
from pygame.locals import *

from colors import *
from life import GAME

pygame.init()

# globals
FPS = 10
SIDE = 20 # length of cell side including border

FramePerSec = pygame.time.Clock()
FONT = pygame.font.SysFont('inkfree',20, bold=True)
surface = pygame.display.set_mode((1200, 750), pygame.RESIZABLE)

pygame.display.set_caption("Game of Life")

class Cells(GAME):
    def __init__(self, surface, side):
        super().__init__()
        self.surface = surface
        self.side = side
        self.simulate = False
        self.color = [RANDOM(),RANDOM()]

    def draw(self, pos, fpos, colorBit):
        self.liveCells[pos]=False
        self.liveCells.pop(pos)
        if colorBit:
            self.liveCells[pos]=True
        pygame.draw.rect(self.surface, self.color[colorBit], (fpos + 2, (self.side - 2,) * 2))

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
def text(surface, world, font, side):
    global delta
    x = surface.get_width()
    x,y = ((x * 0.75) // side) * side, side * 3
    text1 = font.render(f'  Live Cells : {world.cellCount}  ',True,CYAN, BLACK)
    #text1.set_alpha(25)
    text2 = font.render(f'  Epochs     : {world.epochs}  ',True,CYAN, BLACK)
    #text2.set_alpha(25)

    surface.blit(text1, (x, y))
    surface.blit(text2,(x, y + text1.get_height()))

def grid(surface, world, side):
    surface.fill(RANDOM())
    x,y = surface.get_size()
    for i in range(0, y, side): # horizontal lines
        pygame.draw.line(surface, BLACK, (0,i),(x,i), width = 2)
    for i in range(0, x, side): # vertical lines
        pygame.draw.line(surface, BLACK, (i,0),(i,y), width = 2)
    for cell in world.liveCells.copy():
        world.draw(cell, np.array(cell) * SIDE, 1)

world = Cells(surface, SIDE)
grid(surface, world, SIDE)

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print(world.cellCount)
            print(world.epochs)
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            simState, world.simulate = world.simulate, False
            grid(surface, world, SIDE)
            world.simulate = simState
            del simState

    if world.simulate: world.next_day()
    world.msky()
    text(surface, world, FONT, SIDE)
    FramePerSec.tick(FPS)



# make Button class for multiple buttons
# make a colors.py file
# add git

# make map movable/ zoomable
# display stats and buttons
# scalable cells, size should be increased and decreased

# downloadable csv of current state
# random cell state generator
# erase all cells currenly in canvas