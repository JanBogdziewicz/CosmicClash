import pygame
import os

WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 700

LOGO_WIDTH, LOGO_HEIGHT = 360, 250
LOGO_IMAGE_PATH = os.path.join("images/game", "logo.png")
LOGO = pygame.transform.scale(pygame.image.load(LOGO_IMAGE_PATH), (LOGO_WIDTH, LOGO_HEIGHT))

ICON_IMAGE_PATH = os.path.join("images/game", "icon.gif")
ICON = pygame.image.load(ICON_IMAGE_PATH)

BACKGROUND_IMAGE_PATH = os.path.join("images/game", "background.jpg")
BACKGROUND = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE_PATH), (WINDOW_WIDTH, WINDOW_HEIGHT))
BACKGROUND.set_alpha(180)

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

MIN_DISTANCE = 20


