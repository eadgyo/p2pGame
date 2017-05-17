#!/usr/bin/python3

import pickle

class Message:
    OK              = 1 << 0
    ERROR           = 1 << 1
    CONNECT         = 1 << 2
    DISCONNECT      = 1 << 3
    DISCONNECTED    = 1 << 4
    PORT            = 1 << 5
    ID              = 1 << 6
    STRING          = 1 << 7
    INT             = 1 << 8

    TO_STRING = {
        OK: "OK",
        ERROR: "ERROR",
        CONNECT: "CONNECT",
        DISCONNECT: "DISCONNECT",
        DISCONNECTED: "DISCONNECTED",
        PORT: "PORT",
        ID: "ID",
        STRING: "STRING",
        INT: "INT"
    }

    def __init__(self, id, type, data):
        self.id = id
        self.type = type
        self.data = data

    def __str__(self):
        return "[MESSAGE from {}] {}{}".format(self.id, " | ".join([Message.TO_STRING[k] for k in Message.TO_STRING.keys() if self.type & k]), " -> {}".format(self.data) if self.data else '')

