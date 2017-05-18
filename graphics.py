import pygame
import inputbox

from constant import Constant

from Person import *

class Graphics:

    def __init__(self):
        pygame.init()
        pygame.font.init()

    def createWindow(self, width, height):
        self.font = pygame.font.Font(None, Constant.FONT_SIZE)
        self.screen = pygame.display.set_mode((width, height))
        self.clear()

    def ask(self, str):
        return Inputbox.ask(self.screen, str)

    def clear(self):
        self.screen.fill(Constant.white)

    def flip(self):
        pygame.display.flip()

    def renderEntities(self, entities):
        for entity in entities.values():
            pygame.draw.circle(self.screen, entity.color, (entity.position.x, entity.position.y), Constant.DEFAULT_RADIUS, 0)

    def displayScene(self, myPerson, persons):
        # Render all players
        for person in persons:
            if person.state != State.DEAD:
                if person.state == State.ALIVE:
                    radius = Constant.DEFAULT_RADIUS
                else:
                    radius = Constant.FIRING_RADIUS
                pygame.draw.circle(self.screen, Constant.DEFAULT_COLOR, person.getPosInt(), radius, 0)
                pygame.draw.circle(self.screen, person.color, person.getPosInt(), radius, 2)

        # Render person player
        if myPerson.state != State.DEAD:
            pygame.draw.circle(self.screen, Constant.red, myPerson.getPosInt(), 3, 0)

    def drawText(self, text, pos, fc=(255,255,255), bc=(0,0,0)):
        ren = self.font.render(text, True, fc, bc)
        self.screen.blit(ren, pos)

    def displayTopScore(self, owners):
        x = 5
        y = 0
        self.drawText("Scores: ", (x, y), Constant.black, None)
        y += Constant.FONT_SPACING_Y
        x += 2
        for owner in owners:
            self.drawText(owner.name + ": " + str(owner.score), (x, y), Constant.black, None)

    def displayOverlay(self, vel, height):
        x = 5
        y = height - 20

        vel = int(vel * 10) / 10
        self.drawText("Velocity: " + str(vel), (x, y), Constant.black, None)

