import pygame, sys
from pygame.locals import *
import player

pygame.init()

WHITE = 255, 255, 255
WIDTH = 1920
HEIGHT = 1080
BLUE = 0, 188, 255
LBLUE = 0, 100, 200
BLACK = 0, 0, 0
GREY = 32, 78, 81
clock = pygame.time.Clock()
charge = False
chargeTimer = 0
ink = False
inkCooldown = 0

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN, 0)
except:
    WIDTH = 1366
    HEIGHT = 768
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, 0)

playZoneWidth = WIDTH - 80
playZoneHeight = HEIGHT - 180
playZone = pygame.draw.rect(screen, BLUE, (40, 40, playZoneWidth, playZoneHeight))
squid = player.Player((playZoneWidth - (426/3) + 80), (playZoneHeight - (455/3) + 80), 426, 455,"Images/SquidWalk.png")
eel = player.Player(40, 40, 426, 455,"Images/EelWalk.png")

wallDims = [(330, 220, 40, 460), (1550, 220, 40, 460), (570, 270, 440, 40), (910, 590, 440, 40)]
walls = []

for wall in wallDims:
    walls.append(pygame.draw.rect(screen, GREY, wall))

ink_x = 10000
ink_y = 10000
squidInk = pygame.draw.circle(screen, BLACK, (ink_x, ink_y), squid.height * 2, squid.width * 2)


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def message_display(text, x, y):
    largeText = pygame.font.Font(None, 75)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)





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

    screen.fill((LBLUE))
    pygame.draw.rect(screen, BLUE, playZone)

    if pressed[K_RCTRL] and inkCooldown == 0:
        ink_x = squid.x + squid.width / 2
        ink_y = squid.y + squid.height
        ink = True

    # squid wall collisions
    if pygame.Rect.colliderect(walls[0], squid.rect) or pygame.Rect.colliderect(walls[1], squid.rect) or pygame.Rect.colliderect(walls[2], squid.rect) or pygame.Rect.colliderect(walls[3], squid.rect):
        squid.speed = 2
    else:
        squid.speed = 5

    if ink == True:
        inkCooldown = 100
        if squid.inkCounter < 40:
            squid.inkCounter += 1
            squidInk = pygame.draw.circle(screen, BLACK, (ink_x, ink_y), squid.height + (squid.inkCounter * 2) , squid.width + (squid.inkCounter * 2))
        else:
            ink = False
            squid.inkCounter = 0
    if charge == True:
        chargeTimer = 100
        if eel.counter < 20:
            eel.counter += 1
            eel.speed = 15
            if pygame.Rect.colliderect(squid.rect, eel.rect):
                squid.health -= 100
                squid.checkHealth()
                charge = False
                print 'SQUID HP: ', squid.health
        else:
            charge = False
            eel.counter = 0

    if squid.health <= 0:
        message_display('rekt, press enter to restart')
        if pressed[K_RETURN]:
            squid.x = (playZoneWidth - (426/3) + 80)
            squid.y = (playZoneHeight - (455/3) + 80)
            eel.x = 40
            eel.y = 40
            squid.health = 100


    if chargeTimer > 0:
        chargeTimer -= 1

    if inkCooldown > 0:
        inkCooldown -= 0.5

    message_display('Squid HP: ' + str(squid.health), (250),(HEIGHT - 100))

    if inkCooldown == 0:
        message_display('Ink Timer: Ready', (WIDTH - 250), (HEIGHT - 100))
    else:
        message_display('Ink Timer: ' + str(int(99.5 - inkCooldown)) + '%', (WIDTH - 250), (HEIGHT - 100))

    # eel speed changes
    if pygame.Rect.colliderect(walls[0], eel.rect) or pygame.Rect.colliderect(walls[1], eel.rect) or pygame.Rect.colliderect(walls[2], eel.rect) or pygame.Rect.colliderect(walls[3], eel.rect):
        eel.speed = 2
    elif pygame.Rect.colliderect(squidInk, eel.rect) and squid.inkCounter != 0:
        eel.speed = 2
    elif pressed[K_SPACE] and chargeTimer == 0 and not pygame.Rect.colliderect(squid.rect, eel.rect):
        charge = True
    elif charge == False:
        eel.speed = 5

    #Player Collisions
    if pygame.Rect.colliderect(squid.rect, eel.rect):
        eel.speed = 2
        squid.speed = 2

    # squid movement
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

    # eel movement
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

    for i in xrange(4):
        pygame.draw.rect(screen, GREY, walls[i])

    pygame.display.update(squid.rect)

    clock.tick(40)
    pygame.display.update()