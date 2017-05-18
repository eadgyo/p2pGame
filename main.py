#!/usr/bin/python3

from game import *

def main():
    port = int(input("Port number ? "))
    game = Game(port)

    b = input("Start new game ? ")

    if b == 'y':
        n = int(input("Number of players ? "))
        game.new(n)
    else:
        ip = input("Server hostname ? ")
        if ip == '':
            ip = '127.0.0.1'
        port = int(input("Server port number ? "))
        game.connect(ip, port)
if __name__ == "__main__":
    main()

