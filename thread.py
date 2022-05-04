import threading
from player import *
from game import *
from network import *
from mapobjects import *
from config import *

# keyboards responsible for threads control
THREAD_KEYS = {
    1: pygame.K_1,
    2: pygame.K_2,
    3: pygame.K_3,
    4: pygame.K_4,
    5: pygame.K_5
}


# find thread in the list with the given id, if not found return None
def find_thread_by_id(ship_threads, thread_id):
    for ship_thread in ship_threads:
        if ship_thread.thread_id == thread_id:
            return ship_thread
    return None


# find thread in the list with main flag, if not found return None
def find_main_thread(ship_threads):
    for ship_thread in ship_threads:
        if ship_thread.main:
            return ship_thread
    return None


class ShipThread(threading.Thread):
    def __init__(self, thread_id, ship, token):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.ship = ship
        self.token = token
        self.main = False

    # change main flag
    def change_thread(self):
        if self.main:
            self.token.put(True)
            self.ship.color = RED
            self.main = False

        elif not self.token.empty():
            self.main = self.token.get()
            self.ship.color = GREEN

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            if self.main:
                if self.ship.move:
                    self.ship.control_movement(pygame.key.get_pressed())
                else:
                    self.ship.move = True
            else:
                self.ship.random_movement()
