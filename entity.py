import random
import math

from constant import Constant
from position import Position

class Entity:
    def __init__(self, x, y, color):
        self.position = Position(x, y)
        self.color = color

        self.lastMoveT = 0.0

        self.moveT = 0.0
        self.moveDuration = 0.0

        self.start = Position(0, 0)
        self.destination = Position(0, 0)

    def move(self, dx, dy, maxX, maxY):
        self.position.x += dx
        self.position.y += dy
        self.limit(maxX, maxY)

    def moveTo(self, position, maxX, maxY):
        self.position = position
        self.limit(maxX, maxY)

    def limit(self, maxX, maxY):
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x > maxX:
            self.position.x = maxX
        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y > maxY:
            self.position.y = maxY

    def behave(self, dt, maxX, maxY):
        self.moveT = min(self.moveT + dt, self.moveDuration)

        if self.moveT < self.moveDuration:
            vec = Position(self.destination.x - self.start.x, self.destination.y - self.start.y)
            perc = self.moveT / self.moveDuration
            self.moveTo(Position(int(self.start.x + vec.x * perc), int(self.start.y + vec.y * perc)), maxX, maxY)
            return True

        if self.startToMove(maxX, maxY):
            return False

        self.lastMoveT += dt
        return False

    def startToMove(self,maxX, maxY):
        startMoving = random.randint(0, int(Constant.FACT_BEHAVE_RNG / (self.lastMoveT + 1))) == 0

        if startMoving:
            self.lastMoveT = 0
            self.start = self.position
            self.moveT = 0
            self.moveDuration = random.randint(Constant.DURATION_BEHAVE[0], Constant.DURATION_BEHAVE[1])
            self.vec = Position(random.randint(0, 2) - 1, random.randint(0, 2) - 1)
            if self.vec == Position(0, 0):
                a = random.randint(0, 3)
                if a == 0:
                    self.vec = Position(1, 0)
                elif a == 1:
                    self.vec = Position(0, 1)
                elif a == 2:
                    self.vec = Position(-1, 0)
                elif a == 3:
                    self.vec = Position(0, -1)
            self.destination = Position(int(self.start.x + self.vec.x * Constant.VELOCITY * self.moveDuration), int(self.start.y + self.vec.y * Constant.VELOCITY * self.moveDuration))

        return startMoving

    def collide(self, entity, r1, r2):
        return math.sqrt(pow(entity.position.x - self.position.x, 2) + pow(entity.position.y - self.position.y, 2)) < r1 + r2

