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

    def fait_ton_travail(self):
        le_jeu_tourne = True
        while le_jeu_tourne:
            tous_les_evenements = pygame.event.get()

            for evenement in tous_les_evenements:
                if evenement.type == pygame.QUIT: # C'est le bouton X sur la fenêtre
                    pygame.quit()
                    quit()


def boucle_de_jeu():
    le_moteur = MoteurDeJeu('Casse brique', largeur_fenetre = 800, hauteur_fenetre = 600)

    le_terrain = Terrain()
    la_balle = Balle()

    le_moteur.fait_ton_travail()

if __name__ == '__main__':
    boucle_de_jeu()
