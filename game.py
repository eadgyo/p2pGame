#!/usr/bin/python3

import socket
import select
import pickle
import threading

from message import *

class Game:
    def __init__(self, port):
        self.running = False
        #self.players = []
        self.players_socket = []
        self.input = ""

        self.host = socket.gethostname()
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

    def connect(self, ip, port):
        player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        player.connect((ip, port))
        response = pickle.loads(client.recv(1024))

        if response.type & Message.OK:
            if response.type & Message.STRING:
                print(response.data)

            self.addPlayer(player)
            self.run()

    def diconnect(self):
        self.notifyAll(Message.DISCONNECT | Message.STRING, "Disconnecting...")
        self.running = False

    def new(self):
        print("Game created. Listening on port {}.".format(self.port))
        self.run()

    def run(self):
        self.running = True

        t = threading.Thread(target=self.handleInput)
        t.start()

        while self.running:
            pass

    # HANDLER

    def handleInput(self):
        while self.running:
            self.input = input('')

    def addPlayer(self, host, port):
        player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        player.connect((host, port))
        response = pickle.loads(client.recv(1024))

    def handleConnection(self, connection):
        newPlayer, addr = connection.accept()
        self.notifyAll(Message.CONNECT, addr)
        self.sendMessage(newPlayer, Message.JOIN, 'Connected')
        self.addPlayer(newPlayer)

    def handleConnections(self):
        connections, wlist, xlist = select.select([self.socket], [], [], 0.05)

        for connection in connections:
            self.handleConnection(connection)

    def handleMessage(self, message):
        if message.type & Message.CONNECT:
            pass
        elseif message.type & Message.DISCONNECT:
            pass
        else:
            print("Error : Wrong message type")

    def handleMessages(self):
        players = []
        try:
            players, wlist, xlist = select.select(self.players, [], [], 0.05)
        except select.error:
            pass
        else:
            for player in players:
                self.handleMessage(pickle.loads(player.recv(1024)))

    # UTILITY

    def addPlayer(self, player):
        self.players_socket.append(player)

    def notify(self, player, type, data):
        player.send(pickle.dumps(Message(type, data)))

    def notifyAll(self, type, data):
        for player in self.players_socket:
            self.notify(player, data)

