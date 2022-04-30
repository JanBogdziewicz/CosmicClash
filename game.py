import pygame
from player import *
from thread import *
from network import *
from mapobjects import *
from config import *


class Game:
    def __init__(self):
        self.game_started = False
        self.window = self.create_window()
        self.start_button = Button(self.start_game, self.window)

    # create game window
    def create_window(self):
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Cosmic Clash")
        pygame.display.set_icon(ICON)
        return window

    # change state of the game
    def start_game(self):
        self.game_started = True

    # dram game map
    def draw_game(self, map_objects):
        self.window.fill(WHITE)
        self.window.blit(BACKGROUND, (0, 0))
        for map_object in map_objects:
            map_object.draw(self.window)
        pygame.display.update()

    # dram menu before starting the game
    def draw_menu(self):
        self.window.fill(WHITE)
        self.window.blit(BACKGROUND, (0, 0))
        self.window.blit(LOGO, (WINDOW_WIDTH / 2 - LOGO_WIDTH / 2, 50))
        self.start_button.draw()
        pygame.display.update()

    # draw either menu or game map on the window
    def draw_window(self, map_objects):
        if self.game_started:
            self.draw_game(map_objects)
        else:
            self.draw_menu()


class Button:
    def __init__(self, action, window):
        self.pressed = False
        self.elevation = 3
        self.dynamic_elevation = self.elevation
        self.position = (WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2, LOGO_HEIGHT + 100)
        self.action = action
        self.window = window

        self.top_rect = pygame.Rect(self.position, (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.top_color = '#475F77'

        self.bottom_rect = pygame.Rect(self.position, (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.bottom_color = '#354B5E'

        self.text_surf = FONT.render("Start", True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        self.top_rect.y = self.position[1] - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.window, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(self.window, self.top_color, self.top_rect, border_radius=12)
        self.window.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_position = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_position):
            self.top_color = RED
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.action()
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = BLACK
