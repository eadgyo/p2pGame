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
        self.input = ''

        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', self.port))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.listen(5)

    def connect(self, ip, port, new = True):
        print("Connecting to ({}, {})...".format(ip, port))
        player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        player.connect((ip, port))
        self.addPlayer(player)

        if new:
            response = pickle.loads(player.recv(1024))

            if response.type & Message.OK and response.type & Message.INT:
                n = response.data
                self.notify(player, Message.OK | Message.PORT, self.port)
                while n:
                    player, addr = self.socket.accept()
                    self.addPlayer(player)
                    n -= 1
                self.run()

    def diconnect(self):
        self.notifyAll(Message.OK | Message.DISCONNECT | Message.STRING, "Disconnecting...")
        self.running = False

    def new(self):
        print("Game created. Listening on port {}.".format(self.port))
        self.run()

    def run(self):
        self.running = True

        t = threading.Thread(target=self.handleInput)
        t.start()

        while self.running:
            self.handleConnections()
            self.handleMessages()

            if self.input != '':
                self.notifyAll(Message.OK | Message.STRING, self.input)
                self.input = ''

    # HANDLER

    def handleInput(self):
        while self.running:
            self.input = input('')

    def handleConnection(self, connection):
        player, addr = connection.accept()
        print("Accepting new connection from,", addr)
        self.notify(player, Message.OK | Message.INT, len(self.players_socket))
        self.addPlayer(player)

    def handleConnections(self):
        connections, wlist, xlist = select.select([self.socket], [], [], 0.05)

        for connection in connections:
            self.handleConnection(connection)

    def handleMessage(self, player):
        message = pickle.loads(player.recv(1024))
        if message.type & Message.OK:
            if message.type & Message.CONNECT:
                (host, port) = message.data
                self.connect(host, port, False)
            elif message.type & Message.PORT:
                self.notifySome(self.players_socket[:-1], Message.OK | Message.CONNECT, (player.getpeername()[0], message.data))
            elif message.type & Message.STRING:
                print("Message : ", message.data)

    def handleMessages(self):
        players = []
        try:
            players, wlist, xlist = select.select(self.players_socket, [], [], 0.05)
        except select.error:
            pass
        else:
            for player in players:
                self.handleMessage(player)

    # UTILITY

    def addPlayer(self, player):
        self.players_socket.append(player)

    def notify(self, player, type, data):
        player.send(pickle.dumps(Message(type, data)))

    def notifySome(self, players, type, data):
        for player in players:
            self.notify(player, type, data)

    def notifyAll(self, type, data):
        self.notifySome(self.players_socket, type, data)


