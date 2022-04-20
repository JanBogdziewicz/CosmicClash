from config import *
from Object import Object


class Missile(Object):
    def __init__(self, x, y, space, velocity, sprite):
        super().__init__(x, y, space, velocity, sprite)
        if x > WINDOW_WIDTH // 2:
            self.velocity = -self.velocity

    def move(self):
        if self.inWindow(self.position[X] + self.velocity, self.position[Y]):
            self.position[X] += self.velocity
            return True
        else:
            return False


