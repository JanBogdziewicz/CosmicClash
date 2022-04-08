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


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


fleets = [ [], [] ]

def threaded_client(conn, player):
    conn.send((str.encode(str(player))))

    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            fleets[player] = pickle.loads(data)

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = fleets[0]
                else:
                    reply = fleets[1]

                print("Received: ", data)
                print("Sending : ", reply)

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
