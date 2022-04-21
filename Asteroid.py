import math
from config import *
from Object import Object


class Asteroid(Object):

    def __init__(self, x, y, space, velocity, sprite):
        super().__init__(x, y, space, velocity, sprite)
        if x > WINDOW_WIDTH // 2:
            self.velocity = -self.velocity

    def randomMovement(self):
        v_x = math.cos(self.directionAngle) * self.velocity
        v_y = math.sin(self.directionAngle) * self.velocity
        if self.inSpace(self.position[X] + v_x, self.position[Y] + v_y):
            self.position[X] += v_x
            self.position[Y] += v_y
        else:
            self.changeDirection(
                self.position[X] + v_x, self.position[Y] + v_y)
