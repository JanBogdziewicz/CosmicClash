import pygame
from player import *
from game import *
from thread import *
from network import *
from mapobjects import *
from config import *


if __name__ == '__main__':
    running_program = True

    # create connection between client and server
    net = Network()
    player1 = net.get_player()
    player1_new_missiles = []

    # create game
    game = Game()

    # creating and starting threads for each ship
    token = Queue(maxsize=1)
    token.put(True)
    ship_threads = []
    for idx, ship in enumerate(player1.fleet):
        ship_thread = ShipThread(idx + 1, ship, token)
        ship_thread.start()
        ship_threads.append(ship_thread)

    clock = pygame.time.Clock()
    while running_program:
        clock.tick(60)

        # send data to server
        data_to_send = MessageFromClientToServer(player1, player1_new_missiles)
        player1_new_missiles = []

        # data retrieved from server
        data_retrieved = net.send(data_to_send)
        player2, missiles, asteroids = data_retrieved.unpack()

        # check for asteroid collision with ships
        for asteroid in asteroids:
            for player in [player1, player2]:
                for ship in player.fleet:
                    if asteroid.collides_with(ship):
                        ship.hp -= 20

        for event in pygame.event.get():
            # fire missile by commander ship
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                thread = find_main_thread(ship_threads)
                if thread is not None:
                    player1_new_missiles.append(thread.ship.shoot_missile())

            # change commander ship
            if event.type == pygame.KEYDOWN and event.key in list(THREAD_KEYS.values()):
                thread_id = list(THREAD_KEYS.keys())[list(
                    THREAD_KEYS.values()).index(event.key)]
                thread = find_thread_by_id(ship_threads, thread_id)
                if thread is not None:
                    thread.change_thread()

            # quit the game
            if event.type == pygame.QUIT:
                running_program = False
                pygame.quit()

        # draw all objects present in the game
        map_objects = player1.fleet + player2.fleet + missiles + asteroids
        game.draw_window(map_objects)
