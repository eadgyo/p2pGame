#!/usr/bin/python3

import pickle

class Message:
    NOTHING         = 0

    OK              = 1 << 0
    ERROR           = 1 << 1
    CONNECT         = 1 << 2
    DISCONNECT      = 1 << 3
    DISCONNECTED    = 1 << 4

    INIT            = 1 << 5
    PORT            = 1 << 6
    ID              = 1 << 7
    DONE            = 1 << 8

    MOVE            = 1 << 9
    SHOOT           = 1 << 10
    DEAD            = 1 << 11
    SCORE           = 1 << 12

    STRING          = 1 << 13
    INT             = 1 << 14

    TO_STRING = {
        OK: "OK",
        ERROR: "ERROR",
        CONNECT: "CONNECT",
        DISCONNECT: "DISCONNECT",
        DISCONNECTED: "DISCONNECTED",
        INIT: "INIT",
        PORT: "PORT",
        ID: "ID",
		DONE: "DONE",
        MOVE: "MOVE",
        SHOOT: "SHOOT",
        DEAD: "DEAD",
        SCORE: "SCORE",
        STRING: "STRING",
        INT: "INT"
    }

    def __init__(self, id, type, data):
        self.id = id
        self.type = type
        self.data = data

    def __str__(self):
        return "[MESSAGE from {}] {}{}".format(self.id, " | ".join([Message.TO_STRING[k] for k in Message.TO_STRING.keys() if self.type & k]), " -> {}".format(self.data) if self.data else '')

