import socket
import pickle
from _thread import start_new_thread
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
            data_to_send = MessageFromServerToClient(players[another_player_id], missiles, asteroids)
            connection_.sendall(pickle.dumps(data_to_send))

        except:
            break

    print(f"Lost connection with player {player_id}")
    available_players.append(player_id)
    connection_.close()


if __name__ == '__main__':
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    number_of_asteroids = 10
    asteroids = [Asteroid() for i in range(number_of_asteroids)]

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
