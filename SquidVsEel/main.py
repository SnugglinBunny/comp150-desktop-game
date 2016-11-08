import pygame, sys
from pygame.locals import *
import player

pygame.init()

WHITE = 255, 255, 255
WIDTH = 1920
HEIGHT = 1080
#gravity = 0
clock = pygame.time.Clock()

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN, 0)
except:
    screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN, 0)

squid = player.Player(400, 0, 426, 455,"Images/SquidWalk.png")
eel = player.Player(400, 0, 426, 455,"Images/SquidWalk.png")

movex, movey = 0, 0

while True:

    pressed = pygame.key.get_pressed()
    screen.fill((WHITE))
    clock.tick(40)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if pressed[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    if pressed[K_UP] and squid.y > 0:
        squid.y -= 10
    elif pressed[K_DOWN] and squid.y < HEIGHT:
        squid.y += 10
    if pressed[K_RIGHT] and squid.x < WIDTH:
        squid.x += 10
        squid.render(screen)
    elif pressed[K_LEFT] and squid.x > 0:
        squid.x += -10
        flippedImage = pygame.transform.flip(squid.images, 1, 0)
        screen.blit(flippedImage, (squid.x, squid.y), ((squid.numImages - squid.currentImage) * squid.width, 0, squid.width, squid.height))
    else:
        squid.currentImage = 0
        squid.render(screen)

    if pressed[K_w] and eel.y > 0:
        eel.y -= 10
    elif pressed[K_s] and eel.y < HEIGHT:
        eel.y += 10
    if pressed[K_d] and eel.x < WIDTH:
        eel.x += 10
        eel.render(screen)
    elif pressed[K_a] and eel.x > 0:
        eel.x += -10
        flippedImage = pygame.transform.flip(eel.images, 1, 0)
        screen.blit(flippedImage, (eel.x, eel.y), ((eel.numImages - eel.currentImage) * eel.width, 0, eel.width, eel.height))
    else:
        eel.currentImage = 0
        eel.render(screen)

    squid.x += movex
    eel.x += movex

    squid.update()
    eel.update()

    pygame.display.update()