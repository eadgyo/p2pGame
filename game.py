#!/usr/bin/python3

# NETWORK
import socket
import select
import pickle
import threading

from message import *

# GAME
import time
import pygame

import constant

from Graphics import Graphics
from Inputs import Inputs
from MData import MData
from IA import *
from Owner import Owner
from Person import *

class Game:
    def __init__(self, name, port):
        self.running = False

        self.mdata = MData(Constants.WIDTH, Constants.HEIGHT)
        self.mdata.me = Owner(name)
        self.mdata.owners.append(self.mdata.me)
        self.graphics = Graphics()
        self.inputs = Inputs()
        self.vel = Constants.VEL
        persons = self.mdata.createPersons(0, 60, Constants.WIDTH, Constants.HEIGHT)
        self.mdata.persons += persons
        self.mdata.myPerson = self.mdata.persons[0]

        # Assign person to me
        for i in range(len(persons)):
            persons[i].behavior = BehaviorRNG()
            persons[i].owner = self.mdata.me

        self.mdata.myPerson.behavior = Behavior()

        self.n = 0
        self.id = 0
        self.players = {}
        self.players_socket = {}
        self.players_socket_awaiting = {}

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
                    self.notify(player_socket, Message.OK | Message.ID, None)
                    message = self.receive(player_socket)
                    if message.type & Message.OK and message.type & Message.INT:
                        self.players_socket[message.id] = player_socket
                    else:
                        return
                    n -= 1
                self.run()
        else:
            self.players_socket[self.n] = player_socket

    def disconnect(self):
        self.socket.close()
        self.notifyAll(Message.OK | Message.DISCONNECT | Message.STRING, "Disconnecting...")
        for s in self.players_socket.values():
            s.shutdown(socket.SHUT_WR)
        while len(self.players_socket):
            self.handleMessages(self.handleDisconnected)

        self.running = False

    def new(self):
        print("Game created. Listening on port ", self.port)
        self.n = 1
        self.id = 1
        self.run()

    def run(self):
        self.running = True
        #t = threading.Thread(target=self.handleInput)
        #t.start()

        self.graphics.createWindow(Constants.WIDTH, Constants.HEIGHT)

        t = time.time()
        while self.running:
            dt, t = self.getDt(t)

            self.mdata.update(dt)
            self.updateIA(dt)
            self.mdata.event.clear()
            self.display()
            self.handleInputs(dt)

            self.handleConnections()
            self.handleMessages(self.handleMessage)
            #self.handleInputs()

        #t.join()

    # NETWORK HANDLER

    def handleInput(self):
        while self.running:
            self.input = input('')

    def handleInputs(self):
        if self.input != '':
            if self.input == "Close":
                self.disconnect()
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
                self.n += 1
                (host, port) = message.data
                self.connect(host, port, False)
            elif message.type & Message.DISCONNECT:
                self.notify(player_socket, Message.OK | Message.DISCONNECTED, None)
                player_socket.shutdown(socket.SHUT_RDWR)
                player_socket.close()
                del self.players_socket[message.id]
            elif message.type & Message.ID:
                self.notify(player_socket, Message.OK | Message.INT, self.id)
            elif message.type & Message.PORT:
                self.notifySome(self.players_socket.values(), Message.OK | Message.CONNECT, (player_socket.getpeername()[0], message.data))
                self.players_socket[message.id] = self.players_socket_awaiting[message.id]
                del self.players_socket_awaiting[message.id]
            #elif message.type & Message.STRING:
            #    print(message)

    def handleDisconnected(self, player_socket):
        message = self.receive(player_socket)
        if message.type & Message.OK and message.type & Message.DISCONNECTED:
            player_socket.close()
            del self.players_socket[message.id]

    def handleMessages(self, f):
        players_socket = []
        try:
            players_socket, wlist, xlist = select.select(list(self.players_socket.values()) + list(self.players_socket_awaiting.values()), [], [], 0.05)
            for player_socket in players_socket:
                f(player_socket)
        except select.error as e:
            print(e)

    # GAME HANDLER

    def handleInputs(self, dt):
        # Get keyboard inputs
        actionKeys = self.inputs.update()

        # Create action
        for (actionType, obj) in actionKeys:
            if actionType == pygame.QUIT:
                self.isGameRunning = False
            elif actionType == pygame.KEYDOWN:
                if obj == pygame.K_ESCAPE:
                    self.isGameRunning = False
                elif obj == pygame.K_SPACE:
                    self.fire()

        # Get player action
        self.updatePos(dt)

    # NETWORK UTILITY

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
                return Message(0, Message.ERROR, None)
            else:
                if data.endswith(b'.'):
                    m = pickle.loads(data)
                    print(m)
                    return m

    # GAME UTILITY

    def getDt(self, lastTime):
        t = time.time()
        dt = t - lastTime
        return dt, t

    def display(self):
        self.graphics.clear()
        self.graphics.displayScene(self.mdata.myPerson, self.mdata.persons)
        self.graphics.displayTopScore(self.mdata.owners)
        self.graphics.displayOverlay(self.vel, Constants.HEIGHT)
        self.graphics.flip()

    def updatePos(self, dt):
        dx = 0
        dy = 0

        if self.inputs.getKeyDown(pygame.K_LEFT):
            dx = -self.vel * dt
        if self.inputs.getKeyDown(pygame.K_RIGHT):
            dx += self.vel * dt
        if self.inputs.getKeyDown(pygame.K_UP):
            dy = -self.vel * dt
        if self.inputs.getKeyDown(pygame.K_DOWN):
            dy += self.vel * dt

        if self.inputs.getKeyDown(pygame.K_w):
            self.vel = max(self.vel - 5, 5)
        if self.inputs.getKeyDown(pygame.K_x):
            self.vel = min(self.vel + 5, 80)

        if dx != 0 or dy != 0:
            self.mdata.move(dx, dy)

    def fire(self):
        if self.mdata.myPerson.state == State.ALIVE:
            self.mdata.fire(Constants.FIRING_TIME)

    def updateIA(self, dt):
        self.mdata.handlePersons(dt)

