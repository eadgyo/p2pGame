from Multiplayer import Multiplayer
from Graphics import Graphics
from Inputs import Inputs
from MData import MData
import time
import pygame

class Game:
    def __init__(self):
        self.multiplayer = Multiplayer()
        self.mdata = MData()
        self.graphics = Graphics()
        self.inputs = Inputs()

        self.isGameRunning = False

        self.WIDTH = 800
        self.HEIGHT = 600
        self.DT_RUNNING = 13
        self.MOVE = 4
        self.FIRING_TIME = 0.1

        self.test()

    def test(self):
        persons = self.mdata.createPersons(0, 10, self.WIDTH, self.HEIGHT)
        self.mdata.persons += persons
        self.mdata.myPerson = self.mdata.persons[0]

    def start(self):
        self.graphics.createWindow(self.WIDTH, self.HEIGHT)
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
        pass

    def handleInputs(self):
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
                    self.mdata.fire(self.FIRING_TIME)

        # Get player action
        dx = 0
        dy = 0

        if self.inputs.getKeyDown(pygame.K_LEFT):
            dx = -self.MOVE
        if self.inputs.getKeyDown(pygame.K_RIGHT):
            dx += self.MOVE
        if self.inputs.getKeyDown(pygame.K_UP):
            dy = -self.MOVE
        if self.inputs.getKeyDown(pygame.K_DOWN):
            dy += self.MOVE

        if dx != 0 or dy != 0:
            self.mdata.move(dx, dy)

        pass

    def display(self):
        self.graphics.clear()
        self.graphics.displayScene(self.mdata.myPerson, self.mdata.persons)
        self.graphics.flip()

    def update(self, dt):
        self.updateMultiplayer(dt)
        self.updateIA(dt)

    def run(self, dt):
        self.update(dt)
        self.display()
        self.handleInputs()



"""
// Definition du jeu:
Sur une carte, il y a un ensemble de personnes.


// Départ
Création des personnages

// A chaque connexion
On prend une personne libre et on l'associe à un joueur

// Pour un temps donné
// A la fin on calcule le score
// Affichage de la liste de joueurs

// Creation des joueurs


Comment gérer l'ensemble des IA?


Gère un ensemble de personnes par PC

On associe pour chaque personne des Personnes à gérer
Le programme est gérer par un sous programme

C'est cependant peu sécurisé, puisque la personne peut sur sa machine savoir quels personnes il gère.
Mais peu importe




Personne:
x, y
état du joueur

Partie:
MonjoueurId
Ensemble des personnes

GestionDesPersonnes
ensemble de personnes gérer
Qui gère tel personne (pour la répartition)

Engine
Demande de connexion (start game)

Tant que la partie n'est pas fini
Tant le temps n'est pas fini
GérerMulti // Disparition/Apparition d'un nouveau joueur.
SynchronisationMultijoueur // Gestion des actions exterieur,
GérerPersonnes // Gestion de l'IA
GérerInterfaces // Gérer les interfaces clavier
GestionAction // Gestion des action de l'interface
Affichage // Affichage du jeu
Afficher le scores


Gestion des limites
Gestion de l'IA
Gestion des collisions/tirs
Changement de joueur lorsqu'une personne meurt
"""