import pygame
from random import randint

# init instance
pygame.init()
clock = pygame.time.Clock()
# STATS
level = 1

# TEXT
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(f"Points: " + str(level), True, 'white', 'black')
textRect = text.get_rect()
textRect.center = (80, 20)

# Display globals
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
BACKGROUND = pygame.image.load("bg.png")

# Player
DEFAULT_PLAYER_SIZE = (80, 80)
SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load("spaceship.png"), DEFAULT_PLAYER_SIZE)

# Setting Display
pygame.display.set_caption("Space Invaders")
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Player
DEFAULT_PLAYER_SIZE = (80, 80)
SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load("spaceship.png"), DEFAULT_PLAYER_SIZE)
spaceship_speed = 20
playerX = 368
playerY = 500

# Invaders
DEFAULT_INVADER_SIZE = (80, 80)
INVADER_IMAGE = pygame.transform.scale(pygame.image.load("invader.png"), DEFAULT_INVADER_SIZE)
invader_speed = 10
invader_advance = 1
invaders = [[[randint(0, DISPLAY_WIDTH), randint(0, DISPLAY_HEIGHT-DEFAULT_PLAYER_SIZE[1])], INVADER_IMAGE, 'left'], [[randint(0, DISPLAY_WIDTH), randint(0, DISPLAY_HEIGHT-DEFAULT_PLAYER_SIZE[1])], INVADER_IMAGE, 'right'], [[randint(0, DISPLAY_WIDTH), randint(0, DISPLAY_HEIGHT-DEFAULT_PLAYER_SIZE[1])], INVADER_IMAGE, 'right']]

# Missiles
DEFAULT_MISSIL_SIZE = (80, 80)
DFAULT_MISSIL_SPEED = 10
MISSIL_IMAGE = pygame.transform.scale(pygame.image.load("missil.png"), DEFAULT_MISSIL_SIZE)
missil_shot = False
missiles = []


# Statement
game_running = True
finished = False


def player_definition():
    display.blit(SPACESHIP_IMAGE, (playerX, playerY))


def move_spaceship(where):
    global playerX
    if where == 'left':
        if playerX > 0:
            playerX -= spaceship_speed
            display.blit(SPACESHIP_IMAGE, (playerX, playerY))
    else:
        if playerX < DISPLAY_WIDTH - 100:
            playerX += spaceship_speed
            display.blit(SPACESHIP_IMAGE, (playerX, playerY))


def add_invader():
    invaders.append([[randint(0, DISPLAY_WIDTH), randint(0, DISPLAY_HEIGHT-200)], INVADER_IMAGE, 'left' if invaders[-1][2] == 'left' else 'right'])


def add_point():
    global level, invader_speed, text, textRect
    level += 1
    invader_speed += 0.5
    text = font.render(f"Points: " + str(level), True, 'white', 'black')
    display.blit(text, textRect)


def invaders_generator():
    for invader in invaders:
        display.blit(invader[1], invader[0])


def trigger_invaders_movement():
    for invader in invaders:
        if invader[2] == 'left':
            if invader[0][0] > 0:
                invader[0][0] = invader[0][0] - invader_speed

            else:
                invader[0][1] += invader_speed
                invader[2] = 'right'
        else:
            if invader[0][0] < 720:
                invader[0][0] = invader[0][0] + invader_speed
            else:
                invader[0][1] += invader_speed
                invader[2] = 'left'

        display.blit(invader[1], invader[0])
    return level


def generate_shoots():
    for position, missil in enumerate(missiles):
        missil[0][1] -= DFAULT_MISSIL_SPEED
        display.blit(missil[1], missil[0])
        if -20 > missil[0][1]:
            missiles.remove(missil)


def trigger_shoot():
    missiles.append([[playerX, playerY-40], MISSIL_IMAGE])


def impact_on_enemy():
    for invader in invaders:
        for missil in missiles:
            if (
                    invader[0][0] + (DEFAULT_INVADER_SIZE[0]/2) >= missil[0][0] >= invader[0][0] - (DEFAULT_INVADER_SIZE[0] / 2)
            ) and (
                    invader[0][1] + (DEFAULT_INVADER_SIZE[1] / 2) >= missil[0][1] >= invader[0][1] - (DEFAULT_INVADER_SIZE[1] / 2)
            ):
                missiles.remove(missil)
                invaders.remove(invader)
                add_invader()
                add_point()


def check_impact_on_spaceship():
    for invader in invaders:
        if (
                invader[0][0] + (DEFAULT_INVADER_SIZE[0] / 2) >= playerX >= invader[0][0] - (
                DEFAULT_INVADER_SIZE[0] / 2)
        ) and (
                invader[0][1] + (DEFAULT_INVADER_SIZE[1] / 2) >= playerY >= invader[0][1] - (
                DEFAULT_INVADER_SIZE[1] / 2)
        ):
            return True


while game_running:
    clock.tick(60)
    display.fill((0, 0, 0))
    display.blit(BACKGROUND, (0, 0))
    display.blit(text, textRect)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_spaceship('left')
            if event.key == pygame.K_RIGHT:
                move_spaceship('right')
            if event.key == pygame.K_SPACE:
                trigger_shoot()
        if event.type == pygame.QUIT:
            game_running = False
    if not finished:
        if len(missiles) > 0:
            generate_shoots()
        player_definition()
        invaders_generator()
        trigger_invaders_movement()
        impact_on_enemy()
        if check_impact_on_spaceship():
            finished = True
    else:
        display.fill((0, 0, 0))
        display.blit(BACKGROUND, (0, 0))
        font = pygame.font.Font('freesansbold.ttf', 52)
        text = font.render(f"Your record is {level} points.", True, 'white', 'black')
        textRect = text.get_rect()
        textRect.center = (DISPLAY_WIDTH/2, 300)
        display.blit(text, textRect)
    pygame.display.update()

