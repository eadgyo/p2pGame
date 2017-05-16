#!/usr/bin/python3

import pickle

class Message:
    OK          = 1 << 1
    CONNECT     = 1 << 2
    DISCONNECT  = 1 << 3
    PORT        = 1 << 4
    STRING      = 1 << 5
    INT         = 1 << 6

    def __init__(self, type, data):
        self.type = type
        self.data = data
    
