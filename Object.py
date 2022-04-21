import random
from config import *


class Object(object):

    def __init__(self, x, y, space, velocity, sprite):
        self.position = [x, y]
        self.space = space
        self.velocity = velocity
        self.health = MAX_HEALTH
        self.sprite = sprite
        self.directionAngle = random.randint(0, FULL_ANGLE)

    def changeDirection(self, x, y):
        self.directionAngle = random.randint(0, FULL_ANGLE)

    def inSpace(self, x, y):
        return (x - MIN_DISTANCE >= self.space.x) and (x + MIN_DISTANCE <= (self.space.x + self.space.width)) and \
               (y - MIN_DISTANCE >= self.space.y) and (y +
                                                       MIN_DISTANCE <= (self.space.y + self.space.height))

    def inWindow(self, x, y):
        return (x - MIN_DISTANCE >= 0) and (x + MIN_DISTANCE <= WINDOW_WIDTH) and (y - MIN_DISTANCE >= 0) and (y + MIN_DISTANCE <= WINDOW_HEIGHT)

    def draw(self):
        WIN.blit(self.sprite, (self.position[X], self.position[Y]))
