from enum import Enum
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

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def moveEvent(self):
        return "person:{id=" + str(self.id) + ",x=" + str(self.x) + ",y=" + str(self.y) + "}"

    def stateEvent(self):
        return "person:{id=" + str(self.id) + ",state=" + str(self.state) + "}"