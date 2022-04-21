from turtle import pos
import pygame
import random
from config import *
from Asteroid import Asteroid
from Button import Button


class Game(object):

    def __init__(self):
        self.asteroid_list = self.load_asteroids()
        self.obstacles = self.create_obstacles()
        self.players = []
        self.play = False
        self.start_button = Button(START_BUTTON[0],
                                   START_BUTTON[1],
                                   START_BUTTON[2],
                                   START_BUTTON[3],
                                   START_BUTTON[4],
                                   self.switch_play)

    def switch_play(self):
        self.play = True

    def load_asteroids(self):
        asteroid1 = pygame.transform.scale(pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', 'asteroidR1.png')), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        asteroid2 = pygame.transform.scale(pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', 'asteroidR2.png')), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        asteroid3 = pygame.transform.scale(pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', 'asteroidR3.png')), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        asteroid4 = pygame.transform.scale(pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', 'asteroidR4.png')), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        asteroid5 = pygame.transform.scale(pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', 'asteroidR5.png')), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        asteroid6 = pygame.transform.scale(pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', 'asteroidR6.png')), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        asteroid7 = pygame.transform.scale(pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', 'asteroidR7.png')), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        asteroid8 = pygame.transform.scale(pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', 'asteroidR8.png')), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        asteroid9 = pygame.transform.scale(pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', 'asteroidR9.png')), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

        asteroid_images = [asteroid1, asteroid2, asteroid3,
                           asteroid4, asteroid5, asteroid6, asteroid7, asteroid8, asteroid9]

        return asteroid_images

    def obstacle_random_start_position(self):
        x = random.randrange(
            SPACE_WIDTH*2, (WINDOW_WIDTH - 2*SPACE_WIDTH) - OBSTACLE_WIDTH)
        y = random.randrange(
            OBSTACLE_HEIGHT, WINDOW_HEIGHT - 2*OBSTACLE_HEIGHT)
        return x, y

    def create_obstacles(self):
        obstacles = []
        for i in range(ASTEROIDS_NUMBER):
            index = random.randrange(0, 7)
            x, y = self.obstacle_random_start_position()
            obstacles.append(Asteroid(x, y, ASTEROID_SPACE,
                             SHIP_VELOCITY, self.asteroid_list[index]))
        return obstacles

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.randomMovement()
            WIN.blit(obstacle.sprite, obstacle.position)

    def draw_ships(self):
        for player in self.players:
            for ship in player.fleet:
                WIN.blit(ship.sprite, (ship.position[X], ship.position[Y]))
                self.draw_health_bar((ship.position[X] - (HEALTH_BAR_SIZE[0]-SPACESHIP_WIDTH)/2, ship.position[Y] - 15),
                                     HEALTH_BAR_SIZE, ship.health/MAX_HEALTH)
                self.draw_id(
                    ship.id, (ship.position[X] - (HEALTH_BAR_SIZE[0]-SPACESHIP_WIDTH)/2 - 10, ship.position[Y] - 20), ship.color)

    def draw_missiles(self):
        for player in self.players:
            for ship in player.fleet:
                for missile in ship.missiles:
                    WIN.blit(missile.sprite,
                             (missile.position[X], missile.position[Y]))

    def draw_health_bar(self, position, size, fill_level):
        pygame.draw.rect(WIN, BLACK, (*position, *size), 1)
        innerPos = (position[0]+2, position[1]+2)
        innerSizeGreen = ((size[0]-4) * fill_level, size[1]-4)
        innerSizeRed = ((size[0]-4), size[1]-4)
        pygame.draw.rect(WIN, RED, (*innerPos, *innerSizeRed))
        pygame.draw.rect(WIN, GREEN, (*innerPos, *innerSizeGreen))

    def draw_id(self, id, position, color):
        ship_1_text = FONT_ID.render('1', False, color)
        ship_2_text = FONT_ID.render('2', False, color)
        ship_3_text = FONT_ID.render('3', False, color)

        if id == 0:
            WIN.blit(ship_1_text, position)
        elif id == 1:
            WIN.blit(ship_2_text, position)
        elif id == 2:
            WIN.blit(ship_3_text, position)

    def draw_window(self):
        WIN.fill(WHITE)
        WIN.blit(BACKGROUND, (0, 0))
        self.draw_obstacles()
        self.draw_ships()
        self.draw_missiles()
        pygame.display.update()

    def draw_menu(self):
        WIN.blit(BACKGROUND, (0, 0))
        WIN.blit(LOGO, (WINDOW_WIDTH/2-LOGO_WIDTH/2, 50))
        self.start_button.draw()
        pygame.display.update()
