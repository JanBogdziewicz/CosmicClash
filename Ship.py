import pygame
import math
from config import *
from Object import Object


class Ship(Object):

    def __init__(self, x, y, space, velocity, sprite, id):
        self.id = id
        self.color = RED
        super().__init__(x, y, space, velocity, sprite)

    def controlMovement(self, keys_pressed):
        # UP
        if keys_pressed[pygame.K_UP] and self.inSpace(self.position[X], self.position[Y]-self.velocity):
            self.position[Y] -= self.velocity

        # DOWN
        if keys_pressed[pygame.K_DOWN] and self.inSpace(self.position[X], self.position[Y]+self.velocity):
            self.position[Y] += self.velocity

        # LEFT
        if keys_pressed[pygame.K_LEFT] and self.inSpace(self.position[X]-self.velocity, self.position[Y]):
            self.position[X] -= self.velocity

        # RIGHT
        if keys_pressed[pygame.K_RIGHT] and self.inSpace(self.position[X]+self.velocity, self.position[Y]):
            self.position[X] += self.velocity

    def randomMovement(self):
        v_x = math.cos(self.directionAngle) * self.velocity
        v_y = math.sin(self.directionAngle) * self.velocity
        if self.inSpace(self.position[X] + v_x, self.position[Y] + v_y):
            self.position[X] += v_x
            self.position[Y] += v_y
        else:
            self.changeDirection(
                self.position[X] + v_x, self.position[Y] + v_y)
