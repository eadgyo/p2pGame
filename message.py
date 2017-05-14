#!/usr/bin/python3

import pickle

class Message:
    OK          = 0 << 1
    ERROR       = 0 << 2
    CONNECT     = 0 << 3
    DISCONNECT  = 0 << 4
    STRING      = 0 << 5

    def __init__(self, type, data):
        self.type = type
        self.data = data
    
