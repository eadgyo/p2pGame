import pygame


class Inputs:
    def __init__(self):
        self.NUMBER_KEY = 128
        self.wasPressed = [False]*self.NUMBER_KEY
        self.isDown = [False]*self.NUMBER_KEY
        self.isLeaving = True

    def update(self):
        actionKey = []
        for event in pygame.event.get():

            if event.type == event.KEYDOWN:
                actionKey.append((event.KEYDOWN, event.key))
                self.setKeyDown(event.key, True)
                self.setKeyPressed(event.key, True)

            elif event.type == event.KEYUP:
                actionKey.append((event.KEYDOWN, event.key))
                self.setKeyDown(event.key, False)

            elif event.type == pygame.QUIT:
                actionKey.append((event.quit, None))

        return actionKey

    def setKeyDown(self, keyIndex, keyDown):
        self.isDown[keyIndex] = keyDown

    def getKeyDown(self, keyIndex):
        return self.isDown[keyIndex]

    def clearKeyDown(self, keyIndex):
        self.isDown[keyIndex] = False

    def clearAllKeysDown(self):
        for i in range(0, len(self.isDown)):
            self.isDown[i] = False

    def setKeyPressed(self, keyIndex, keyPressed):
            self.wasPressed[keyIndex] = keyPressed

    def getKeyPressed(self, keyIndex):
        return self.wasPressed[keyIndex]

    def clearAllKeysPressed(self):
        for i in range(0, len(self.isDown)):
            self.wasPressed[i] = False

    def clearKeyPressed(self, keyIndex):
        self.wasPressed[keyIndex] = False