import pygame
from Person import *
import Constants

class Graphics:

    def __init__(self):
        pygame.init()
        pygame.font.init()

    def createWindow(self, width, height):
        self.font = pygame.font.Font(None, Constants.FONT_SIZE)
        self.screen = pygame.display.set_mode((width, height))
        self.clear()


    def clear(self):
        self.screen.fill(Constants.white)

    def flip(self):
        pygame.display.flip()

    def displayScene(self, myPerson, persons):
        # Render all players
        for person in persons:
            if person.state != State.DEAD:
                if person.state == State.ALIVE:
                    radius = Constants.DEFAULT_RADIUS
                else:
                    radius = Constants.FIRING_RADIUS
                pygame.draw.circle(self.screen, Constants.DEFAULT_COLOR, person.getPosInt(), radius, 0)
                pygame.draw.circle(self.screen, person.color, person.getPosInt(), radius, 2)

        # Render person player
        if myPerson.state != State.DEAD:
            pygame.draw.circle(self.screen, Constants.red, myPerson.getPosInt(), 3, 0)


    def drawText(self, text, pos, fc=(255,255,255), bc=(0,0,0)):
        ren = self.font.render(text, True, fc, bc)
        self.screen.blit(ren, pos)

    def displayTopScore(self, owners):
        x = 5
        y = 0
        self.drawText("Scores: ", (x, y), Constants.black, None)
        y += Constants.FONT_SPACING_Y
        x += 2
        for owner in owners:
            self.drawText(owner.name + ": " + str(owner.score), (x, y), Constants.black, None)

    def displayOverlay(self, vel, height):
        x = 5
        y = height - 20

        vel = int(vel * 10) / 10
        self.drawText("Velocity: " + str(vel), (x, y), Constants.black, None)