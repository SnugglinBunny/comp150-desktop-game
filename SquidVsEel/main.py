import pygame, sys
from pygame.locals import *
import player

pygame.init()

WHITE = 255, 255, 255
w = 1920
h = 1080
gravity = 0
clock = pygame.time.Clock()

screen = pygame.display.set_mode((w, h), 0, 32)

squid = player.Player(400, 0)

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

    if pressed[K_RIGHT]:
        squid.x += 10
        squid.render(screen)
    elif pressed[K_LEFT]:
        squid.x += -10
        flippedImage = pygame.transform.flip(squid.images, 1, 0)
        screen.blit(flippedImage, (squid.x, squid.y), ((squid.numImages - squid.currentImage) * squid.width, 0, squid.width, squid.height))
    else:
        squid.currentImage = 0
        squid.render(screen)


    squid.x += movex

    squid.update()

    pygame.display.update()