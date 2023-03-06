import random

# Objet stoquand la partie
class Game():
    def __init__(self):
        # Id du joueur 1 (joueur qui fait l'invitation)
        self.id01 = str(random.randint(0, 999999))
        # Id du joueur 2
        self.id02 = str(random.randint(0, 999999))
        # Stockage de la map de donnée (liste de 0, de 1 ou de 2 en fonction de si le slot est innocupé, ou occupé par un des deux joueurs)
        self.map_ = ""
        # A qui de jouer
        self.turn = 1

        # Création de la matrice de la map 7 colonnes de 6 cases
        for i in range(7 * 6):
            self.map_ += "0"

        # Si oui : la partie n'a pas démarré
        self.is_pending = True

    # Fonction pour changer de tour de jeu
    def switch_turn(self):
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1

    def get_cell(self, x, y):
        return int(self.map_[y * 6 + x])

    def set_cell(self, x, y, value):
        index = y * 6 + x
        self.map_ = self.map_[:index] + str(value) + self.map_[index + 1:]

    # Liste de chaque possibilité de victoire ( 2 diagonales, une horizontale et un verticale)
    def verify_win(self, player):
        for j in range(3):
            for i in range(7):
                if self.get_cell(i, j) == player and \
                        self.get_cell(i, j + 1) == player and self.get_cell(i, j + 2) == player and self.get_cell(i, j + 3) == player:
                    return True

        for i in range(4):
            for j in range(6):
                if self.get_cell(i, j) == player and \
                        self.get_cell(i + 1, j) == player and self.get_cell(i + 2, j) == player and self.get_cell(i + 3, j) == player:
                    return True

        for i in range(3, 6):
            for j in range(3):
                if self.get_cell(i, j) == player and \
                        self.get_cell(i - 1, j + 1) == player and self.get_cell(i - 2, j + 2) == player and self.get_cell(i - 3, j + 3) == player:
                    return True

        for i in range(3, 6):
            for j in range(3, 7):
                if self.get_cell(i, j) == player and \
                        self.get_cell(i - 1, j - 1) == player and self.get_cell(i - 2, j - 2) == player and self.get_cell(i - 3, j - 3) == player:
                    return True

        return False;

    # Fonction utilisé lorsqu'il faut ajouter une piece a une colonne
    def add_column(self, x, value):
        for i in range(6):
            if self.get_cell(x, i) == 0:
                self.set_cell(x, i, value)
                return True
        return False
    # Infos
    def print_info(self):
        print("Id01: ", self.id01)
        print("Id02: ", self.id02)
        print("Map: ", self.map_)
        print("IsPending: ", self.is_pending)

# Super Objet qui stoque toutes les parties en cours
class Games():
    def __init__(self):
        self.list_ = []

# Fonction utile pour recuper une classe par son id
def get_game(id_, games):
    for game in games.list_:
        if game.id01 == id_ or game.id02 == id_:
            return game

    return None
