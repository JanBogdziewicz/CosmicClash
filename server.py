from random import randrange
import socket
import pickle
from _thread import start_new_thread
import sys
from player import *
from game import *
from thread import *
from network import *
from mapobjects import *
from config import *

server = "127.0.0.1"
port = 5555

players = [Player(0), Player(1)]
missiles = []
asteroids = []


def client_thread(connection_, player_id):
    another_player_id = (player_id + 1) % 2

    # send to the client player object
    players[player_id] = Player(player_id)
    connection_.send(pickle.dumps(players[player_id]))

    while True:
        try:
            # data retrieved from the client
            data_retrieved = pickle.loads(connection_.recv(8192))
            players[player_id], player_new_missiles = data_retrieved.unpack()

            # checking if connection is active
            if not data_retrieved:
                print(f"Player {player_id} disconnected")
                available_players.append(player_id)
                break

            # append fired missiles to the list of missiles
            for i in range(len(player_new_missiles)):
                missiles.append(player_new_missiles[i])

            # sent data to the client
            data_to_send = MessageFromServerToClient(
                players[another_player_id], missiles, asteroids)
            connection_.sendall(pickle.dumps(data_to_send))

        except:
            break

    print(f"Lost connection with player {player_id}")
    available_players.append(player_id)
    connection_.close()


def server_thread():
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        # move asteroids
        for asteroid_id in range(len(asteroids)):
            asteroid = asteroids[asteroid_id]
            # check for collisions with other asteroids
            for other_asteroid_id in range(asteroid_id + 1, len(asteroids)):
                other_asteroid = asteroids[other_asteroid_id]
                if asteroid.collides_with(other_asteroid):
                    asteroid.change_direction_of_movement()
                    other_asteroid.change_direction_of_movement()
                    if asteroid.next_move().collides_with(other_asteroid.next_move()):
                        asteroid.movement = False
                        other_asteroid.movement = False
            # check for collisions with ships
            for player in players:
                for ship in player.fleet:
                    if asteroid.collides_with(ship):
                        asteroid.hp = 0
            # check for collisions with missiles
            for missile in missiles:
                if asteroid.collides_with(missile):
                    missile.hp = 0
                    asteroid.hp -= 20
            if asteroid.movement:
                asteroid.move()
            else:
                asteroid.movement = True
        # remove destroyed asteroids
        for asteroid in asteroids:
            if asteroid.hp <= 0:
                asteroids.remove(asteroid)
        # move missiles
        for missile_id in range(len(missiles)):
            missile = missiles[missile_id]
            # check for collisions with players
            for player in players:
                for ship in player.fleet:
                    if missile.collides_with(ship):
                        missile.hp = 0
            # check for collisions with other missiles
            for other_missile_id in range(missile_id+1, len(missiles)):
                other_missile = missiles[other_missile_id]
                if missile.collides_with(other_missile):
                    missile.hp = 0
                    other_missile.hp = 0
            missile.move()
        # remove destroyed missiles
        for missile in missiles:
            if missile.hp <= 0:
                missiles.remove(missile)


if __name__ == '__main__':
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    number_of_asteroids = 15
    asteroids = [Asteroid(randrange(9)) for i in range(number_of_asteroids)]

    # changing position of colliding asteroids
    for asteroid_id in range(len(asteroids)):
        asteroid = asteroids[asteroid_id]
        for other_asteroid_id in range(asteroid_id + 1, len(asteroids)):
            other_asteroid = asteroids[other_asteroid_id]
            while asteroid.collides_with(other_asteroid):
                x = random.randint(PLAYER_SPACE_WIDTH + MIN_DISTANCE + 40,
                                   WINDOW_WIDTH - PLAYER_SPACE_WIDTH - MIN_DISTANCE - 40)
                y = random.randint(MIN_DISTANCE + 40,
                                   WINDOW_HEIGHT - MIN_DISTANCE - 40)
                asteroid.x = x
                asteroid.y = y

    max_number_of_clients = 2
    available_players = [0, 1]

    try:
        soc.bind((server, port))
    except socket.error as se:
        str(se)

    soc.listen(max_number_of_clients)
    print("Waiting for a connection, Server Started")

    while True:
        connection, address = soc.accept()
        available_players.sort()
        current_player_id = available_players[0]
        available_players.remove(current_player_id)

        print(f"Player {current_player_id} connected to: {address}")

        start_new_thread(client_thread, (connection, current_player_id))
        if len(available_players) == 1:
            start_new_thread(server_thread, ())
