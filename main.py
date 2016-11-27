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
chargeCooldown = 0
ink = False
inkCooldown = 0
punchCooldown = 0
electrifyCooldown = 0
punch = False
eelWins = False
squidWins = False
eelWinCount = 0
squidWinCount = 0
electrify = False

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN, 0)
except:
    WIDTH = 1366
    HEIGHT = 768
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, 0)

playZoneWidth = WIDTH - 80
playZoneHeight = HEIGHT - 180
playZone = pygame.draw.rect(screen, BLUE, (40, 40, playZoneWidth, playZoneHeight))
squid = player.Player((playZoneWidth - (426/3) + 80), (playZoneHeight - (455/3) + 80), 426, 455,"Images/SquidWalk.png", "Images/EelWalkUp.png")
eel = player.Player(40, 40, 426, 455,"Images/EelWalk.png", "Images/EelWalkUpSmall.png")

wall1 = pygame.draw.rect(screen, GREY, (330, 220, 40, 460))
wall2 = pygame.draw.rect(screen, GREY, (1550, 220, 40, 460))
wall3 = pygame.draw.rect(screen, GREY, (570, 270, 440, 40))
wall4 = pygame.draw.rect(screen, GREY, (910, 590, 440, 40))

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

    if pressed[K_e]:
        electrify = True
    else:
        electrify = False

    if pressed[K_KP0] and punchCooldown == 0:
        punch = True

    if pressed[K_RCTRL] and inkCooldown == 0:
        ink_x = squid.x + squid.width / 2
        ink_y = squid.y + squid.height
        ink = True

    # squid wall collisions
    if pygame.Rect.colliderect(wall1, squid.rect) or pygame.Rect.colliderect(wall2, squid.rect) or pygame.Rect.colliderect(wall3, squid.rect) or pygame.Rect.colliderect(wall4, squid.rect):
        squid.speed = 2
    else:
        squid.speed = 5

    if electrify == True:
        if pygame.Rect.colliderect(squid.rect, eel.rect):
            squid.health -= 0.2

    if punch == True:
        punchCooldown = 100
        if pygame.Rect.colliderect(squid.rect, eel.rect):
            eel.health -= 20
            eel.checkHealth()
            punch = False
        else:
            punch = False
            squid.punchCounter = 0

    if ink == True:
        inkCooldown = 100
        if squid.inkCounter < 40:
            squid.inkCounter += 1
            squidInk = pygame.draw.circle(screen, BLACK, (ink_x, ink_y), squid.height + (squid.inkCounter * 2) , squid.width + (squid.inkCounter * 2))
        else:
            ink = False
            squid.inkCounter = 0

    if charge == True:
        chargeCooldown = 100
        if eel.counter < 20:
            eel.counter += 1
            eel.speed = 15
            if pygame.Rect.colliderect(squid.rect, eel.rect):
                if chargeDamage == True:
                    squid.health -= 34
                    chargeDamage = False
                squid.checkHealth()
                # charge = False
            print 'SQUID HP: ', squid.health
        else:
            charge = False
            chargeDamage = True
            eel.counter = 0

    if squid.health <= 0:
        eelWins = True
    if eelWins == True:
        message_display('squid got rekt, press enter to restart', (WIDTH/2), (HEIGHT/2 - 100))
        if pressed[K_RETURN]:
            squid.x = (playZoneWidth - (426/3) + 80)
            squid.y = (playZoneHeight - (455/3) + 80)
            eel.x = 40
            eel.y = 40
            squid.health = 100
            eel.health = 100
            message_display(' ', (WIDTH / 2), (HEIGHT / 2 - 100))
            eelWins = False




    if eel.health <= 0:
        squidWins = True
    if squidWins == True:
        eel_rect_text = "eel got rekt, press enter to restart"
        message_display(eel_rect_text, (WIDTH/2), (HEIGHT/2 - 100))
        if pressed[K_RETURN]:
            squid.x = (playZoneWidth - (426/3) + 80)
            squid.y = (playZoneHeight - (455/3) + 80)
            eel.x = 40
            eel.y = 40
            eel.health = 100
            squid.health = 100
            squidWins = False





    if chargeCooldown > 0:
        chargeCooldown -= 1

    if inkCooldown > 0:
        inkCooldown -= 0.5

    if punchCooldown > 0:
        punchCooldown -= 2


    message_display('Squid HP: ' + str(squid.health), (200),(HEIGHT - 100))
    message_display('Eel HP: ' + str(eel.health), (550), (HEIGHT - 100))

    if inkCooldown == 0:
        message_display('Ink: Ready', (WIDTH - 250), (HEIGHT - 100))
    else:
        message_display('Ink Timer: ' + str(int(99.5 - inkCooldown)) + '%', (WIDTH - 250), (HEIGHT - 100))

    if chargeCooldown == 0:
        message_display('Charge: Ready', (WIDTH - 800), (HEIGHT - 100))
    else:
        message_display('Charge Timer: ' + str(int(99.5 - chargeCooldown)) + '%', (WIDTH - 800), (HEIGHT - 100))

    # eel speed changes
    if pygame.Rect.colliderect(wall1, eel.rect) or pygame.Rect.colliderect(wall2, eel.rect) or pygame.Rect.colliderect(wall3, eel.rect) or pygame.Rect.colliderect(wall4, eel.rect):
        eel.speed = 4
    elif pygame.Rect.colliderect(squidInk, eel.rect) and squid.inkCounter != 0:
        eel.speed = 2
    elif pressed[K_SPACE] and chargeCooldown == 0 and not pygame.Rect.colliderect(squid.rect, eel.rect):
        charge = True
    elif charge == False:
        eel.speed = 7
    #Player Collisions
    # if pygame.Rect.colliderect(squid.rect, eel.rect):
    #     eel.speed = 2
    #     squid.speed = 2


    # squid movement
    if not squid.health <= 0 and not eel.health <= 0:
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

        # eel movement (images)
        if pressed[K_w] and eel.y > 40:
            eel.images = eel.imageUp
            eel.width = 40
        elif pressed[K_s] and eel.y < playZoneHeight - eel.height + 40:
            eel.images = pygame.transform.flip(eel.imageUp, 0, 1)
            eel.width = 40
        elif pressed[K_d] and eel.x < playZoneWidth - eel.width + 40:
            eel.images = eel.imageRight
            eel.width = 106
        elif pressed[K_a] and eel.x > 40:
            eel.images = pygame.transform.flip(eel.imageRight, 1, 0)
            eel.width = 106
        else:
            eel.currentImage = 0

        # eel movement (movement)
        if pressed[K_w] and eel.y > 40:
            eel.y -= eel.speed
        elif pressed[K_s] and eel.y < playZoneHeight - eel.height + 40:
            eel.y += eel.speed
        if pressed[K_d] and eel.x < playZoneWidth - eel.width + 40:
            eel.x += eel.speed
        elif pressed[K_a] and eel.x > 40:
            eel.x -= eel.speed

    eel.render(screen)
    squid.update()
    eel.update()

    pygame.draw.rect(screen, GREY, wall1)
    pygame.draw.rect(screen, GREY, wall2)
    pygame.draw.rect(screen, GREY, wall3)
    pygame.draw.rect(screen, GREY, wall4)

    pygame.display.update(squid.rect)

    clock.tick(40)
    pygame.display.update()