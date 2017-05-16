from Person import *
from random import randint
class Firing:
    def __init__(self, person, t):
        self.person = person
        self.time = t

class MData:
    def __init__(self):
        self.myPerson = None

        # Owner computer
        self.owners = []

        # Link persons to his owner
        self.persons = []

        # Multiplayer events
        self.event = []

        # Keep firing persons for n time
        self.firingPersons = []

    def createPersons(self, startId, number, xmax, ymax):
        persons = []
        id = startId
        for i in range(number):
            color = randint(0,255), randint(0,255), randint(0,255)
            persons.append(Person(id, randint(0, xmax), randint(0, ymax), color))
            id += 1
        return persons

    def move(self, dx, dy, person=None):
        if person == None:
            person = self.myPerson
        person.move(dx, dy)
        self.event.append(person.moveEvent())

    def fire(self, firingTime, person=None):
        if person == None:
            person = self.myPerson
        person.state = State.FIRING
        self.firingPersons.append(Firing(person, firingTime))
        self.event.append(person.stateEvent())

    def update(self, dt):
        for firingPerson in self.firingPersons:
            firingPerson.time -= dt
            if firingPerson.time < 0:
                self.firingPersons.remove(firingPerson)
                if firingPerson.person.state == State.FIRING:
                    firingPerson.person.state = State.ALIVE
                    self.event.append(firingPerson.person.stateEvent())

    # def handlePersons
    # Assign persons to owner