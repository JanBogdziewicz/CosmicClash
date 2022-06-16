import threading
from player import *
from game import *
from network import *
from mapobjects import *
from config import *
import random
from queue import Queue

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
    def __init__(self, player_id, thread_id, ship, token, player=None):
        threading.Thread.__init__(self)
        self.player = player
        self.player_id = player_id
        self.thread_id = thread_id
        self.ship_threads = None
        self.ship = ship
        self.token = token
        self.main = False
        self.running = True

        self.formation = False
        self.formation_leader_position = (0, 0)
        self.position_in_formation = 0
        self.random_shot_ready = False
        self.random_shot_cooldown = random.randint(50, 250)

    # change main flag
    def change_thread(self, ship_threads):
        if self.main:
            self.ship.color = RED
            self.main = False
        else:
            main_thread = find_main_thread(ship_threads)
            if main_thread is not None:
                main_thread.ship.color = RED
                main_thread.main = False
            
            self.main = True
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

    # shoot missile 
    def shoot_missile(self, velocity=None):
        if self.formation:
            for ship in self.player.fleet:
                self.token.put((self.thread_id, "shoot"))
            
        self.token.put(self.ship.shoot_missile(velocity))

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)

            # check thread information
            if not self.token.empty():
                current_token = self.token.get()
                if isinstance(current_token, tuple):
                    if current_token[0] != self.thread_id:
                        if current_token[1] == "shoot":             
                            self.token.put(self.ship.shoot_missile(10))
                else:
                    self.token.put(current_token)
        
            # control the cooldown of random shot
            if self.random_shot_cooldown > 0:
                self.random_shot_cooldown -= 1

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
