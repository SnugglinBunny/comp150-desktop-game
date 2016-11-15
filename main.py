import pygame, sys
from pygame.locals import *
import player

pygame.init()

WHITE = 255, 255, 255
WIDTH = 1920
HEIGHT = 1080
BLUE = 0, 188, 255
GREY = 32, 78, 81
clock = pygame.time.Clock()
squid = player.Player(40, 40, 426, 455,"Images/SquidWalk.png")
eel = player.Player(40, 40, 426, 455,"Images/EelWalk.png")

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN, 0)
except:
    WIDTH = 1366
    HEIGHT = 768
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, 0)

playZoneWidth = WIDTH - 80
playZoneHeight = HEIGHT - 180
playZone = pygame.draw.rect(screen, BLUE, (40, 40, playZoneWidth, playZoneHeight))
wall1 = pygame.draw.rect(screen, GREY, (330, 220, 40, 460))
wall2 = pygame.draw.rect(screen, GREY, (330, 220, 40, 460))
wall3 = pygame.draw.rect(screen, GREY, (330, 220, 40, 460))
wall4 = pygame.draw.rect(screen, GREY, (330, 220, 40, 460))


while True:

    pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if pressed[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    screen.fill((WHITE))
    pygame.draw.rect(screen, BLUE, playZone)

    if pressed[K_UP] and squid.y > 40:
        squid.y -= 5
    elif pressed[K_DOWN] and squid.y < playZoneHeight - squid.height + 40:
        squid.y += 5
    if pressed[K_RIGHT] and squid.x < playZoneWidth - squid.width + 40:
        squid.x += 5
        squid.render(screen)
    elif pressed[K_LEFT] and squid.x > 40:
        squid.x -= 5
        flippedImage = pygame.transform.flip(squid.images, 1, 0)
        screen.blit(flippedImage, (squid.x, squid.y), ((squid.numImages - squid.currentImage) * squid.width, 0, squid.width, squid.height))
    else:
        squid.currentImage = 0
        squid.render(screen)

    if pressed[K_w] and eel.y > 40:
        eel.y -= 5
    elif pressed[K_s] and eel.y < playZoneHeight - eel.height + 40:
        eel.y += 5
    if pressed[K_d] and eel.x < playZoneWidth - eel.width + 40:
        eel.x += 5
        eel.render(screen)
    elif pressed[K_a] and eel.x > 40:
        eel.x -= 5
        flippedImage = pygame.transform.flip(eel.images, 1, 0)
        screen.blit(flippedImage, (eel.x, eel.y), ((eel.numImages - eel.currentImage) * eel.width, 0, eel.width, eel.height))
    else:
        eel.currentImage = 0
        eel.render(screen)

    squid.update()
    eel.update()

    clock.tick(40)
    pygame.display.update()