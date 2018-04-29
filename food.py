import pygame
from rgb import *
from random import randint


class Food:
    # Food given random location on initiation
    def __init__(self, width, height, scale):
        self.x = scale * (randint(1, (width // scale) - 2))
        self.y = scale * (randint(1, (height // scale) - 2))
        if self.x == scale and self.y == scale:
            self.newXY(width, height, scale)
            # DEBUG
            # print("fixed")

    # Food given random location on call
    def newXY(self, width, height, scale):
        self.x = scale * (randint(1, (width // scale) - 2))
        self.y = scale * (randint(1, (height // scale) - 2))

    # Prevents food from spawning on snake
    def check(self, tail, otherTail, width, height, scale):
        i = 0
        while i < len(tail):
            if self.x == tail[i][0] and self.y == tail[i][1]:
                self.newXY(width, height, scale)
                # DEBUG
                # print("fixed")
            i += 1
            
        i = 0
        while i < len(otherTail):
            if self.x == otherTail[i][0] and self.y == otherTail[i][1]:
                self.newXY(width, height, scale)
            i += 1        

    # Draws food
    def draw(self, window, scale):
        pygame.draw.rect(window, green, (self.x, self.y, scale, scale))
