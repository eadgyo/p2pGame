from random import randint
import math
import Constants

class Behavior:
    def __init__(self):
        self.lastMoveT = 0.0

        self.moveT = 0.0
        self.moveDuration = 0.0

        self.start = (0, 0)
        self.destination = (0, 0)

    def behave(self, dt, pos, maxX, maxY):
        return (False, (0,0))

class BehaviorRNG(Behavior):
    def __init__(self):
        Behavior.__init__(self)
        self.type = type

    def behave(self, dt, pos, maxX, maxY):

        # If person is moving
        if self.moveT < self.moveDuration:
            return (True, self.move(dt))
        elif self.canIStartMoving(pos, maxX, maxY):
            return (False, (0,0))

        self.lastMoveT += dt
        return (False, (0,0))

    def move(self, dt):
        self.moveT = min(self.moveT + dt, self.moveDuration)

        # Compute corresponding location
        vec = (self.destination[0] - self.start[0], self.destination[1] - self.start[1])
        perc = self.moveT / self.moveDuration
        pos = (int(self.start[0] + vec[0] * perc), int(self.start[1] + vec[1] * perc))
        return pos

    def canIStartMoving(self, pos, maxX, maxY):
        startMoving = randint(0, int(Constants.FACT_BEHAVE_RNG / (self.lastMoveT + 1))) == 0

        if startMoving:
            self.lastMoveT = 0
            self.start = pos
            self.moveT = 0
            self.moveDuration = randint(Constants.DURATION_BEHAVE[0], Constants.DURATION_BEHAVE[1])
            self.vec = (randint(0, 2) - 1, randint(0, 2) - 1)
            if self.vec == (0, 0):
                a = randint(0, 3)
                if a == 0:
                    self.vec = (1, 0)
                elif a == 1:
                    self.vec = (0, 1)
                elif a == 2:
                    self.vec = (-1, 0)
                elif a == 3:
                    self.vec = (0, -1)
            self.destination = (int(self.start[0] + self.vec[0] * Constants.VEL * self.moveDuration),
                                int(self.start[1] + self.vec[1] * Constants.VEL * self.moveDuration))

        return startMoving