import pygame

class Terrain(object):
    pass


class Balle(object):
    pass

class MoteurDeJeu(object):
    def __init__(self, titre, largeur_fenetre, hauteur_fenetre):
        pygame.init()

        self.FPS = 120

        self.fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
        pygame.display.set_caption(titre)
        self.horloge = pygame.time.Clock()


def boucle_de_jeu():
    le_moteur = MoteurDeJeu('Casse brique', largeur_fenetre = 800, hauteur_fenetre = 600)

    le_terrain = Terrain()
    la_balle = Balle()

if __name__ == '__main__':
    boucle_de_jeu()
