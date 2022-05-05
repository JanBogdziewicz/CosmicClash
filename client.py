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
        # finding main thread
        thread = find_main_thread(ship_threads)

        # send data to server
        data_to_send = MessageFromClientToServer(player1, player1_new_missiles)
        player1_new_missiles = []

        # data retrieved from server
        data_retrieved = net.send(data_to_send)
        player2, missiles, asteroids = data_retrieved.unpack()

        # check for ships collision
        for player in [player1, player2]:
            for ship_id in range(len(player.fleet)):
                ship = player.fleet[ship_id]
                # check for collision with other ships
                for other_ship_id in range(ship_id + 1, len(player.fleet)):
                    other_ship = player.fleet[other_ship_id]
                    if ship.collides_with(other_ship):
                        ship.change_direction_of_movement()
                        other_ship.change_direction_of_movement()
                        if ship.next_move().collides_with(other_ship.next_move()):
                            ship.movement = False
                            other_ship.movement = False
                        if thread:
                            if ship == thread.ship:
                                ship.movement = False
                # check for collisions with asteroids
                for asteroid in asteroids:
                    if ship.collides_with(asteroid):
                        ship.hp -= 20
                # check for collisions with missiles
                for missile in missiles:
                    if ship.collides_with(missile) and missile.player_id != player.player_id:
                        ship.hp -= 20

        for event in pygame.event.get():
            # fire missile by commander ship
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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
