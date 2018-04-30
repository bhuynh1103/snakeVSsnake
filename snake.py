import pygame
from constants import *


class Snake:
    def __init__(self, startX, startY, color):
        self.x = startX
        self.y = startY
        self.color = color
        self.xSpeed = 1
        self.ySpeed = 0
        self.total = 0
        self.tail = []
        self.score = 0

    def update(self):
        # Maintains list of (x, y) points of snake's tail
        while len(self.tail) != self.total:
            self.tail.append([self.x, self.y])
            del self.tail[:(len(self.tail) - self.total)]
        self.tail.append([self.x, self.y])

        # Moves snake
        self.x += self.xSpeed * scale
        self.y += self.ySpeed * scale

        # Prevents snake from exceeding screen borders
        if self.x >= width - scale:  # right edge
            self.x -= self.xSpeed * scale
        elif self.y >= height - scale:  # bottom edge
            self.y -= self.ySpeed * scale
        elif self.x <= 0:  # left edge
            self.x -= self.xSpeed * scale
        elif self.y <= 0:  # top edge
            self.y -= self.ySpeed * scale

    # Draws snake head and tail
    def draw(self, window):
        i = 0
        while i < len(self.tail):
            pygame.draw.rect(window, self.color, (self.tail[i][0], self.tail[i][1], scale, scale))
            pygame.draw.rect(window, (0, 0, 0), (self.tail[i][0], self.tail[i][1], scale, scale), 1)
            i += 1

        pygame.draw.rect(window, self.color, (self.x, self.y, scale, scale))
        pygame.draw.rect(window, (0, 0, 0), (self.x, self.y, scale, scale), 1)

    # Dictates direction of snake based on user input
    def dir(self, x, y):
        self.xSpeed = x
        self.ySpeed = y

    # If snake's position is same as food position, returns True
    def eat(self, otherX, otherY):
        if self.x == otherX and self.y == otherY:
            return True
        else:
            return False

    # Checks for various things that would end game and resets game
    def death(self, window, othertail):
        i = 0
        while i < len(self.tail):
            xPos = self.tail[i][0]
            yPos = self.tail[i][1]

            if xPos == self.x and yPos == self.y:
                self.total = 0
                self.tail = []
                self.score = 0
                # Changes border to color for short time to indicate death
                pygame.draw.rect(window, self.color, (0, 0, width, height), (scale * 2) - 1)
            i += 1

        i = 0
        while i < len(othertail):
            xPos = othertail[i][0]
            yPos = othertail[i][1]

            if xPos == self.x and yPos == self.y:
                self.total = 0
                self.tail = []
                self.score = 0
                # Changes border to color for short time to indicate death
                pygame.draw.rect(window, self.color, (0, 0, width, height), (scale * 2) - 1)
            i += 1

    # DEBUG
    def addTotal(self):
        self.total += 2
        self.score += 1
