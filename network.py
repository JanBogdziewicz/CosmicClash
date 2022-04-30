import socket
import pickle
from player import *
from game import *
from thread import *
from mapobjects import *
from config import *


# client send to server data about his player and new objects created by him
class MessageFromClientToServer:
    def __init__(self, player, player_new_missiles):
        self.player = player
        self.player_new_missiles = player_new_missiles

    def unpack(self):
        return self.player, self.player_new_missiles


# server send to client data about another player and all objects on the game map
class MessageFromServerToClient:
    def __init__(self, player, missiles, asteroids):
        self.player = player
        self.missiles = missiles
        self.asteroids = asteroids

    def unpack(self):
        return self.player, self.missiles, self.asteroids


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.address = (self.server, self.port)
        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(8192))
        except socket.error as se:
            print(se)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(8192))
        except socket.error as se:
            print(se)

