import socket
import select
import pickle
import threading
import time
import pygame
import random

from constant   import Constant
from input      import Input
from message    import Message
from graphics   import Graphics
from player     import Player
from entity     import Entity

class Game:
    def __init__(self, port):
        self.running = False

        self.pid = 0
        self.pids = []

        self.nbPlayer = 0
        self.players = {}

        self.entities = {}

        self.moves = []
        self.shoot = False
        self.deads = []

        self.input = Input()
        self.graphics = Graphics()
        self.velocity = Constant.VELOCITY

        self.id = 0
        self.port = port

        self.players_socket = {}
        self.players_socket_awaiting = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', self.port))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.listen(5)

    def init(self, name, nbEntity, nbPlayer = 1, pids = None):
        self.id = nbPlayer
        self.players[self.id] = Player(name)

        self.nbPlayer = nbPlayer

        self.pids = pids if pids else list(range(1, nbEntity + 1))
        self.pid = self.pids[random.randrange(len(self.pids))]
        self.pids.remove(self.pid)

    def connect(self, ip, port, name):
        print("Connecting to ({}, {})...".format(ip, port))
        player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        player_socket.connect((ip, port))
        message = self.receive(player_socket)
        if message.type & Message.OK and message.type & Message.INIT:
            (nbPlayer, pids, entities) = message.data
            self.init(name, 0, nbPlayer, pids)
            for (pid, position) in entities:
                self.entities[pid] = self.entity(position.x, position.y)

            n = nbPlayer - 2
            self.players_socket[message.id] = player_socket
            self.notify(player_socket, Message.OK | Message.PORT, self.port)
            while n:
                player_socket, addr = self.socket.accept()
                self.notify(player_socket, Message.OK | Message.ID, None)
                message = self.receive(player_socket)
                if message.type & Message.OK and message.type & Message.ID:
                    self.players_socket[message.id] = player_socket
                else:
                    print("Can't join")
                    self.disconnect()
                    return
                n -= 1
            self.run()

    def connectTo(self, ip, port):
        print("Connecting to ({}, {})...".format(ip, port))
        player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        player_socket.connect((ip, port))
        self.players_socket[self.nbPlayer] = player_socket

    def disconnect(self):
        print("Disconnecting...")

        self.socket.close()

        if self.nbPlayer > 1:
            player_socket = next(iter(self.players_socket.values()))
            data = [(pid, entity.position) for (pid, entity) in self.entities.items()]
            self.notify(player_socket, Message.OK | Message.MOVE, data)
            time.sleep(0.05) # NEEDED : Wait at least one loop from the remote player
            self.notify(player_socket, Message.OK | Message.INIT, self.pids + [self.pid])
            time.sleep(0.05)
            self.notifyAll(Message.OK | Message.DISCONNECT | Message.STRING, "Disconnecting...")
            for s in self.players_socket.values():
                s.shutdown(socket.SHUT_WR)
            while len(self.players_socket):
                self.handleMessages(self.handleDisconnected)

        self.running = False

        print("Disconnected")

    def new(self, name, nbEntity):
        print("Game created")
        print("Listening on port", self.port)

        self.init(name, nbEntity)
        for i in range(1, nbEntity + 1):
            self.entities[i] = self.entity(random.randrange(Constant.WIDTH), random.randrange(Constant.HEIGHT))
        self.run()

    def run(self):
        self.running = True

        self.graphics.createWindow(Constant.WIDTH, Constant.HEIGHT)

        t = time.time()
        while self.running:
            dt, t = self.getDt(t)

            self.handleConnections()
            self.handleMessages(self.handleMessage)
            self.clear()
            self.handleInputs(dt)
            self.update(dt)
            self.sendMessages()
            self.render()

    # NETWORK HANDLER

    def handleConnection(self, connection):
        player_socket, addr = connection.accept()
        self.nbPlayer += 1
        player_pids, self.pids = self.pids[:len(self.pids)//2+1], self.pids[len(self.pids)//2+1:]
        data = (self.nbPlayer, player_pids, [(pid, self.entities[pid].position) for pid in player_pids])
        self.notify(player_socket, Message.OK | Message.INIT, data)
        self.players_socket_awaiting[self.nbPlayer] = player_socket

        print("Accepting new connection from", addr)

    def handleConnections(self):
        connections, wlist, xlist = select.select([self.socket], [], [], 0.05)
        for connection in connections:
            self.handleConnection(connection)

    def handleMessage(self, player_socket):
        message = self.receive(player_socket)
        if message.type & Message.OK:
            if message.type & Message.CONNECT:
                self.nbPlayer += 1
                (host, port) = message.data
                self.connectTo(host, port)
            elif message.type & Message.INIT:
                self.pids.extend(message.data)
            elif message.type & Message.DISCONNECT:
                self.nbPlayer -= 1
                self.notify(player_socket, Message.OK | Message.DISCONNECTED, None)
                player_socket.shutdown(socket.SHUT_RDWR)
                player_socket.close()
                del self.players_socket[message.id]
            elif message.type & Message.ID:
                self.notify(player_socket, Message.OK | Message.ID, None)
            elif message.type & Message.PORT:
                self.notifyAll(Message.OK | Message.CONNECT, (player_socket.getpeername()[0], message.data))
                self.players_socket[message.id] = self.players_socket_awaiting[message.id]
                del self.players_socket_awaiting[message.id]
            elif message.type & Message.MOVE:
                for (pid, position) in message.data:
                    if pid in self.entities:
                        self.entities[pid].position = position
                    else:
                        self.entities[pid] = self.entity(position.x, position.y)

            #elif message.type & Message.STRING:
            #    print(message)

    def handleDisconnected(self, player_socket):
        message = self.receive(player_socket)
        if message.type & Message.OK and message.type & Message.DISCONNECTED:
            player_socket.close()
            del self.players_socket[message.id]

    def handleMessages(self, f):
        players_socket = []
        if len(self.players_socket) + len(self.players_socket_awaiting):
            try:
                players_socket, wlist, xlist = select.select(list(self.players_socket.values()) + list(self.players_socket_awaiting.values()), [], [], 0.05)
                for player_socket in players_socket:
                    f(player_socket)
            except select.error as e:
                #print(e)
                pass

    # GAME HANDLER

    def handleInputs(self, dt):
        # Get keyboard inputs
        actionKeys = self.input.update()

        # Create action
        for (actionType, obj) in actionKeys:
            if actionType == pygame.QUIT:
                self.disconnect()
            elif actionType == pygame.KEYDOWN:
                if obj == pygame.K_ESCAPE:
                    self.disconnect()
                elif obj == pygame.K_SPACE:
                    self.fire()

        # Get player action
        dx = 0
        dy = 0

        if self.input.getKeyDown(pygame.K_LEFT):
            dx = int(-self.velocity * dt)
        if self.input.getKeyDown(pygame.K_RIGHT):
            dx += int(self.velocity * dt)
        if self.input.getKeyDown(pygame.K_UP):
            dy = int(-self.velocity * dt)
        if self.input.getKeyDown(pygame.K_DOWN):
            dy += int(self.velocity * dt)

        if self.input.getKeyDown(pygame.K_w):
            self.velocity = max(self.velocity - 5, 5)
        if self.input.getKeyDown(pygame.K_x):
            self.velocity = min(self.velocity + 5, 80)

        if dx != 0 or dy != 0:
            self.entities[self.pid].move(dx, dy, Constant.WIDTH, Constant.HEIGHT)
            self.moves.append(self.pid)

    # NETWORK UTILITY

    def notify(self, player, type, data):
        try:
            player.sendall(pickle.dumps(Message(self.id, type, data)))
            print("Sending -> ", Message(self.id, type, data))
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

    def sendMessages(self):
        if len(self.moves):
            data = [(pid, self.entities[pid].position) for pid in self.moves]
            self.notifyAll(Message.OK | Message.MOVE, data)

    # GAME UTILITY

    def getDt(self, lastTime):
        t = time.time()
        dt = t - lastTime
        return dt, t

    def entity(self, x, y):
        return Entity(x, y, (random.randrange(256), random.randrange(256), random.randrange(256)))

    def clear(self):
        self.moves.clear()
        self.deads.clear()

    def update(self, dt):
        for pid in self.pids:
            if self.entities[pid].behave(dt, Constant.WIDTH, Constant.HEIGHT):
                self.moves.append(pid)

    def render(self):
        self.graphics.clear()
        self.graphics.renderEntities(self.entities)
        self.graphics.displayTopScore(self.players)
        self.graphics.displayOverlay(Constant.VELOCITY, Constant.HEIGHT)
        self.graphics.flip()

    def fire(self):
        if self.mdata.myPerson.state == State.ALIVE:
            self.mdata.fire(Constants.FIRING_TIME)

