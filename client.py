import pygame
import math
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
        ship_thread = ShipThread(player1.player_id, idx + 1, ship, token)
        ship_thread.start()
        ship_threads.append(ship_thread)

    for ship_thread in ship_threads:
        ship_thread.ship_threads = ship_threads

    ships_in_formation = False

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
                # reload if not on cooldown and if not at full ammo
                if not ship.reload_cooldown and ship.ammo < PLAYER_AMMO:
                    ship.reload_cooldown = AMMO_RELOAD_TIME
                    ship.ammo += 1
                elif ship.ammo < PLAYER_AMMO:
                    ship.reload_cooldown -= 1

        for event in pygame.event.get():
            # fire missile by commander ship
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if thread is not None and thread.ship.ammo > 0:
                    player1_new_missiles.append(thread.ship.shoot_missile())

            # change commander ship
            if event.type == pygame.KEYDOWN and event.key in list(THREAD_KEYS.values()):
                thread_id = list(THREAD_KEYS.keys())[list(
                    THREAD_KEYS.values()).index(event.key)]
                thread = find_thread_by_id(ship_threads, thread_id)
                if thread is not None:
                    thread.change_thread(ship_threads)
                    if ships_in_formation:
                        for ship_thread in ship_threads:
                            ship_thread.release_formation()
                        ships_in_formation = False

            # set or release the formation
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                ship_positions = []
                if not ships_in_formation:
                    if thread is not None:
                        main_ship_position = thread.ship.get_position()
                        for ship_thread in ship_threads:
                            if ship_thread.thread_id != thread.thread_id:
                                ship_position = ship_thread.ship.get_position()
                                vertical_distance = ship_position[1] - \
                                    main_ship_position[1]
                                ship_positions.append(
                                    (ship_thread, vertical_distance))

                        ship_positions.sort(key=lambda x: x[1])

                        for idx, (ship_thread, distance) in enumerate(ship_positions):
                            if idx < math.ceil(len(ship_positions) // 2):
                                position = idx - \
                                    (len(ship_positions) % 2) - \
                                    (len(ship_positions) // 2)
                            else:
                                position = idx + 1 - (len(ship_positions) // 2)

                            ship_thread.set_formation(
                                position, main_ship_position)

                        thread.set_formation(0, main_ship_position)
                        ships_in_formation = True

                else:
                    for ship_thread in ship_threads:
                        ship_thread.release_formation()

                    ships_in_formation = False

            # quit the game
            if event.type == pygame.QUIT:
                running_program = False
                pygame.quit()

        # send position of the leader to other ships in the formation
        if ships_in_formation:
            formation_leader = find_formation_leader(ship_threads)

            if formation_leader is not None:
                leader_position = formation_leader.get_position()
                for ship_thread in ship_threads:
                    ship_thread.set_formation_leader_position(leader_position)

        # draw all objects present in the game
        map_objects = player1.fleet + player2.fleet + missiles + asteroids
        game.draw_window(map_objects)
