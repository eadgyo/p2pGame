#!/usr/bin/python3

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def incx(self):
        self.x += 1

    def incy(self):
        self.y += 1

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

