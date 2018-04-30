import pygame
from random import randint
from constants import *


class Food:
    # Food given random location on initiation
    def __init__(self, color):
        self.x = scale * (randint(1, (width // scale) - 2))
        self.y = scale * (randint(1, (height // scale) - 2))
        self.color = color
        if self.x == scale and self.y == scale:
            self.newXY()
            # DEBUG
            # print("fixed")

    # Food given random location on call
    def newXY(self):
        self.x = scale * (randint(1, (width // scale) - 2))
        self.y = scale * (randint(1, (height // scale) - 2))

    # Prevents food from spawning on snake
    def check(self, tail, otherTail):
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
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, scale, scale))


class Apple(Food):
    def eaten(self, player, otherPlayer):
        if player.eat(self.x, self.y):
            self.newXY()
            self.check(player.tail, otherPlayer.tail)
            player.total += 2
            player.score += 1


class Freeze(Food):
    pass
