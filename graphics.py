import pygame
import inputbox

from constant import Constant

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

    def renderEntities(self, entities, me, fire, shoots):
        for pid, entity in entities.items():
            if (pid == me and fire) or pid in shoots:
                radius = Constant.FIRING_RADIUS
            else:
                radius = Constant.DEFAULT_RADIUS
            pygame.draw.circle(self.screen, Constant.DEFAULT_COLOR, (entity.position.x, entity.position.y), radius, 0)
            pygame.draw.circle(self.screen, entity.color, (entity.position.x, entity.position.y), radius, 2)

        p = entities[me].position
        pygame.draw.circle(self.screen, Constant.red, (p.x, p.y), 3, 0)

    def drawText(self, text, pos, fc=(255,255,255), bc=(0,0,0)):
        ren = self.font.render(text, True, fc, bc)
        self.screen.blit(ren, pos)

    def displayTopScore(self, player):
        x = 5
        y = 0
        self.drawText("Scores: ", (x, y), Constant.black, None)
        y += Constant.FONT_SPACING_Y
        x += 2
        for player in player.values():
            self.drawText(player.name + " : " + str(player.score), (x, y), Constant.black, None)

    def displayOverlay(self, vel, height):
        x = 5
        y = height - 20

        vel = int(vel * 10) / 10
        self.drawText("Velocity: " + str(vel), (x, y), Constant.black, None)

