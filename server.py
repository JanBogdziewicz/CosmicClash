import socket
from _thread import *
import sys
import pickle

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

fleets = [None, None]
missiles = [None, None]

def threaded_client(conn, player):
    conn.send((str.encode(str(player))))

    reply = [None, None]
    while True:
        try:
            data = conn.recv(2048)
            data_loaded = pickle.loads(data)
            display_message = data_loaded.pop()
            fleets[player] = data_loaded[0]
            missiles[player] = data_loaded[1]

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply[0] = fleets[0]
                    reply[1] = missiles[0]
                else:
                    reply[0] = fleets[1]
                    reply[1] = missiles[1]

                if display_message:
                    # print("Received: ", data)
                    # print("Sending : ", reply)
                    print(f"Player {player+1} positions: ", fleets[player])
                
                if missiles[player] is not None:
                    print(f"Player {player+1} shot a bullet from a ship number {missiles[player]}")
                
            msg = pickle.dumps(reply)
            conn.sendall(msg)

        except:
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
