import threading
import pygame
from config import *

THREAD_KEYS = {
    1: pygame.K_1,
    2: pygame.K_2,
    3: pygame.K_3,
    4: pygame.K_4,
    5: pygame.K_5
}

class ShipThread(threading.Thread):
    def __init__(self, threadID, ship, q, main=False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.ship = ship
        self.q = q
        self.main = main
        self.current_key = None
        self.cooldown = 20

    def get_current_key(self, key):
        self.current_key = key

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(FPS)
            if self.cooldown == 0:
                self.ship.missile_cooldown = False
                self.cooldown = 20
            else:
                self.cooldown -= 1

            if self.current_key == THREAD_KEYS[self.threadID] and self.main:
                self.q.put(True)
                self.ship.color = RED
                self.main = False
                self.current_key = None

            if self.current_key == THREAD_KEYS[self.threadID] and not self.q.empty():
                self.main = self.q.get()
                self.ship.color = GREEN
                self.current_key = None

            if self.current_key == pygame.K_SPACE and self.main:
                self.ship.shootMissile()
                self.current_key = None

            if self.main:
                self.ship.controlMovement(pygame.key.get_pressed())
                
            else:
                self.ship.randomMovement()

            
