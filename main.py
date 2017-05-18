#!/usr/bin/python3

from game import *

def main():
    name = input("Name ? ")
    port = int(input("Port number ? "))
    game = Game(name, port)

    b = input("Start new game ? ")

    if len(b) and b.lower()[0] == 'y':
        n = int(input("Number of entities ? "))
        game.new(n)
    else:
        ip = input("Server hostname ? ")
        if ip == '':
            ip = '127.0.0.1'
        port = int(input("Server port number ? "))
        game.connect(ip, port)

if __name__ == "__main__":
    main()

