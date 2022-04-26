import math
import pygame
from config import *
from Object import Object
from Missile import Missile


class Ship(Object):

    def __init__(self, x, y, space, velocity, sprite, missile_sprite, id, color):
        self.id = id
        self.color = color
        super().__init__(x, y, space, velocity, sprite)
        self.missile_sprite = missile_sprite
        self.missiles = []
        self.missile_cooldown = False
        self.missile_cooldown_count = 20

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

    def shootMissile(self):
        if not self.missile_cooldown:
            missile = Missile(self.position[X] + SPACESHIP_WIDTH/2, self.position[Y] + (
                (SPACESHIP_HEIGHT - 15)/2), self.space, MISSILE_VELOCITY, self.missile_sprite)
            self.missiles.append(missile)
            self.missile_cooldown = True
            self.missile_cooldown_count = 20
    
    def decreaseCooldown(self):
        self.missile_cooldown_count -= 1
        if self.missile_cooldown_count == 0:
            self.missile_cooldown = False
            self.missile_cooldown_count = 20
