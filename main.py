import pygame
import sys
from pygame.locals import *
import player
import winsound

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=4096)

WHITE = 255, 255, 255
WIDTH = 1920
HEIGHT = 1080
BLUE = 0, 188, 255
LBLUE = 0, 100, 200
BLACK = 0, 0, 0
GREY = 32, 78, 81
clock = pygame.time.Clock()
charge = False
charge_cooldown = 0
ink = False
ink_cooldown = 0
punch_cooldown = 0
electrify_cooldown = 0
punch = False
eel_wins = False
squid_wins = False
eel_win_count = 0
squid_win_count = 0
electrify = False
charge_damage = True
sound_played = False
eel_is_dead = False
squid_is_dead = False

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, 0)
except:
    WIDTH = 1366
    HEIGHT = 768
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, 0)

try:  # Background music is loaded here.
    background = pygame.mixer.Sound("Sounds/melody.wav")
    background.set_volume(0.02)
    background.play(loops=-1)
except pygame.error, message:
    print "Cannot load sound"

playZoneWidth = WIDTH - 80
playZoneHeight = HEIGHT - 180
playZone = pygame.draw.rect(screen, BLUE, (40, 40, playZoneWidth, playZoneHeight))
squid = player.Player((playZoneWidth - (426 / 3) + 80), (playZoneHeight - (455 / 3) + 80), 426, 455,
                      "Images/SquidWalk.png", "Images/EelWalkUp.png", "Images/EelwalkElectric.png",
                      "Images/EelWalkUpSmallElectric.png")
eel = player.Player(40, 40, 426, 455, "Images/EelWalk.png", "Images/EelWalkUpSmall.png", "Images/EelWalkElectric.png",
                    "Images/EelWalkUpSmallElectric.png")

wall1 = pygame.draw.rect(screen, GREY, (WIDTH / 5.8, WIDTH / 8.7, WIDTH / 48, WIDTH / 4.2))
wall2 = pygame.draw.rect(screen, GREY, (WIDTH / 1.23, WIDTH / 8.7, WIDTH / 48, WIDTH / 4.2))
wall3 = pygame.draw.rect(screen, GREY, (WIDTH / 3.36, WIDTH / 7.1, WIDTH / 4.36, WIDTH / 48))
wall4 = pygame.draw.rect(screen, GREY, (WIDTH / 2.1, WIDTH / 3.25, WIDTH / 4.36, WIDTH / 48))

ink_x = 10000
ink_y = 10000
squidInk = pygame.draw.circle(screen, BLACK, (ink_x, ink_y), squid.height * 2, squid.width * 2)


def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y):
    large_text = pygame.font.Font(None, 75)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)


def play_sfx(name, times_played):
    sfx = pygame.mixer.Sound('Sounds/' + name + '.wav')
    sfx.play(loops=times_played)


electric_sfx = pygame.mixer.Sound("Sounds/electric.wav")

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

    screen.fill(LBLUE)
    pygame.draw.rect(screen, BLUE, playZone)

    if pressed[K_COMMA]:
        electrify = True
        if not sound_played:
            electric_sfx.play(loops=-1)
            sound_played = True
    else:
        electric_sfx.stop()
        sound_played = False
        electrify = False

    if pressed[K_KP4]:
        foo = 1

    if pressed[K_KP0] and punch_cooldown == 0:
        punch = True
        play_sfx('woosh', 0)

    if pressed[K_KP_PERIOD] and ink_cooldown == 0:
        ink_x = squid.x + squid.width / 2
        ink_y = squid.y + squid.height
        ink = True
        play_sfx('inksound', 0)

    # Checks if player is dead
    if eel.health <= 0:
        eel_is_dead = True
    else:
        eel_is_dead = False
    if squid.health <= 0:
        squid_is_dead = True
    else:
        squid_is_dead = False

    # squid wall collisions
    if pygame.Rect.colliderect(wall1, squid.rect) or pygame.Rect.colliderect(wall2,
                                                                             squid.rect) or pygame.Rect.colliderect(
            wall3, squid.rect) or pygame.Rect.colliderect(wall4, squid.rect):
        squid.speed = 2
    else:
        squid.speed = 5

    if electrify:
        eel.health -= 0.1
        if pygame.Rect.colliderect(squid.rect, eel.rect):
            squid.health -= 0.4

    if punch:
        punch_cooldown = 100
        if pygame.Rect.colliderect(squid.rect, eel.rect):
            eel.health -= 20
            play_sfx('woosh', 0)
            play_sfx('punch', 0)
            eel.check_health()
            punch = False
        else:
            punch = False
            squid.punchCounter = 0

    if ink:
        ink_cooldown = 100
        if squid.inkCounter < 40:
            squid.inkCounter += 1
            squidInk = pygame.draw.circle(screen, BLACK, (ink_x, ink_y), squid.height + (squid.inkCounter * 2),
                                          squid.width + (squid.inkCounter * 2))
        else:
            ink = False
            squid.inkCounter = 0

    if charge:
        charge_cooldown = 100
        if eel.counter < 20:
            eel.counter += 1
            eel.speed = 15
            if pygame.Rect.colliderect(squid.rect, eel.rect):
                if charge_damage:
                    play_sfx('ChargeHit', 0)
                    squid.health -= 15
                    charge_damage = False
                squid.check_health()
        else:
            charge = False
            charge_damage = True
            eel.counter = 0

    if squid_is_dead:
        eel_wins = True
    if eel_wins:
        message_display('squid got rekt, press enter to restart', (WIDTH / 2), (HEIGHT / 2 - 100))
        if pressed[K_RETURN]:
            squid.x = (playZoneWidth - (426 / 3) + 80)
            squid.y = (playZoneHeight - (455 / 3) + 80)
            eel.x = 40
            eel.y = 40
            squid.health = 100
            eel.health = 100
            message_display(' ', (WIDTH / 2), (HEIGHT / 2 - 100))
            eel_wins = False

    if eel_is_dead:
        squid_wins = True
    if squid_wins:
        eel_rect_text = "eel got rekt, press enter to restart"
        message_display(eel_rect_text, (WIDTH / 2), (HEIGHT / 2 - 100))
        if pressed[K_RETURN]:
            squid.x = (playZoneWidth - (426 / 3) + 80)
            squid.y = (playZoneHeight - (455 / 3) + 80)
            eel.x = 40
            eel.y = 40
            eel.health = 100
            squid.health = 100
            squid_wins = False

    if charge_cooldown > 0:
        charge_cooldown -= 1

    if ink_cooldown > 0:
        ink_cooldown -= 0.5

    if punch_cooldown > 0:
        punch_cooldown -= 2.5

    if squid_is_dead:
        message_display('Squid HP: DEAD', (WIDTH - 220), (HEIGHT - 100))
    else:
        message_display('Squid HP: ' + str(squid.health), (WIDTH - 220), (HEIGHT - 100))

    if eel_is_dead:
        message_display('Eel HP: DEAD', 180, (HEIGHT - 100))
    else:
        message_display('Eel HP: ' + str(eel.health), 180, (HEIGHT - 100))

    if ink_cooldown == 0:
        message_display('Ink: Ready', (WIDTH - 550), (HEIGHT - 40))
    else:
        message_display('Ink: ' + str(int(99.5 - ink_cooldown)) + '%', (WIDTH - 550), (HEIGHT - 40))

    if charge_cooldown == 0:
        message_display('Charge: Ready', 220, (HEIGHT - 40))
    else:
        message_display('Charge: ' + str(int(99.5 - charge_cooldown)) + '%', 220, (HEIGHT - 40))

    if punch_cooldown == 0:
        message_display('Punch: Ready', (WIDTH - 220), (HEIGHT - 40))
    else:
        message_display(('Punch: ' + str(int(99.5 - punch_cooldown)) + '%'), (WIDTH - 220), (HEIGHT - 40))

    # eel speed changes
    if pygame.Rect.colliderect(wall1, eel.rect) or \
            pygame.Rect.colliderect(wall2, eel.rect) or \
            pygame.Rect.colliderect(wall3, eel.rect) or \
            pygame.Rect.colliderect(wall4, eel.rect):
        eel.speed = 3.5
    elif pygame.Rect.colliderect(squidInk, eel.rect) and squid.inkCounter != 0:
        eel.speed = 2
        eel.health -= 0.2
    elif pressed[K_SPACE] and charge_cooldown == 0:
        charge = True
    elif not charge:
        eel.speed = 7

    # squid movement
    if not squid_is_dead and not eel_is_dead:
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
            screen.blit(flippedImage, (squid.x, squid.y),
                        ((squid.numImages - squid.currentImage) * squid.width, 0, squid.width, squid.height))
        else:
            squid.currentImage = 0
            squid.render(screen)

        # eel movement (images)

        if electrify:
            eel.images = eel.imagesElectric

            if pressed[K_w] and eel.y > 40:
                eel.images = eel.imagesElectricUp
                eel.width = 40
            elif pressed[K_s] and eel.y < playZoneHeight - eel.height + 40:
                eel.images = pygame.transform.flip(eel.imagesElectricUp, 0, 1)
                eel.width = 40
            elif pressed[K_d] and eel.x < playZoneWidth - eel.width + 40:
                eel.images = eel.imagesElectric
                eel.width = 106
            elif pressed[K_a] and eel.x > 40:
                eel.images = pygame.transform.flip(eel.imagesElectric, 1, 0)
                eel.width = 106
        else:
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

    if squid_wins is not True and eel_wins is not True:
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
