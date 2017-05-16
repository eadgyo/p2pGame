#!/usr/bin/python3

import server
from game import *

"""
def main():
    port = int(input("Port number ? "))
    game = server.Server(port)

    b = input("Start new game ? ")
    
    if b == "y":
        game.new()
    else:
        ip = input("Server hostname ? ")
        if ip == "":
            ip = game.host
        port = int(input("Server port number ? "))
        game.connect(ip, port)
"""

def main():
    port = int(input("Port number ? "))
    game = Game(port)

    b = input("Start new game ? ")
    
    if b == 'y':
        game.new()
    else:
        ip = input("Server hostname ? ")
        if ip == '':
            ip = '127.0.0.1'
        port = int(input("Server port number ? "))
        game.connect(ip, port)
if __name__ == "__main__":
    main()
