from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
def RANDOM():
    return tuple([randint(0,255) for i in range(3)])