from Multiplayer import Multiplayer
from Graphics import Graphics
from Inputs import Inputs
from time import time
import pygame

class Game:
    def __init__(self):
        self.multiplayer = Multiplayer()
        self.graphics = Graphics()
        self.inputs = Inputs()

        self.isGameRunning = False

        self.DEFAULT_WIDTH = 800
        self.DEFAULT_HEIGHT = 600
        self.DT_RUNNING = 0.25

    def start(self):
        self.graphics.createWindow(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)
        self.isGameRunning = True

        t = time()
        while self.isGameRunning:
            dt, t = self.getDt(t)
            self.run(dt)
            self.sleep(dt)

    def sleep(self, t):
        startTime = time()
        while time() - startTime < t:
            time.sleep(10)

    def getDt(self, lastTime):
        t = time()
        dt = t - lastTime
        return dt, t

    def updateMultiplayer(self):
        # Handle networks events
        self.multiplayer.handleNetworksEvents()

        # Multiplayer synchro
        self.multiplayer.handleGameEvents()

    def updateIA(self):
        pass

    def handleInputs(self):
        # Get keyboard inputs
        actionKeys = self.inputs.update()

        # Create action
        for (actionType, obj) in actionKeys:
            if actionType == pygame.QUIT:
                self.isGameRunning = False

        # Save action
        pass

    def display(self):
        pass

    def update(self, dt):
        self.updateMultiplayer()
        self.updateIA(dt)

    def run(self, dt):
        self.update(self, dt)
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
"""