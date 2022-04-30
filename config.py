import pygame
import os

WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 700

LOGO_WIDTH, LOGO_HEIGHT = 360, 250
LOGO_IMAGE_PATH = os.path.join("images/game", "logo.png")
LOGO = pygame.transform.scale(pygame.image.load(
    LOGO_IMAGE_PATH), (LOGO_WIDTH, LOGO_HEIGHT))

ICON_IMAGE_PATH = os.path.join("images/game", "icon.gif")
ICON = pygame.image.load(ICON_IMAGE_PATH)

BACKGROUND_IMAGE_PATH = os.path.join("images/game", "background.jpg")
BACKGROUND = pygame.transform.scale(pygame.image.load(
    BACKGROUND_IMAGE_PATH), (WINDOW_WIDTH, WINDOW_HEIGHT))
BACKGROUND.set_alpha(180)

SHIP_WIDTH, SHIP_HEIGHT = 45, 35

PLAYER_1_SHIP_PATH = os.path.join("images/player1", "ship.png")
PLAYER_1_SHIP = pygame.transform.scale(pygame.image.load(
    PLAYER_1_SHIP_PATH), (SHIP_WIDTH, SHIP_HEIGHT))

PLAYER_2_SHIP_PATH = os.path.join("images/player2", "ship.png")
PLAYER_2_SHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    PLAYER_2_SHIP_PATH), (SHIP_WIDTH, SHIP_HEIGHT)), 180)

MISSILE_WIDTH, MISSILE_HEIGHT = 20, 16

PLAYER_1_MISSILE_PATH = os.path.join("images/player1", "missile.png")
PLAYER_1_MISSILE = pygame.transform.scale(pygame.image.load(
    PLAYER_1_MISSILE_PATH), (MISSILE_WIDTH, MISSILE_HEIGHT))

PLAYER_2_MISSILE_PATH = os.path.join("images/player2", "missile.png")
PLAYER_2_MISSILE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    PLAYER_2_MISSILE_PATH), (MISSILE_WIDTH, MISSILE_HEIGHT)), 180)

ASTEROID_WIDTH, ASTEROID_HEIGHT = 40, 40

ASTEROID_PATHS = [
    os.path.join("images/asteroids", "asteroidR1.png"),
    os.path.join("images/asteroids", "asteroidR2.png"),
    os.path.join("images/asteroids", "asteroidR3.png"),
    os.path.join("images/asteroids", "asteroidR4.png"),
    os.path.join("images/asteroids", "asteroidR5.png"),
    os.path.join("images/asteroids", "asteroidR6.png"),
    os.path.join("images/asteroids", "asteroidR7.png"),
    os.path.join("images/asteroids", "asteroidR8.png"),
    os.path.join("images/asteroids", "asteroidR9.png")
]

ASTEROIDS = [
    pygame.transform.scale(pygame.image.load(
        ASTEROID_PATHS[0]), (ASTEROID_WIDTH, ASTEROID_HEIGHT)),
    pygame.transform.scale(pygame.image.load(
        ASTEROID_PATHS[1]), (ASTEROID_WIDTH, ASTEROID_HEIGHT)),
    pygame.transform.scale(pygame.image.load(
        ASTEROID_PATHS[2]), (ASTEROID_WIDTH, ASTEROID_HEIGHT)),
    pygame.transform.scale(pygame.image.load(
        ASTEROID_PATHS[3]), (ASTEROID_WIDTH, ASTEROID_HEIGHT)),
    pygame.transform.scale(pygame.image.load(
        ASTEROID_PATHS[4]), (ASTEROID_WIDTH, ASTEROID_HEIGHT)),
    pygame.transform.scale(pygame.image.load(
        ASTEROID_PATHS[5]), (ASTEROID_WIDTH, ASTEROID_HEIGHT)),
    pygame.transform.scale(pygame.image.load(
        ASTEROID_PATHS[6]), (ASTEROID_WIDTH, ASTEROID_HEIGHT)),
    pygame.transform.scale(pygame.image.load(
        ASTEROID_PATHS[7]), (ASTEROID_WIDTH, ASTEROID_HEIGHT)),
    pygame.transform.scale(pygame.image.load(
        ASTEROID_PATHS[8]), (ASTEROID_WIDTH, ASTEROID_HEIGHT)),
]

pygame.font.init()
FONT = pygame.font.SysFont('Courier New', 35, bold=pygame.font.Font.bold)
FONT_ID = pygame.font.SysFont('Courier New', 15, bold=pygame.font.Font.bold)

BUTTON_WIDTH, BUTTON_HEIGHT = 250, 60

PLAYER_SPACE_WIDTH = 0.15 * WINDOW_WIDTH

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (34, 139, 34)
RED = (153, 0, 0)

MIN_DISTANCE = 15
