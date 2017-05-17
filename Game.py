from Multiplayer import Multiplayer
from Graphics import Graphics
from Inputs import Inputs
from MData import MData
from IA import *
from Owner import Owner
from Person import *
import time
import pygame
import Constants

class Game:
    def __init__(self):

        self.multiplayer = Multiplayer()
        self.mdata = MData(Constants.WIDTH, Constants.HEIGHT)
        self.graphics = Graphics()
        self.inputs = Inputs()
        self.vel = Constants.VEL

        self.isGameRunning = False

    def solo(self):
        self.mdata.me = Owner("Jacky")
        self.mdata.owners.append(self.mdata.me)

        persons = self.mdata.createPersons(0, 2, Constants.WIDTH, Constants.HEIGHT)
        self.mdata.persons += persons
        self.mdata.myPerson = self.mdata.persons[0]

        # Assign person to me
        for i in range(len(persons)):
            persons[i].behavior = BehaviorRNG()
            persons[i].owner = self.mdata.me

        self.mdata.myPerson.behavior = Behavior()

    def start(self):
        self.graphics.createWindow(Constants.WIDTH, Constants.HEIGHT)
        self.isGameRunning = True

        t = time.time()
        while self.isGameRunning:
            dt, t = self.getDt(t)
            self.run(dt)
            self.sleepTo(t + dt)

    def sleepTo(self, t):
        while t - time.time() > 0:
            pass
            #time.sleep(0.001)

    def getDt(self, lastTime):
        t = time.time()
        dt = t - lastTime
        return dt, t

    def updateMultiplayer(self, dt):
        self.mdata.update(dt)

        # Handle networks events
        self.multiplayer.handleNetworksEvents()

        # Multiplayer synchro
        self.multiplayer.handleGameEvents()

    def updateIA(self, dt):
        self.mdata.handlePersons(dt)

    def fire(self):
        if self.mdata.myPerson.state == State.ALIVE:
            self.mdata.fire(Constants.FIRING_TIME)

    def updatePos(self, dt):
        dx = 0
        dy = 0

        if self.inputs.getKeyDown(pygame.K_LEFT):
            dx = -self.vel * dt
        if self.inputs.getKeyDown(pygame.K_RIGHT):
            dx += self.vel * dt
        if self.inputs.getKeyDown(pygame.K_UP):
            dy = -self.vel * dt
        if self.inputs.getKeyDown(pygame.K_DOWN):
            dy += self.vel * dt

        if self.inputs.getKeyDown(pygame.K_w):
            self.vel = max(self.vel - 5, 5)
        if self.inputs.getKeyDown(pygame.K_x):
            self.vel = min(self.vel + 5, 80)

        if dx != 0 or dy != 0:
            self.mdata.move(dx, dy)

    def handleInputs(self, dt):
        # Get keyboard inputs
        actionKeys = self.inputs.update()

        # Create action
        for (actionType, obj) in actionKeys:
            if actionType == pygame.QUIT:
                self.isGameRunning = False
            elif actionType == pygame.KEYDOWN:
                if obj == pygame.K_ESCAPE:
                    self.isGameRunning = False
                elif obj == pygame.K_SPACE:
                    self.fire()

        # Get player action
        self.updatePos(dt)


    def display(self):
        self.graphics.clear()
        self.graphics.displayScene(self.mdata.myPerson, self.mdata.persons)
        self.graphics.displayTopScore(self.mdata.owners)
        self.graphics.displayOverlay(self.vel, Constants.HEIGHT)
        self.graphics.flip()

    def update(self, dt):
        self.updateMultiplayer(dt)
        self.updateIA(dt)

    def run(self, dt):
        self.update(dt)
        self.display()
        self.handleInputs(dt)
