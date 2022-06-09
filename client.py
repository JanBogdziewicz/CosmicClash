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
    token = Queue()
    ship_threads = []
    for idx, ship in enumerate(player1.fleet):
        ship_thread = ShipThread(player1.player_id, idx + 1, ship, token, player=player1)
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
        data_to_send = MessageFromClientToServer(
            game.player_connected, player1, player1_new_missiles)
        player1_new_missiles = []

        # thread messages
        if not token.empty():
            current_token = token.get()
            if isinstance(current_token, Missile):
                player1_new_missiles.append(current_token)
            else:
                token.put(current_token)

        # data retrieved from server
        data_retrieved = net.send(data_to_send)
        game.game_started, player2, missiles, asteroids = data_retrieved.unpack()

        # check for ships collision
        ship_number = len(player1.fleet)
        ship_id = 0
        while ship_id < ship_number:
            ship = player1.fleet[ship_id]
            # check for collision with other ships
            for other_ship_id in range(ship_id + 1, len(player1.fleet)):
                other_ship = player1.fleet[other_ship_id]
                if ship.collides_with(other_ship):
                    ship.change_direction_of_movement(other_ship)
                    if thread:
                        if ship == thread.ship:
                            ship.movement = False
            # check for collisions with asteroids
            for asteroid in asteroids:
                if ship.collides_with(asteroid):
                    ship.hp -= 20
            # check for collisions with missiles
            for missile in missiles:
                if ship.collides_with(missile) and missile.player_id != player1.player_id:
                    ship.hp -= 20
            # reload if not on cooldown and if not at full ammo
            if not ship.reload_cooldown and ship.ammo < PLAYER_AMMO:
                ship.reload_cooldown = AMMO_RELOAD_TIME
                ship.ammo += 1
            elif ship.ammo < PLAYER_AMMO:
                ship.reload_cooldown -= 1
            # remove destoryed ships and stop their threads
            if ship.hp <= 0:
                player1.fleet.remove(ship)
                thread = find_thread_by_id(ship_threads, ship.ship_id)
                if thread is not None:
                    if thread.main:
                        thread.main = False
                        if ships_in_formation:
                            for ship_thread in ship_threads:
                                ship_thread.release_formation()
                            ships_in_formation = False
                    thread.running = False
                    ship_threads.remove(thread)
                ship_id -= 1
                ship_number -= 1
            ship_id += 1
        # check if player has any ships in fleet if not end game
        if not player1.fleet and not game.game_over:
            game.game_over = True
            game.game_outcome = "You lost!!!"
        elif not player2.fleet and not game.game_over:
            game.game_over = True
            game.game_outcome = "Congratulations, you won!!!"

        # autonomous missile firing by ships
        for thread in ship_threads:
            if not thread.main:
                for asteroid in asteroids:
                    if thread.ship.is_coming_asteroid(asteroid) and thread.random_shot_cooldown == 0:
                        thread.shoot_missile()
                        thread.random_shot_cooldown = 10

        for event in pygame.event.get():
            # fire missile by commander ship
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if thread is not None and thread.ship.ammo > 0:
                    # if ships_in_formation:
                    #     for ship in player1.fleet:
                    #         player1_new_missiles.append(ship.shoot_missile(velocity=10))
                    # else:
                    #     player1_new_missiles.append(thread.ship.shoot_missile())
                    if ships_in_formation:
                        thread.shoot_missile(velocity=10)
                    else:
                        thread.shoot_missile()

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
