import pygame
import threading
from Thread import ShipThread
from config import *
from Ship import Ship
from queue import Queue


class Player(object):
    def __init__(self, space, shipsNumber, id):
        self.space = space
        self.fleet = []
        self.threads = []
        self.q = Queue(maxsize=1)
        self.id = id

        for i in range(shipsNumber):
            x = space.x + (space.width / 2)
            y = space.y + (i + 0.5) * (space.height / shipsNumber)
            main = True if i == shipsNumber // 2 else False
            if self.id == 1:
                self.fleet.append(
                    Ship(x, y, space, SHIP_VELOCITY, FACTION_1_SPACESHIP, PROJECTILES_1_MISSILE, i))
            else:
                self.fleet.append(
                    Ship(x, y, space, SHIP_VELOCITY, FACTION_2_COMMANDER, PROJECTILES_2_MISSILE, i))
            self.threads.append(ShipThread(
                i + 1, self.fleet[-1], self.q, main))

    def startGame(self):
        for i in range(len(self.threads)):
            self.threads[i].start()

    def moveShips(self):
        for i in range(len(self.fleet)):
            self.fleet[i].randomMovement()
