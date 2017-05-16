import Multiplayer
class game:
    def __init__(self):
        self.multiplayer = Multiplayer()

    def init(self):
        pass

    def updateMultiplayer(self):
        # Handle networks events
        self.multiplayer.handlNetworksEvents()

        # Multiplayer synchro
        self.multiplayer.handleGameEvents()

    def updateIA(self):
        pass

    def updateInputs(self):
        # Get keyboard inputs

        # Create action

        # Save action
        pass

    def update(self, dt):
        self.updateMultiplayer()
        self.display()
        self.updateIA()
        self.updateInputs()
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