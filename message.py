#!/usr/bin/python3

import pickle

class Message:
    OK              = 1 << 0
    ERROR           = 1 << 1
    CONNECT         = 1 << 2
    DISCONNECT      = 1 << 3
    DISCONNECTED    = 1 << 4

    INIT            = 1 << 5
    PORT            = 1 << 6
    ID              = 1 << 7

    MOVE            = 1 << 8
    SHOOT           = 1 << 9
    DEAD            = 1 << 10
    SCORE           = 1 << 11

    STRING          = 1 << 12
    INT             = 1 << 13

    TO_STRING = {
        OK: "OK",
        ERROR: "ERROR",
        CONNECT: "CONNECT",
        DISCONNECT: "DISCONNECT",
        DISCONNECTED: "DISCONNECTED",
        INIT: "INIT",
        PORT: "PORT",
        ID: "ID",
        POS: "POS",
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

