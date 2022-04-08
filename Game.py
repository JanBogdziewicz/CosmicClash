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
        asteroids = []
        asteroid1 = pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', '08.png'))
        asteroid2 = pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', '07.png'))
        asteroid3 = pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', '06.png'))
        asteroid4 = pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', '05.png'))
        asteroid5 = pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', '01.png'))
        asteroid6 = pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', '02.png'))
        asteroid7 = pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', '03.png'))
        asteroid8 = pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', '04.png'))
        asteroid9 = pygame.image.load(os.path.join(
            'assets', 'asteroids', 'Asteroids', 'Mini', '09.png'))

        asteroid_images = [asteroid1, asteroid2, asteroid3,
                           asteroid4, asteroid5, asteroid6, asteroid7, asteroid8, asteroid9]

        return asteroid_images

    def obstacle_random_start_position(self):
        x = random.randrange(
            SPACE_WIDTH*2, (WINDOW_WIDTH - 2*SPACE_WIDTH) - 10*OBSTACLE_WIDTH)
        y = random.randrange(0, WINDOW_HEIGHT - 10*OBSTACLE_HEIGHT)
        return x, y

    def create_obstacles(self):
        obstacles = []
        for i in range(ASTEROIDS_NUMBER):
            index = random.randrange(0, 7)
            x, y = self.obstacle_random_start_position()
            obstacles.append(Asteroid(x, y, pygame.Rect(
                x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT), SHIP_VELOCITY, self.asteroid_list[index]))
        return obstacles

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            WIN.blit(obstacle.sprite, obstacle.position)

    def draw_ships(self):
        for player in self.players:
            for ship in player.fleet:
                WIN.blit(ship.sprite, (ship.position[X], ship.position[Y]))
                self.draw_health_bar((ship.position[X] - (HEALTH_BAR_SIZE[0]-SPACESHIP_WIDTH)/2, ship.position[Y] - 15),
                                     HEALTH_BAR_SIZE, ship.health/MAX_HEALTH)
                self.draw_id(
                    ship.id, (ship.position[X] - (HEALTH_BAR_SIZE[0]-SPACESHIP_WIDTH)/2 - 10, ship.position[Y] - 20), ship.color)

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
        pygame.display.update()

    def draw_menu(self):
        WIN.blit(BACKGROUND, (0, 0))
        WIN.blit(LOGO, (WINDOW_WIDTH/2-LOGO_WIDTH/2, 50))
        self.start_button.draw()
        pygame.display.update()
