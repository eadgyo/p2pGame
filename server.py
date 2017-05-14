#!/usr/bin/python3

import socket
import select
import pickle
import threading

from message import *

class Server:
    def __init__(self, port):
        self.host = socket.gethostname()
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.clients = []
        self.input = ''
        self.running = False

    def handleInput(self):
        while self.running:
            self.input = input('')

    def sendMessage(self, client, type, msg):
        client.send(pickle.dumps(Message(type, msg)))

    def receiveMessage(self, msg):
        pass

    def addClient(self, client):
        self.clients.append(client)

    def removeClient(self):
        pass

    def new(self):
        print("Game created. Listening on port {}.".format(self.port))
        self.run()

    def connect(self, ip, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        msg = pickle.loads(client.recv(1024))
        if msg.type == Message.JOIN:
            print(msg.data)
        self.addClient(client)

        self.run()

    def disconnect():
        pass

    def handleNewConnections(self):
        connections, wlist, xlist = select.select([self.socket], [], [], 0.05)

        for connection in connections:
            newclient, addr = connection.accept()
            print("New connection from : {}".format(str(addr)))
            for client in self.clients:
                self.sendMessage(client, Message.JOIN, addr)
            self.sendMessage(newclient, Message.JOIN, 'OK')
            self.addClient(newclient)

    def handleMessages(self):
        clients = []
        try:
            clients, wlist, xlist = select.select(self.clients, [], [], 0.05)
        except select.error:
            pass
        else:
            for client in clients:
                #msg = client.recv(1024).decode('ascii')
                data = client.recv(1024)
                msg = pickle.loads(data).data
                print("Message '{}' from {}".format(msg, str(client.getpeername())))
                if msg == "Close":
                    self.running = False

    def run(self):
        self.running = True
        
        t = threading.Thread(target=self.handleInput)
        t.start()

        while self.running:
            self.handleNewConnections()
            self.handleMessages()

            if self.input != '':
                for client in self.clients:
                    self.sendMessage(client, Message.STRING, self.input)
                self.input = ''

        print("Server closed.")
        for client in self.clients:
            client.close()

        self.socket.close()

