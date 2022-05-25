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


# find ship which is the leader of the formation, if not found return None
def find_formation_leader(ship_threads):
    for ship_thread in ship_threads:
        if ship_thread.formation and ship_thread.position_in_formation == 0:
            return ship_thread.ship
    return None


class ShipThread(threading.Thread):
    def __init__(self, player_id, thread_id, ship, token):
        threading.Thread.__init__(self)
        self.player_id = player_id
        self.thread_id = thread_id
        self.ship_threads = None
        self.ship = ship
        self.token = token
        self.main = False

        self.formation = False
        self.formation_leader_position = (0, 0)
        self.position_in_formation = 0

    # change main flag
    # if thread was main remove the token and add it to the pool
    # if thread wan't main get token from pool or current main
    def change_thread(self, ship_threads):
        if self.main:
            self.token.put(True)
            self.ship.color = RED
            self.main = False
        elif self.token.empty():
            main_thread = find_main_thread(ship_threads)
            main_thread.token.put(True)
            main_thread.ship.color = RED
            main_thread.main = False

            self.main = self.token.get()
            self.ship.color = GREEN
        else:
            self.main = self.token.get()
            self.ship.color = GREEN

    # set ships in the formation
    def set_formation(self, position, leader_position):
        self.position_in_formation = position
        self.formation_leader_position = leader_position
        self.formation = True

    # release ships from the formation
    def release_formation(self):
        self.position_in_formation = 0
        self.formation_leader_position = (0, 0)
        self.formation = False

    # set position of the leader of the formation
    def set_formation_leader_position(self, position):
        self.formation_leader_position = position

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            # player controls the movement of the ship through the keyboard
            if self.main and not self.formation:
                if self.ship.movement:
                    self.ship.control_movement(pygame.key.get_pressed())
                else:
                    self.ship.movement = True

            # movement of the formation
            if self.formation and self.position_in_formation == 0:
                if self.ship.movement:
                    if find_main_thread(self.ship_threads) is not None:
                        self.ship.control_movement(pygame.key.get_pressed())
                    else:
                        self.ship.random_movement()
                else:
                    self.ship.movement = True

            # ship follows the main ship in the formation
            elif self.formation:
                if self.ship.movement:
                    side = -1 if self.player_id == 0 else 1
                    target = (self.formation_leader_position[0] + side * abs(self.position_in_formation * FORMATION_DISTANCE),
                              self.formation_leader_position[1] + self.position_in_formation * FORMATION_DISTANCE)
                    self.ship.target_movement(target)
                else:
                    self.ship.movement = True

            # ship moves in random direction (not commander and not in formation)
            elif not self.main and not self.formation:
                if self.ship.movement:
                    self.ship.random_movement()
                else:
                    self.ship.movement = True
