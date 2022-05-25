import copy
import pygame
import random
import math
from player import *
from game import *
from thread import *
from network import *
from config import *


class MapObject:
    def __init__(self, x, y, width, height, hp, space, velocity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp
        self.space = space
        self.velocity = velocity
        self.movement_direction_angle = random.randint(0, 360)
        self.movement = True
        self.out_of_map = False  # flag for adding new asteroids

    # object movement in random direction
    def random_movement(self):
        velocity_x = math.cos(self.movement_direction_angle) * self.velocity
        velocity_y = math.sin(self.movement_direction_angle) * self.velocity
        if self.position_in_space(self.x + velocity_x, self.y + velocity_y) or self.out_of_map:
            if self.position_in_space(self.x + velocity_x, self.y + velocity_y) and self.out_of_map:
                self.out_of_map = False
            self.x += velocity_x
            self.y += velocity_y
        else:
            self.change_direction_of_movement()

    # object movement to target position
    def target_movement(self, target):
        x = target[0] - self.x
        y = target[1] - self.y
        z = (x ** 2 + y ** 2) ** 0.5 + 0.0000001
        velocity_x = x / z * self.velocity
        velocity_y = y / z * self.velocity
        if self.position_in_space(self.x + velocity_x, self.y + velocity_y) and z > 5:
            self.x += velocity_x
            self.y += velocity_y

    # checking if the given coordinates are inside the space where object can move
    def position_in_space(self, x, y):
        return (x - MIN_DISTANCE >= self.space.x) and \
               (x + self.width + MIN_DISTANCE <= (self.space.x + self.space.width)) and \
               (y - MIN_DISTANCE >= self.space.y) and \
               (y + self.height + MIN_DISTANCE <=
                (self.space.y + self.space.height))

    # return the same object with position after next move
    def next_move(self):
        result = copy.copy(self)
        velocity_x = math.cos(self.movement_direction_angle) * self.velocity
        velocity_y = math.sin(self.movement_direction_angle) * self.velocity
        result.x += velocity_x
        result.y += velocity_y
        return result

    # change direction of random movement of the object
    def change_direction_of_movement(self):
        self.movement_direction_angle = random.randint(0, 360)

    # return position in the form of tuple
    def get_position(self):
        return self.x, self.y

    # draw image of the object on the window, abstract method to be implemented in subclasses
    def draw(self):
        raise NotImplementedError("Please Implement this method")

    # check whether this and given object collide
    def collides_with(self, other_obj):
        object_center = pygame.Vector2(
            (self.x + self.width/2, self.y + self.height/2))
        object_radius = self.width / 2
        oth_object_center = pygame.Vector2(
            (other_obj.x + other_obj.width/2, other_obj.y + other_obj.height/2))
        oth_object_radius = other_obj.width / 2
        distance = object_center.distance_to(oth_object_center)
        return distance < object_radius + oth_object_radius


class Asteroid(MapObject):
    def __init__(self, image_id, out_of_map):
        # initial position of the asteroid is between players spaces
        x = random.randint(PLAYER_SPACE_WIDTH + MIN_DISTANCE + 40,
                           WINDOW_WIDTH - PLAYER_SPACE_WIDTH - MIN_DISTANCE - 40)
        y = random.randint(MIN_DISTANCE + 40,
                           WINDOW_HEIGHT - MIN_DISTANCE - 40)
        # asteroid can move everywhere in the window space
        space = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        super().__init__(x, y, 40, 40, 100, space, 1)
        self.image_id = image_id
        self.out_of_map = out_of_map

    # asteroid moves in random direction
    def move(self):
        self.random_movement()

    def draw(self, window):
        window.blit(ASTEROIDS[self.image_id], (self.x, self.y))


class Missile(MapObject):
    def __init__(self, player_id, x, y):
        # missile can move everywhere in the window space
        space = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        super().__init__(x, y, 20, 16, 5, space, 3)
        self.player_id = player_id

    # missile moves horizontally in proper direction
    def move(self):
        if self.player_id == 0:
            self.x += self.velocity
        else:
            self.x -= self.velocity

    # overriding collision so that missiles don't
    # collide with ones from the same player nor
    # with the ship that shot the missile
    def collides_with(self, other_obj):
        if isinstance(other_obj, Missile) or isinstance(other_obj, Ship):
            return self.player_id != other_obj.player_id and super().collides_with(other_obj)
        else:
            return super().collides_with(other_obj)

    def draw(self, window):
        if self.player_id == 0:
            window.blit(PLAYER_1_MISSILE, (self.x, self.y))
        else:
            window.blit(PLAYER_2_MISSILE, (self.x, self.y))


class Ship(MapObject):
    def __init__(self, player_id, ship_id, x, y, color):
        # ship can move everywhere in the player space
        space_x = 0 if player_id == 0 else WINDOW_WIDTH - PLAYER_SPACE_WIDTH
        space = pygame.Rect(space_x, 0, PLAYER_SPACE_WIDTH, WINDOW_HEIGHT)
        super().__init__(x, y, 45, 35, 100, space, 2)
        self.ship_id = ship_id
        self.player_id = player_id
        self.color = color
        self.max_hp = 100
        self.ammo = PLAYER_AMMO
        self.reload_cooldown = AMMO_RELOAD_TIME

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
        # remove one ammo from ship magazine
        self.ammo -= 1
        return Missile(self.player_id, x, self.y + self.height / 2 - MIN_DISTANCE / 2)

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
        pygame.draw.rect(
            window, BLACK, (hb_position, (hb_width, hb_height)), 1)
        pygame.draw.rect(window, RED, (*innerPos, *innerSizeRed))
        pygame.draw.rect(window, GREEN, (*innerPos, *innerSizeGreen))
        self.draw_id(window, hb_position)

    def draw(self, window):
        if self.player_id == 0:
            window.blit(PLAYER_1_SHIP, (self.x, self.y))
        else:
            window.blit(PLAYER_2_SHIP, (self.x, self.y))
        self.draw_health_bar(window)
