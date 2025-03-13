import os
import pygame
from enum import Enum

"""
J'ai décidé de combiner sokoban et sokoban_model pour n'avoir qu'un fichier
"""

class Symbol(Enum):
    """
    Symboles utilisés pour représenter chaque élément dans le niveau
    • Utilisation d'une énumération pour éviter les erreurs de frappe et standardiser 
      les symboles à travers tout le code
    • Ces symboles correspondent aux caractères utilisés dans les fichiers de niveau .xsb
    """
    BOX = "$"
    BOX_ON_GOAL = "*"
    PLAYER = "@"
    PLAYER_ON_GOAL = "+"
    GOAL = "."
    WALL = "#"
    FLOOR = "-"


class MoveResponse(Enum):
    """
    Messages de retour pour les tentatives de mouvement
    • Permet de communiquer clairement la raison d'un échec de mouvement
    • Sépare la logique du jeu de l'affichage des messages d'erreur
    """
    INVALID_WALL = "can't push walls"
    INVALID_BOX = "can't push this box"
    VALID = "valid"


class SokobanModel:
    def __init__(self, level_data):
        """
        • Utilise des ensembles (sets) pour les éléments du jeu plutôt que d'utiliser
          une seule matrice pour représenter le plateau de jeu
        • Cela simplifie la logique de déplacement et la détection des collisions
        • Réduit la complexité lors de la gestion des cases qui contiennent à la fois
          un objectif et un autre élément (joueur ou boîte)
        """
        self.walls = set()
        self.boxes = set()
        self.goals = set()

        self.size = [0, 0]
        if level_data and len(level_data) > 0:
            # Vérification de la présence de la méthode strip() pour gérer différents types d'entrées
            # (fichiers texte ou listes de chaînes)
            if hasattr(level_data[0], 'strip'):
                self.size = [len(level_data[0].strip()), len(level_data)]
            else:
                self.size = [len(level_data[0]), len(level_data)]

        # Parcourt chaque caractère du niveau pour extraire la position des éléments
        # Utilise le pattern matching (match/case) pour une meilleure lisibilité
        for y, row in enumerate(level_data):
            row_str = row.strip() if hasattr(row, 'strip') else row
            for x, symbol in enumerate(row_str):
                pos = (x, y)
                match symbol:
                    case Symbol.BOX.value:
                        self.boxes.add(pos)
                    case Symbol.BOX_ON_GOAL.value:
                        # Une boîte sur un objectif est représentée en ajoutant la position 
                        # à la fois dans l'ensemble des boîtes et dans celui des objectifs
                        self.boxes.add(pos)
                        self.goals.add(pos)
                    case Symbol.PLAYER.value:
                        self.player = pos
                    case Symbol.PLAYER_ON_GOAL.value:
                        self.player = pos
                        self.goals.add(pos)
                    case Symbol.GOAL.value:
                        self.goals.add(pos)
                    case Symbol.WALL.value:
                        self.walls.add(pos)
                    # Les cases vides (sol) ne sont pas stockées pour économiser de la mémoire

    def is_empty(self, x, y):
        """
        • Méthode auxiliaire pour vérifier si une case est vide
        • Simplifie les vérifications dans la méthode de déplacement
        • Plutôt que de vérifier ce qu'une case contient, on vérifie ce qu'elle ne contient pas
        """
        pos = (x, y)
        if pos in self.walls:
            return False
        if pos in self.boxes:
            return False
        return True

    def move(self, dx, dy):
        """
        • Implémente les règles de déplacement de Sokoban:
          1. Le joueur peut se déplacer dans un espace vide
          2. Le joueur peut pousser une boîte si l'espace derrière est vide
          3. Le joueur ne peut pas traverser les murs ou pousser des boîtes bloquées
        • Retourne un type de réponse plutôt qu'un simple booléen pour indiquer la cause 
          d'un échec de mouvement
        """
        (x, y) = self.player
        (nx, ny) = (x + dx, y + dy)  # nx, ny sont où le joueur essaie d'aller
        if self.is_empty(nx, ny):
            # Cas 1: Se déplacer vers une case vide
            self.player = (nx, ny)
            return MoveResponse.VALID
        elif (nx, ny) in self.boxes:
            # Cas 2: Le joueur tente de pousser une boîte
            # nnx, nny sont où la boîte essaie d'aller
            (nnx, nny) = (nx+dx, ny+dy)
            if self.is_empty(nnx, nny):
                # La boîte peut être poussée
                self.boxes.remove((nx, ny))
                self.boxes.add((nnx, nny))
                self.player = (nx, ny)
                return MoveResponse.VALID
            else:
                # La boîte est bloquée par un mur ou une autre boîte
                return MoveResponse.INVALID_BOX
        else:
            # Cas 3: Le joueur tente de traverser un mur
            return MoveResponse.INVALID_WALL

    def width(self):
        """
        • Accès au premier élément du tableau size pour faciliter la lisibilité du code
        • Encapsule l'accès aux données internes
        """
        return self.size[0]

    def height(self):
        """
        • Accès au second élément du tableau size pour faciliter la lisibilité du code
        • Encapsule l'accès aux données internes
        """
        return self.size[1]

    def symbol(self, x, y):
        """
        • Convertit les données internes en symboles d'affichage
        • Ordre de vérification important: d'abord les objectifs car ils peuvent 
          contenir d'autres éléments
        • Encapsule la logique d'affichage pour maintenir la séparation entre 
          données et représentation
        """
        pos = (x, y)
        if pos in self.goals:
            if pos in self.boxes:
                return Symbol.BOX_ON_GOAL
            if pos == self.player:
                return Symbol.PLAYER_ON_GOAL
            return Symbol.GOAL
        if pos in self.boxes:
            return Symbol.BOX
        if pos == self.player:
            return Symbol.PLAYER
        if pos in self.walls:
            return Symbol.WALL
        return Symbol.FLOOR
        
    def is_level_complete(self):
        """
        • Vérifie si le niveau est terminé en s'assurant que toutes les boîtes 
          sont sur des objectifs
        • Implémente deux approches équivalentes pour une meilleure robustesse
        • Évite l'itération sur tous les emplacements du plateau en utilisant les ensembles
        """
        # Approche 1: Vérifier qu'il n'y a pas de boîtes en dehors des objectifs
        for box_pos in self.boxes:
            if box_pos not in self.goals:
                return False
        
        # Approche 2: Vérifier que toutes les boîtes sont sur des objectifs
        # La vérification len(self.boxes) > 0 évite les faux positifs si aucune boîte n'existe
        return len(self.boxes) > 0 and all(box_pos in self.goals for box_pos in self.boxes)


class SokobanPygameView:
    """
    • Implémente le pattern MVC en séparant l'affichage (View) de la logique de jeu (Model)
    • Utilise Pygame pour le rendu graphique du jeu
    • Inclut un système de secours pour les images manquantes
    """

    def __init__(self, tile_size=64):
        """
        • Initialise Pygame et prépare les ressources nécessaires pour l'affichage
        • tile_size en paramètre pour permettre différentes résolutions d'affichage
        """
        pygame.init()
        self.tile_size = tile_size
        self.images = {}
        self.font = pygame.font.SysFont(None, 48)  # Police par défaut, taille 48 pour lisibilité
        self.load_images()

    def load_images(self):
        """
        • Centralise le chargement des images en un seul endroit
        • Utilise un dictionnaire pour associer chaque symbole à son image
        • Inclut un système de secours pour gérer les erreurs de chargement d'images
        """
        image_paths = {
            Symbol.WALL: os.path.join("assets", "wall.png"),
            Symbol.BOX: os.path.join("assets", "box.png"),
            Symbol.GOAL: os.path.join("assets", "goal.png"),
            Symbol.BOX_ON_GOAL: os.path.join("assets", "box-on-goal.png"),
            Symbol.PLAYER: os.path.join("assets", "player.png"),
            Symbol.PLAYER_ON_GOAL: os.path.join("assets", "player-on-goal.png")
        }

        for symbol, path in image_paths.items():
            try:
                image = pygame.image.load(path)
                self.images[symbol] = pygame.transform.scale(image, (self.tile_size, self.tile_size))
            except pygame.error as e:
                # Plan de secours en cas d'échec de chargement d'image
                print(f"Couldn't load image {path}: {e}")
                fallback = pygame.Surface((self.tile_size, self.tile_size))
                fallback.fill(self.get_fallback_color(symbol))
                self.images[symbol] = fallback

    def get_fallback_color(self, symbol):
        """
        • Fournit des couleurs de secours pour chaque type d'élément
        • Permet au jeu de fonctionner même si les images sont absentes
        • Utilise des couleurs distinctives pour chaque élément afin de maintenir la jouabilité
        """
        colors = {
            Symbol.WALL: (255, 160, 60),  # Orange pour les murs
            Symbol.BOX: (220, 180, 80),   # Tan pour les boîtes
            Symbol.GOAL: (0, 0, 0),       # Noir pour les objectifs
            Symbol.BOX_ON_GOAL: (150, 100, 50),  # Marron pour une boîte sur un objectif
            Symbol.PLAYER: (255, 255, 0),  # Jaune pour le joueur
            Symbol.PLAYER_ON_GOAL: (255, 200, 0)  # Jaune-orange pour le joueur sur un objectif
        }
        return colors.get(symbol, (100, 100, 100))  # Gris par défaut

    def setup_display(self, model):
        """
        • Configure la fenêtre de jeu en fonction de la taille du niveau
        • Adapte dynamiquement la taille de la fenêtre plutôt que d'utiliser une taille fixe
        • Assure que tous les éléments du niveau sont visibles
        """
        width = model.width() * self.tile_size
        height = model.height() * self.tile_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sokoban")

    def render(self, model):
        """
        • Dessine l'état actuel du jeu à l'écran
        • Utilise le modèle pour déterminer ce qui doit être affiché à chaque position
        • Ignore les cases de sol pour optimiser le rendu (seul le fond blanc est affiché)
        """
        self.screen.fill((255, 255, 255))  # Fond blanc

        # Parcourt chaque case du niveau
        for y in range(model.height()):
            for x in range(model.width()):
                symbol = model.symbol(x, y)

                # Dessine seulement les éléments qui ont une image associée
                if symbol in self.images:
                    self.screen.blit(self.images[symbol], (x * self.tile_size, y * self.tile_size))

        pygame.display.flip()  # Met à jour l'affichage

    def show_message(self, text, color=(0, 255, 0)):
        """
        • Affiche des messages temporaires à l'écran (erreurs, succès, etc.)
        • Utilise un fond semi-transparent pour améliorer la lisibilité
        • Centré sur l'écran pour attirer l'attention du joueur
        """
        screen = pygame.display.get_surface()
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        # Fond semi-transparent pour le message
        background = pygame.Surface((text_rect.width + 20, text_rect.height + 20))
        background.set_alpha(200)  # Valeur d'alpha pour la transparence
        background.fill((0, 0, 0))
        background_rect = background.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        screen.blit(background, background_rect)
        screen.blit(text_surface, text_rect)
        pygame.display.flip()


class SokobanController:
    """
    • Implémente le pattern MVC en reliant le modèle (logique) et la vue (affichage)
    • Gère les entrées utilisateur et les transmet au modèle
    • Contrôle le flux du jeu (initialisation, boucle principale, redémarrage)
    """
    def __init__(self, xsb_file):
        """
        • Initialise le jeu en chargeant un niveau à partir d'un fichier
        • Crée le modèle, la vue, et configure l'affichage
        • Stocke le chemin du niveau pour permettre le redémarrage
        """
        with open(xsb_file, "r") as f:
            self.model = SokobanModel(list(f))
        self.view = SokobanPygameView()
        self.view.setup_display(self.model)
        self.current_level = xsb_file  # Conservé pour la fonctionnalité de redémarrage

    def handle_move_response(self, move_response):
        """
        • Traite les réponses aux tentatives de mouvement (succès ou échec)
        • Affiche un message d'erreur temporaire en cas d'échec
        • Maintient l'affichage à jour même en cas de mouvement invalide
        """
        if move_response != MoveResponse.VALID:
            # Affiche un message d'erreur
            self.view.show_message(move_response.value, color=(255, 100, 100))
            pygame.time.delay(500)  # Affiche le message pendant 500ms

            # Redessine le plateau
            self.view.render(self.model)

    def game_loop(self):
        """
        • Boucle principale du jeu qui:
          1. Capture les événements utilisateur
          2. Met à jour le modèle
          3. Actualise l'affichage
        • Utilise une horloge pour limiter la fréquence d'images
        • Vérifie la complétion du niveau après chaque mouvement valide
        """
        running = True

        # Rendu initial
        self.view.render(self.model)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Gestion des touches
                if event.type == pygame.KEYDOWN:
                    move_response = None

                    # Associe les touches directionnelles et WASD aux déplacements
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        move_response = self.model.move(0, -1)
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        move_response = self.model.move(-1, 0)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        move_response = self.model.move(0, 1)
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        move_response = self.model.move(1, 0)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:  # Redémarrage du niveau
                        with open(self.current_level, "r") as f:
                            self.model = SokobanModel(list(f))
                        self.view.render(self.model)
                        continue

                    # Si un mouvement a été tenté
                    if move_response:
                        self.handle_move_response(move_response)

                        # Redessine après les mouvements valides
                        if move_response == MoveResponse.VALID:
                            self.view.render(self.model)

                            # Vérifie si le niveau est terminé
                            if self.model.is_level_complete():
                                self.view.show_message("success", color=(50, 255, 50))
                                pygame.time.delay(2000)  # Affiche le message de succès pendant 2 secondes
                                running = False

            # Limite la fréquence d'images
            pygame.time.Clock().tick(60)

        pygame.quit()


def main():
    """
    • Point d'entrée du programme
    • Utilise os.path.join pour la portabilité entre systèmes d'exploitation
    • Crée le contrôleur et lance la boucle de jeu
    """
    # Utilise os.path.join pour un code portable (fonctionne sur Mac/Windows/Linux)
    level_path = os.path.join("levels", "level0.xsb")

    # Démarre le jeu
    sokoban = SokobanController(level_path)
    sokoban.game_loop()


if __name__ == "__main__":
    """
    • Exécute la fonction main() seulement si ce fichier est exécuté directement
    • Permet au fichier d'être importé sans exécuter main()
    """
    main()