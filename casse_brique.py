import pygame
COULEUR_NOIR = (0, 0, 0)
COULEUR_BLANC = (255, 255, 255)

class Terrain(object):
    def __init__(self, x0, y0, largeur, hauteur ):
        self.x0 = x0
        self.y0 = y0
        self.largeur = largeur
        self.hauteur = hauteur


class Balle(object):
    def __init__(self):
        self.x = 50
        self.y = 60
        self.vx = 1
        self.vy = 1
        self.rayon = 10

    def dessine_toi(self, fenetre):
        pygame.draw.circle(fenetre, COULEUR_NOIR, [self.x, self.y], self.rayon)
        pass

    def bouge(self, terrain):
        dt = 1
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt

        pass

class MoteurDeJeu(object):
    def __init__(self, titre, largeur_fenetre, hauteur_fenetre):
        pygame.init()

        self.FPS = 120

        self.fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
        pygame.display.set_caption(titre)
        self.horloge = pygame.time.Clock()

    def fait_ton_travail(self, terrain, balle):
        le_jeu_tourne = True
        while le_jeu_tourne:
            tous_les_evenements = pygame.event.get()

            for evenement in tous_les_evenements:
                if evenement.type == pygame.QUIT: # C'est le bouton X sur la fenêtre
                    pygame.quit()
                    quit()

            self.fenetre.fill(COULEUR_BLANC)

            balle.bouge(terrain)
            balle.dessine_toi(self.fenetre)

            pygame.display.update()
            self.horloge.tick(self.FPS)

def boucle_de_jeu():
    le_moteur = MoteurDeJeu('Casse brique', largeur_fenetre = 800, hauteur_fenetre = 600)

    le_terrain = Terrain(x0=0, y0=0, largeur=800, hauteur=600)
    la_balle = Balle()

    le_moteur.fait_ton_travail(le_terrain, la_balle)

if __name__ == '__main__':
    boucle_de_jeu()
