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

    run = True
    while run:
        clock.tick(FPS)

        player_fleet_positions = []

        for ship in player1.fleet:
            player_fleet_positions.append(ship.position)

        msg = n.send(pickle.dumps(player_fleet_positions))
        player2_fleet_positions = pickle.loads(msg)

        for i in range(len(player2_fleet_positions)):
            player2.fleet[i].position = player2_fleet_positions[i]

        if game.play == False:
            game.draw_menu()
        else:
            game.draw_window()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for player in game.players:
                    for thread in player.threads:
                        thread.get_current_key(event.key)
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


if __name__ == '__main__':
    main()
