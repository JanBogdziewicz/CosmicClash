import pygame
import os
pygame.font.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cosmic Clash")
LOGO_WIDTH, LOGO_HEIGHT = 360, 250
LOGO = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'logo.png')), (LOGO_WIDTH, LOGO_HEIGHT))
ICON = pygame.image.load(os.path.join('assets', 'icon.gif'))
BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'space_background.jpg')), (WINDOW_WIDTH, WINDOW_HEIGHT))
BACKGROUND.set_alpha(180)
pygame.display.set_icon(ICON)

FONT = pygame.font.SysFont('Courier New', 35, bold=pygame.font.Font.bold)
FONT_ID = pygame.font.SysFont('Courier New', 15, bold=pygame.font.Font.bold)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (34, 139, 34)
RED = (153, 0, 0)

FPS = 60

BUTTON_WIDTH, BUTTON_HEIGHT = 250, 60

ASTEROIDS_NUMBER = 15
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 10, 10

HEALTH_BAR_SIZE = (60, 8)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 45, 35
COMMANDER_WIDTH, COMMANDER_HEIGTH = 60, 55
MISSILE_WIDTH, MISSILE_HEIGHT = 20, 16

FACTION_1_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'faction1', 'blueshuttlenoweps.png'))
FACTION_1_SPACESHIP = pygame.transform.scale(
    FACTION_1_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

FACTION_1_COMMANDER_IMAGE = pygame.image.load(
    os.path.join('assets', 'faction1', 'bluecarrier.png'))
FACTION_1_COMMANDER = pygame.transform.scale(
    FACTION_1_COMMANDER_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

PROJECTILES_1_MISSILE_IMAGE = pygame.image.load(
    os.path.join('assets', 'projectiles', 'Blood-Magic-Effect_03.png'))
PROJECTILES_1_MISSILE = pygame.transform.scale(
    PROJECTILES_1_MISSILE_IMAGE, (MISSILE_WIDTH, MISSILE_HEIGHT))

FACTION_2_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'faction2', 'cruiser.png'))
FACTION_2_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    FACTION_2_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

FACTION_2_COMMANDER_IMAGE = pygame.image.load(
    os.path.join('assets', 'faction2', 'destroyer.png'))
FACTION_2_COMMANDER = pygame.transform.rotate(pygame.transform.scale(
    FACTION_2_COMMANDER_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

PROJECTILES_2_MISSILE_IMAGE = pygame.image.load(
    os.path.join('assets', 'projectiles', 'Blood-Magic-Effect_12.png'))
PROJECTILES_2_MISSILE = pygame.transform.rotate(pygame.transform.scale(
    PROJECTILES_2_MISSILE_IMAGE, (MISSILE_WIDTH, MISSILE_HEIGHT)), 180)

SHIP_RADIUS = 6
SHIP_VELOCITY = 2
MISSILE_VELOCITY = 2
MAX_HEALTH = 100
SPACE_WIDTH = 0.15 * WINDOW_WIDTH
MIN_DISTANCE = 10
FULL_ANGLE = 360
RIGHT_ANGLE = 90

X = 0
Y = 1


PLAYER1_KEYS = {
    'KEY_UP': pygame.K_w,
    'KEY_DOWN': pygame.K_s,
    'KEY_LEFT': pygame.K_a,
    'KEY_RIGHT': pygame.K_d,
}
PLAYER1_SPACE = pygame.Rect(
    10, HEALTH_BAR_SIZE[Y], SPACE_WIDTH, WINDOW_HEIGHT-SPACESHIP_HEIGHT)

PLAYER2_KEYS = {
    'KEY_UP': pygame.K_UP,
    'KEY_DOWN': pygame.K_DOWN,
    'KEY_LEFT': pygame.K_LEFT,
    'KEY_RIGHT': pygame.K_RIGHT,
}
PLAYER2_SPACE = pygame.Rect(
    WINDOW_WIDTH - SPACE_WIDTH - 10, HEALTH_BAR_SIZE[Y], SPACE_WIDTH, WINDOW_HEIGHT-SPACESHIP_HEIGHT)


START_BUTTON = ('START', BUTTON_WIDTH, BUTTON_HEIGHT,
                (WINDOW_WIDTH/2-BUTTON_WIDTH/2, 50 + LOGO_HEIGHT + 50), 3)
