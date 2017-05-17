from Person import *
import Constants
from random import randint
class Firing:
    def __init__(self, person, t):
        self.person = person
        self.time = t

class MData:
    def __init__(self, maxX, maxY):
        self.myPerson = None
        self.me = None

        # Owner computer
        self.owners = []

        # Link persons to his owner
        self.persons = []

        # Multiplayer events
        self.event = []

        # Keep firing persons for n time
        self.firingPersons = []

        self.maxX = maxX
        self.maxY = maxY

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
        person.limitMove(self.maxX, self.maxY)
        self.event.append(person.moveEvent())

    def moveTo(self, pos, person=None):
        if person == None:
            person = self.myPerson
        person.moveTo(pos)
        person.limitMove(self.maxX, self.maxY)
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

        collisions = self.detectCollisions(dt)
        for collision in collisions:
            collision[1].state = State.DEAD
            self.event.append(collision[1].stateEvent())

    def detectCollisions(self, dt):
        colliding = []
        for firing in self.firingPersons:
            person = firing.person
            if person.state == State.FIRING:
                for other in self.persons:
                    if person != other and person.state != State.DEAD:
                        if person.state == State.ALIVE:
                            r2 = Constants.DEFAULT_RADIUS
                        else:
                            r2 = Constants.FIRING_RADIUS
                        if person.isColliding(other, Constants.FIRING_RADIUS, r2):
                            colliding.append((person, other))

        return colliding

    def getPersonsOwned(self):
        personsOwned = {}
        for person in self.persons:
            if person.owner in personsOwned:
                personsOwned[person.owner].append(person)
            else:
                personsOwned[person.owner] = [person]
        return personsOwned

    def handlePersons(self, dt):
        persons = self.getPersonsOwned()
        myPersons = persons[self.me]
        for person in myPersons:
            (isMoving, pos) = person.behave(dt)
            if isMoving:
                self.moveTo(pos, person)


    # def handlePersons
    # Assign persons to owner