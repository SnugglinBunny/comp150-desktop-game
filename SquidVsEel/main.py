import pygame, sys
from pygame.locals import *
import player

pygame.init()

WHITE = 255, 255, 255
WIDTH = 1920
HEIGHT = 1080
BLUE = 0, 188, 255
BLUEalpha = 0, 188, 255, 0
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
wall2 = pygame.draw.rect(screen, GREY, (1550, 220, 40, 460))
wall3 = pygame.draw.rect(screen, GREY, (570, 270, 440, 40))
wall4 = pygame.draw.rect(screen, GREY, (910, 590, 440, 40))


#squid.rect = pygame.draw.rect(screen, BLUE, (squid.x, squid.y, squid.width, squid.height))


while True:
    squid.rect = pygame.draw.rect(screen, BLUE, (squid.x, squid.y, squid.width, squid.height))
    eel.rect = pygame.draw.rect(screen, BLUE, (eel.x, eel.y, eel.width, eel.height))
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

    # squid wall collisions
    if pygame.Rect.colliderect(wall1, squid.rect) or pygame.Rect.colliderect(wall2, squid.rect) or pygame.Rect.colliderect(wall3, squid.rect) or pygame.Rect.colliderect(wall4, squid.rect):
        squid.speed = 2
    else:
        squid.speed = 5

    # eel wall collisions
    if pygame.Rect.colliderect(wall1, eel.rect) or pygame.Rect.colliderect(wall2, eel.rect) or pygame.Rect.colliderect(wall3, eel.rect) or pygame.Rect.colliderect(wall4, eel.rect):
        eel.speed = 2
    else:
        eel.speed = 5

    if pressed[K_UP] and squid.y > 40:
        squid.y -= squid.speed
    elif pressed[K_DOWN] and squid.y < playZoneHeight - squid.height + 40:
        squid.y += squid.speed
    if pressed[K_RIGHT] and squid.x < playZoneWidth - squid.width + 40:
        squid.x += squid.speed
        squid.render(screen)
    elif pressed[K_LEFT] and squid.x > 40:
        squid.x -= squid.speed
        flippedImage = pygame.transform.flip(squid.images, 1, 0)
        screen.blit(flippedImage, (squid.x, squid.y), ((squid.numImages - squid.currentImage) * squid.width, 0, squid.width, squid.height))
    else:
        squid.currentImage = 0
        squid.render(screen)

    if pressed[K_w] and eel.y > 40:
        eel.y -= eel.speed
    elif pressed[K_s] and eel.y < playZoneHeight - eel.height + 40:
        eel.y += eel.speed
    if pressed[K_d] and eel.x < playZoneWidth - eel.width + 40:
        eel.x += eel.speed
        eel.render(screen)
    elif pressed[K_a] and eel.x > 40:
        eel.x -= eel.speed
        flippedImage = pygame.transform.flip(eel.images, 1, 0)
        screen.blit(flippedImage, (eel.x, eel.y), ((eel.numImages - eel.currentImage) * eel.width, 0, eel.width, eel.height))
    else:
        eel.currentImage = 0
        eel.render(screen)


    squid.update()
    eel.update()


    pygame.draw.rect(screen, GREY, wall1)
    pygame.draw.rect(screen, GREY, wall2)
    pygame.draw.rect(screen, GREY, wall3)
    pygame.draw.rect(screen, GREY, wall4)

    #squid.rect = pygame.draw.rect(screen, BLUE, (squid.x, squid.y, squid.width, squid.height))
    pygame.display.update(squid.rect)

    clock.tick(40)
    pygame.display.update()