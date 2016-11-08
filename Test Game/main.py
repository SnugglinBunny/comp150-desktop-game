import pygame, sys, random, time
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

WIDTH = 1920
HEIGHT = 1080
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LBLUE = (0, 170, 255)
BLUE = (0, 188, 255)
key = pygame.key.get_pressed()
speed = 5
playerOneSize = (40, 40)
playerTwoSize = (40, 40)

try:
    window = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN, 0)
    gameWindow = pygame.draw.rect(window, BLUE, (10, 10, 1900, 900))
except:
    window = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN, 0)
    gameWindow = pygame.draw.rect(window, BLUE, (10, 10, 1346, 748))

pygame.display.set_caption('Squid VS Eel')
mainloop = True
playerOne = pygame.draw.rect(window, RED, (10, 10, 40, 40))
playerTwo = pygame.draw.rect(window, BLACK, (10, 10, 40, 40))

while mainloop == True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        playerOne.move_ip(0, -speed)
    if key[pygame.K_a]:
        playerOne.move_ip(-speed, 0)
    if key [pygame.K_s]:
        playerOne.move_ip(0, speed)
    if key[pygame.K_d]:
        playerOne.move_ip(speed, 0)
    if key[pygame.K_LSHIFT]:
        playerOneSize = 50,50


    if key [pygame.K_DOWN]:
        playerTwo.move_ip(0, speed)
    if key[pygame.K_UP]:
        playerTwo.move_ip(0, -speed)
    if key[pygame.K_RIGHT]:
        playerTwo.move_ip(speed, 0)
    if key[pygame.K_LEFT]:
        playerTwo.move_ip(-speed, 0)


    window.fill(LBLUE)
    pygame.draw.rect(window, BLUE, gameWindow)
    pygame.draw.rect(window, WHITE, playerOne)
    playerOne.clamp_ip(gameWindow)
    pygame.draw.rect(window, BLACK, playerTwo)
    playerTwo.clamp_ip(gameWindow)
    pygame.display.update()
    clock.tick(120)

