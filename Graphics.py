import pygame
from Person import *

class Graphics:

    def __init__(self):
        self.DEFAULT_RADIUS = 8
        self.FIRING_RADIUS = 12
        self.DEFAULT_COLOR = 196, 196, 196
        self.white = 255, 255, 255
        self.black = 0, 0, 0
        self.red = 255, 0, 0

    def createWindow(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clear()


    def clear(self):
        self.screen.fill(self.white)

    def flip(self):
        pygame.display.flip()

    def displayScene(self, myPerson, persons):
        # Render all players
        for person in persons:
            if person.state != State.DEAD:
                if person.state == State.ALIVE:
                    radius = self.DEFAULT_RADIUS
                else:
                    radius = self.FIRING_RADIUS
                pygame.draw.circle(self.screen, self.DEFAULT_COLOR, (person.x, person.y), radius, 0)
                pygame.draw.circle(self.screen, person.color, (person.x, person.y), radius, 2)

        # Render person player
        if myPerson.state != State.DEAD:
            pygame.draw.circle(self.screen, self.red, (myPerson.x, myPerson.y), 3, 0)



