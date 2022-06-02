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

players_conn = [False, False]
players = [Player(0), Player(1)]
missiles = []
asteroids = []

# adding new asteroids if one of the existing ones is destroyed
def add_new_asteroid():
    new_asteroid = Asteroid(randrange(9), True)  # 9
    new_asteroid.x = random.randint(2*PLAYER_SPACE_WIDTH,
                                    WINDOW_WIDTH - 2*PLAYER_SPACE_WIDTH)
    new_asteroid.y = random.choice([- MIN_DISTANCE - 40,
                                    WINDOW_HEIGHT + MIN_DISTANCE + 40])
    if new_asteroid.y < 0:
        new_asteroid.movement_direction_angle = 0
    else:
        new_asteroid.movement_direction_angle = 180
    asteroids.append(new_asteroid)


def client_thread(connection_, player_id):
    another_player_id = (player_id + 1) % 2

    # send to the client player object
    players[player_id] = Player(player_id)
    connection_.send(pickle.dumps(players[player_id]))

    while True:
        try:
            # data retrieved from the client
            data_retrieved = pickle.loads(connection_.recv(8192))
            players_conn[player_id], players[player_id], player_new_missiles = data_retrieved.unpack()

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
                players_conn[another_player_id], players[another_player_id], missiles, asteroids)
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
                if asteroid.collides_with(other_asteroid) and (asteroid.out_of_map or other_asteroid.out_of_map):
                    if asteroid.out_of_map:
                        asteroids.remove(asteroid)
                    else:
                        asteroids.remove(other_asteroid)
                    add_new_asteroid()
                elif asteroid.collides_with(other_asteroid):
                    # asteroid.change_direction_of_movement()
                    # other_asteroid.change_direction_of_movement()
                    asteroid.change_direction_of_movement(other_asteroid)
                    # if asteroid.next_move().collides_with(other_asteroid.next_move()):
                    #     asteroid.movement = False
                    #     other_asteroid.movement = False
                    pass
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
        # remove destroyed asteroids and a new one instead of destroyed one
        for asteroid in asteroids:
            if asteroid.hp <= 0:
                asteroids.remove(asteroid)
                add_new_asteroid()

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
        # remove destroyed and out of map missiles
        for missile in missiles:
            if missile.player_id == 0:
                x = missile.x - MIN_DISTANCE
            else:
                x = missile.x + MIN_DISTANCE
            if missile.hp <= 0 or not missile.position_in_space(x, missile.y):
                missiles.remove(missile)


if __name__ == '__main__':
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_thread_running = False

    number_of_asteroids = 15
    asteroids = [Asteroid(randrange(9), False)
                 for i in range(number_of_asteroids)]

    # changing position of colliding asteroids
    for asteroid_id in range(len(asteroids)):
        asteroid = asteroids[asteroid_id]
        for other_asteroid_id in range(asteroid_id, len(asteroids)):
            if asteroid_id != other_asteroid_id:
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
        if available_players:
            connection, address = soc.accept()
            available_players.sort()
            current_player_id = available_players[0]
            available_players.remove(current_player_id)

            print(f"Player {current_player_id} connected to: {address}")

            start_new_thread(client_thread, (connection, current_player_id))
        if all(players_conn) and not server_thread_running:
            start_new_thread(server_thread, ())
            server_thread_running = True
