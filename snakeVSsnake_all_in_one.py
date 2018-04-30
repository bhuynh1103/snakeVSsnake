import pygame, sys
from pygame.locals import *
from random import randint

# Cause I need colors all the time and I am too lazy to keep on creating variables

# Creates all gray-scale colors with one argument
def gray(x):
    return x, x, x


red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (127, 0, 255)
pink = (255, 0, 255)
black = gray(0)
white = gray(255)


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
        self.highscore = 0

    def update(self, width, height, scale):
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
    def draw(self, window, scale):
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
    def death(self, window, width, height, scale, othertail):
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


# Game runner
pygame.init()
pygame.font.init()

# Creates screen
width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake VS Snake")

# Scale controls the size of all components of the game except the window size
# Scale should be divisible by screen width and screen height
scale = 50
winScore = 25

# Instantiates snake and food
player1 = Snake(scale, scale, red)
player2 = Snake(width - scale * 2, height - scale * 2, blue)

food1 = Food(width, height, scale)
food2 = Food(width, height, scale)

# Changes player 2's direction so that it doesn't run into border on start
player2.dir(-1, 0)


# Based on what input is given, changes direction
def keyPressed(up, left, down, right, player):
    if event.type == KEYDOWN and event.key == up:
        player.dir(0, -1)
    elif event.type == KEYDOWN and event.key == left:
        player.dir(-1, 0)
    elif event.type == KEYDOWN and event.key == down:
        player.dir(0, 1)
    elif event.type == KEYDOWN and event.key == right:
        player.dir(1, 0)

    # DEBUG
    elif event.type == KEYDOWN and event.key == K_SPACE:
        player.addTotal()


def writeText(window, written, cenX, cenY, color, size):
    font = pygame.font.Font(None, size)
    text = font.render(written, 1, color)
    textpos = text.get_rect()
    textpos.centerx = cenX
    textpos.centery = cenY
    window.blit(text, textpos)
    return (textpos)


def eaten(player, otherPlayer, food):
    if player.eat(food.x, food.y):
        food.newXY(width, height, scale)
        food.check(player.tail, otherPlayer.tail, width, height, scale)
        player.total += 2
        player.score += 1


# Loop control variables
pause = False
GameOver = False

while not GameOver:
    # Game loop
    while not pause:
        # Controls FPS
        pygame.time.wait(100)

        # Draws background and border
        screen.fill(black)
        pygame.draw.rect(screen, gray(51), (0, 0, width, height), (scale * 2) - 1)

        player1.death(screen, width, height, scale, player2.tail)
        player1.update(width, height, scale)

        player2.death(screen, width, height, scale, player1.tail)
        player2.update(width, height, scale)

        # Draws snake and food
        player1.draw(screen, scale)
        player2.draw(screen, scale)
        food1.draw(screen, scale)
        food2.draw(screen, scale)

        # DEBUG
        # print(snake.tail, snake.total)

        # If snake is at same position as food, then it is 'eaten'
        eaten(player1, player2, food1)
        eaten(player1, player2, food2)
        eaten(player2, player1, food1)
        eaten(player2, player1, food2)

        # Displays scores
        writeText(screen, str(player1.score), width * (1 / 3), scale // 2, player1.color, int(scale * .66))
        writeText(screen, str(player2.score), width * (2 / 3), scale // 2, player2.color, int(scale * .66))

        # Updates screen
        pygame.display.update()

        # Quit loop and keyPressed checker
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            keyPressed(K_w, K_a, K_s, K_d, player1)
            keyPressed(K_UP, K_LEFT, K_DOWN, K_RIGHT, player2)

            # Checks if "P" is pressed, if so it pauses game
            if event.type == KEYDOWN and event.key == K_p:
                pause = True

        # Checks if someone has reached target score
        if player1.score == winScore or player2.score == winScore:
            GameOver = True
            break

    # Pause loop
    screen.fill(black)
    pygame.draw.rect(screen, yellow, (0, 0, width, height), (scale * 2) - 1)

    player1.draw(screen, scale)
    player2.draw(screen, scale)
    food1.draw(screen, scale)
    food2.draw(screen, scale)

    writeText(screen, str(player1.score), width * (1 / 3), scale // 2, player1.color, int(scale * .66))
    writeText(screen, str(player2.score), width * (2 / 3), scale // 2, player2.color, int(scale * .66))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_p:
            pause = False
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

# Game over loop
while True:
    # DEBUG
    # print("Game Over)
    screen.fill(black)
    pygame.draw.rect(screen, white, (0, 0, width, height), (scale * 2) - 1)

    player1.draw(screen, scale)
    player2.draw(screen, scale)
    food1.draw(screen, scale)
    food2.draw(screen, scale)

    writeText(screen, str(player1.score), width * (1 / 3), scale // 2, player1.color, int(scale * .66))
    writeText(screen, str(player2.score), width * (2 / 3), scale // 2, player2.color, int(scale * .66))

    if player1.score == winScore:
        writeText(screen, "Red Won!", width // 2, height // 2, white, 75)
    else:
        writeText(screen, "Blue Won!", width // 2, height // 2, white, 75)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
