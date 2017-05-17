from enum import Enum
import math
import Constants

class State(Enum):
    ALIVE = 1
    DEAD = 2
    FIRING = 3

class Person:
    def __init__(self, id, x=0, y=0, color=(255,255,255), state=State.ALIVE):
        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.state = state
        self.owner = None
        self.behavior = None

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def moveTo(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def limitMove(self, maxX, maxY):
        if self.x < 0:
            self.x = 0
        elif self.x > maxX:
            self.x = maxX
        if self.y < 0:
            self.y = 0
        elif self.y > maxY:
            self.y = maxY

    def moveEvent(self):
        return "person:{id=" + str(self.id) + ",x=" + str(self.x) + ",y=" + str(self.y) + "}"

    def stateEvent(self):
        return "person:{id=" + str(self.id) + ",state=" + str(self.state) + "}"

    def isColliding(self, otherPerson, r1, r2):
        distance = math.sqrt(pow(otherPerson.x - self.x, 2) + pow(otherPerson.y - self.y, 2))
        return distance < r1 + r2

    def behave(self, dt):
        return self.behavior.behave(dt, (self.x, self.y), Constants.WIDTH, Constants.HEIGHT)

    def getPosInt(self):
        return (int(self.x), int(self.y))
