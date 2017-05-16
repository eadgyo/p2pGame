import pygame

class Graphics:

    def __init__(self):
        self.white = 255, 255, 255
        self.black = 0, 0, 0

    def createWindow(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(self.white)
        pygame.display.flip()

