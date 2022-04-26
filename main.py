import sys
import pygame
from config import *
from Player import Player
from Game import Game
from network import Network
import pickle


def draw_window(player1):
    WIN.fill(WHITE)
    player1.displayShips()
    pygame.display.update()

# def make_pos(list):
#     return str(list[0]) + "," + str(list[1])

# def read_pos(str):
#     str = str.split(",")
#     return [int(str[0]), int(str[1])]


def main():

    # network part
    n = Network()
    cooldown = 0
    player_id = int(n.getPos())

    if player_id == 0:
        player1 = Player(PLAYER1_SPACE, 3, 1)
        player2 = Player(PLAYER2_SPACE, 3, 2)

    if player_id == 1:
        player1 = Player(PLAYER2_SPACE, 3, 2)
        player2 = Player(PLAYER1_SPACE, 3, 1)

    player1.startGame()

    game = Game()
    game.players.append(player1)
    game.players.append(player2)

    clock = pygame.time.Clock()
    display_message = False
    run = True
    while run:
        clock.tick(FPS)
        
        # list that will contain all information that needs to be sent
        # first - ships positions
        # second - new missle id
        # third - should server display message

        data_to_send = [None, None, None]

        player_fleet_positions = []
        missile_id = None
        display_message = False

        for ship in player1.fleet:
            player_fleet_positions.append(ship.position)
        
        if cooldown == 180:
            display_message = True
            cooldown = 0
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for thread in player1.threads:
                        if thread.main:
                            missile_id = thread.threadID

                for player in game.players:
                    for thread in player.threads:
                        thread.get_current_key(event.key)

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        data_to_send[0] = player_fleet_positions
        data_to_send[1] = missile_id
        data_to_send[2] = display_message

        msg = n.send(pickle.dumps(data_to_send))
        msg_loaded = pickle.loads(msg)
        player2_fleet_positions = msg_loaded[0]

        for i in range(len(player2_fleet_positions)):
            player2.fleet[i].position = player2_fleet_positions[i]

        if msg_loaded[1] is not None:
            player2.fleet[msg_loaded[1] - 1].shootMissile()

        for ship in player2.fleet:
            ship.decreaseCooldown()

        for player in game.players:
            for ship in player.fleet:
                for missile in ship.missiles:
                    exist = missile.move()
                    if not exist:
                        ship.missiles.remove(missile)

        if game.play == False:
            game.draw_menu()
        else:
            game.draw_window()

        cooldown += 1


if __name__ == '__main__':
    main()
