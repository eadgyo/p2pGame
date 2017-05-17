#!/usr/bin/python3

import socket
import select
import pickle
import threading

from message import *

class Game:
    def __init__(self, port):
        self.running = False

        self.n = 0
        self.id = 0
        self.players = {}
        self.players_socket = {}
        self.players_socket_awaiting = {}

        self.input = ''

        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', self.port))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.listen(5)

    def connect(self, ip, port, new = True):
        print("Connecting to ({}, {})...".format(ip, port))
        player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        player_socket.connect((ip, port))

        if new:
            message = self.receive(player_socket)
            if message.type & Message.OK and message.type & Message.INT:
                n = message.data - 2
                self.n = message.data
                self.id = message.data
                self.players_socket[message.id] = player_socket
                self.notify(player_socket, Message.OK | Message.PORT, self.port)
                while n:
                    player_socket, addr = self.socket.accept()
                    self.notify(player_socket, Message.OK | Message.ID, self.id)
                    message = self.receive(player_socket)
                    if message.type & Message.OK and message.type & Message.INT:
                        self.players_socket[message.id] = player_socket
                    else:
                        return
                    n -= 1
                self.run()
        else:
            self.players_socket[self.n] = player_socket

    def diconnect(self):
        self.notifyAll(Message.OK | Message.DISCONNECT | Message.STRING, "Disconnecting...")
        self.socket.close()
        for s in self.players_socket:
            s.sock.shutdown(socket.SHUT_RDWR)
        while len(self.players_socket):
            pass

        self.running = False

    def new(self):
        print("Game created. Listening on port ", self.port)
        self.n = 1
        self.id = 1
        self.run()

    def run(self):
        self.running = True

        t = threading.Thread(target=self.handleInput)
        t.start()

        while self.running:
            self.handleConnections()
            self.handleMessages()
            self.handleInputs()

    # HANDLER

    def handleInput(self):
        while self.running:
            self.input = input('')

    def handleInputs(self):
        if self.input != '':
            if self.input == "Close":
                self.diconnect()
            else:
                self.notifyAll(Message.OK | Message.STRING, self.input)
                self.input = ''

    def handleConnection(self, connection):
        player_socket, addr = connection.accept()
        self.n += 1
        self.notify(player_socket, Message.OK | Message.INT, self.n)
        self.players_socket_awaiting[self.n] = player_socket

        print("Accepting new connection from", addr)

    def handleConnections(self):
        connections, wlist, xlist = select.select([self.socket], [], [], 0.05)
        for connection in connections:
            self.handleConnection(connection)

    def handleMessage(self, player_socket):
        message = self.receive(player_socket)
        if message.type & Message.OK:
            if message.type & Message.CONNECT:
                (host, port) = message.data
                self.connect(host, port, False)
                self.n += 1
            elif message.type & Message.DISCONNECT:
                pass
            elif message.type & Message.DISCONNECTED:
                pass
            elif message.type & Message.ID:
                self.notify(player_socket, Message.OK | Message.INT, self.id)
            elif message.type & Message.PORT:
                self.notifySome(self.players_socket.values(), Message.OK | Message.CONNECT, (player_socket.getpeername()[0], message.data))
                self.players_socket[message.id] = self.players_socket_awaiting[message.id]
                del self.players_socket_awaiting[message.id]
            #elif message.type & Message.STRING:
            #    print(message)

    def handleMessages(self):
        players_socket = []
        try:
            players_socket, wlist, xlist = select.select(list(self.players_socket.values()) + list(self.players_socket_awaiting.values()), [], [], 0.05)
            for player_socket in players_socket:
                self.handleMessage(player_socket)
        except select.error as e:
            print(e)

    # UTILITY

    def notify(self, player, type, data):
        try:
            player.sendall(pickle.dumps(Message(self.id, type, data)))
        except:
            pass

    def notifySome(self, players, type, data):
        for player in players:
            self.notify(player, type, data)

    def notifyAll(self, type, data):
        self.notifySome(self.players_socket.values(), type, data)
    
    def receive(self, s):
        BUFFER_SIZE = 4096
        data = b''
        while True:
            data += s.recv(BUFFER_SIZE)
            if not data:
                return Message(0, Message.ERROR, '')
            else:
                if data.endswith(b'.'):
                    m = pickle.loads(data)
                    print(m)
                    return m

