import pygame, sys
from snake import *
from food import *
from pygame.locals import *
from rgb import *

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
