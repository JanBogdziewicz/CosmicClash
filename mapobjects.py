import pygame
import random
import math
from player import *
from game import *
from thread import *
from network import *
from config import *


class MapObject:
    def __init__(self, x, y, width, height, hp, space, velocity, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp
        self.space = space
        self.velocity = velocity
        self.image_path = image_path
        self.movement_direction_angle = random.randint(0, 360)

    # object movement in random direction
    def random_movement(self):
        velocity_x = math.cos(self.movement_direction_angle) * self.velocity
        velocity_y = math.sin(self.movement_direction_angle) * self.velocity
        if self.position_in_space(self.x + velocity_x, self.y + velocity_y):
            self.x += velocity_x
            self.y += velocity_y
        else:
            self.change_direction_of_movement()

    # checking if the given coordinates are inside the space where object can move
    def position_in_space(self, x, y):
        return (x + self.width - MIN_DISTANCE >= self.space.x) and \
               (x + self.width + MIN_DISTANCE <= (self.space.x + self.space.width)) and \
               (y + self.height - MIN_DISTANCE >= self.space.y) and \
               (y + self.height + MIN_DISTANCE <= (self.space.y + self.space.height))

    # change direction of random movement of the object
    def change_direction_of_movement(self):
        self.movement_direction_angle = random.randint(0, 360)

    # load image from file
    def load_image(self):
        return pygame.image.load(self.image_path)

    # transform image to proper size
    def transform_image(self, image):
        return pygame.transform.scale(image, (self.width, self.height))

    # return position in the form of tuple
    def get_position(self):
        return self.x, self.y

    # draw image of the object on the window
    def draw(self, window):
        image = self.load_image()
        image = self.transform_image(image)
        window.blit(image, (self.x, self.y))


class Asteroid(MapObject):
    def __init__(self):
        # initial position of the asteroid is between players spaces
        x = random.randint(PLAYER_SPACE_WIDTH + MIN_DISTANCE + 40, WINDOW_WIDTH - PLAYER_SPACE_WIDTH - MIN_DISTANCE - 40)
        y = random.randint(MIN_DISTANCE + 40, WINDOW_HEIGHT - MIN_DISTANCE - 40)
        # asteroid can move everywhere in the window space
        space = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        folder_path = "images/asteroids"
        image_path = os.path.join(folder_path, random.choice(os.listdir(folder_path)))
        super().__init__(x, y, 40, 40, 20, space, 1, image_path)

    # asteroid moves in random direction
    def move(self):
        self.random_movement()


class Missile(MapObject):
    def __init__(self, player_id, x, y):
        # missile can move everywhere in the window space
        space = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        folder_path = "images/player" + str(player_id + 1)
        image_path = os.path.join(folder_path, "missile.png")
        super().__init__(x, y, 20, 16, 5, space, 2, image_path)
        self.player_id = player_id

    # missile moves horizontally in proper direction
    def move(self):
        if self.player_id == 0:
            self.x += self.velocity
        else:
            self.x -= self.velocity


class Ship(MapObject):
    def __init__(self, player_id, ship_id, x, y, color):
        # ship can move everywhere in the player space
        space_x = 0 if player_id == 0 else WINDOW_WIDTH - PLAYER_SPACE_WIDTH
        space = pygame.Rect(space_x, 0, PLAYER_SPACE_WIDTH, WINDOW_HEIGHT)
        folder_path = "images/player" + str(player_id + 1)
        image_path = os.path.join(folder_path, "ship.png")
        super().__init__(x, y, 45, 35, 100, space, 1, image_path)
        self.ship_id = ship_id
        self.player_id = player_id
        self.color = color
        self.max_hp = 100

    def control_movement(self, keys_pressed):
        if keys_pressed[pygame.K_UP] and self.position_in_space(self.x, self.y - self.velocity):
            self.y -= self.velocity

        if keys_pressed[pygame.K_DOWN] and self.position_in_space(self.x, self.y + self.velocity):
            self.y += self.velocity

        if keys_pressed[pygame.K_LEFT] and self.position_in_space(self.x - self.velocity, self.y):
            self.x -= self.velocity

        if keys_pressed[pygame.K_RIGHT] and self.position_in_space(self.x + self.velocity, self.y):
            self.x += self.velocity

    def shoot_missile(self):
        # if player is on the left side of the window, create missile on the right side of the ship and conversely
        x = self.x + self.width / 2 if self.player_id == 0 else self.x - self.width / 2
        return Missile(self.player_id, x, self.y)

    def transform_image(self, image):
        image = pygame.transform.scale(image, (self.width, self.height))
        if self.player_id == 1:
            image = pygame.transform.rotate(image, 180)
        return image
    
    def draw_id(self, window, hb_position):
        id_text = FONT_ID.render(str(self.ship_id), False, self.color)
        id_position = (hb_position[0] - 10, self.y - 20)
        window.blit(id_text, id_position)

    def draw_health_bar(self, window):
        hb_width, hb_height = 60, 8
        hb_position = (self.x - (hb_width - self.width) / 10, self.y - 15)
        hb_fill = self.hp / self.max_hp

        innerPos = (hb_position[0] + 2, hb_position[1] + 2)
        innerSizeGreen = ((hb_width - 4) * hb_fill, hb_height - 4)
        innerSizeRed = ((hb_width - 4), hb_height - 4)
        pygame.draw.rect(window, BLACK, (hb_position, (hb_width, hb_height)), 1)
        pygame.draw.rect(window, RED, (*innerPos, *innerSizeRed))
        pygame.draw.rect(window, GREEN, (*innerPos, *innerSizeGreen))
        self.draw_id(window, hb_position)

    def draw(self, window):
        image = self.load_image()
        image = self.transform_image(image)
        window.blit(image, (self.x, self.y))
        self.draw_health_bar(window)
