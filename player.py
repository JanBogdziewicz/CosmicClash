import pygame
import threading
from queue import Queue
from game import *
from thread import *
from network import *
from mapobjects import *
from config import *


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        space_x = 0 if player_id == 0 else WINDOW_WIDTH - PLAYER_SPACE_WIDTH
        self.space = pygame.Rect(space_x, 0, PLAYER_SPACE_WIDTH, WINDOW_HEIGHT)
        self.fleet = self.create_fleet()

    def create_fleet(self, ships_number=3):
        fleet = []
        for ship_num in range(ships_number):
            x = self.space.x + self.space.width / 2
            y = self.space.y + (ship_num + 0.5) * \
                (self.space.height / ships_number)
            ship = Ship(self.player_id, ship_num + 1, x, y, RED)
            fleet.append(ship)
        return fleet
