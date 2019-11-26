# Version en cours réalisée par enfant

import pygame
COULEUR_NOIR = (0, 0, 0)
COULEUR_GRIS_FONCE = (70, 70, 70)
COULEUR_BLANC = (255, 255, 255)

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

class Terrain(object):
    def __init__(self, x, y, l, h):
        self.x0 = x
        self.y0 = y
        self.largeur = l
        self.hauteur = h

    def reagis_a_la_balle(self, une_balle):
        x1 = self.x0 + self.largeur
        y1 = self.y0 + self.hauteur

        cvx = -1 if une_balle.x < self.x0 or x1 < une_balle.x else 1
        cvy = -1 if une_balle.y < self.y0 or y1 < une_balle.y else 1

        return cvx, cvy

class Balle(object):
    son_rebond = pygame.mixer.Sound('269718__michorvath__ping-pong-ball-hit.wav')

    def __init__(self):
        self.x = 50
        self.y = 60
        self.vx = 1
        self.vy = 1
        self.rayon = 10

    def dessine_toi(self, fenetre):
        pygame.draw.circle(fenetre, COULEUR_GRIS_FONCE, [int(self.x), int(self.y)], self.rayon)
        pass

    def bouge(self, terrain):
        dt = 1
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt

        cvx, cvy = terrain.reagis_a_la_balle(self)

        if cvx == -1 or cvy == -1:
            self.son_rebond.play()

        self.vx *= cvx
        self.vy *= cvy

        pass

class MoteurDeJeu(object):
    def __init__(self, titre, largeur_fenetre, hauteur_fenetre):
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

    le_terrain = Terrain(x=0, y=0, l=800, h=600)
    la_balle = Balle()

    le_moteur.fait_ton_travail(le_terrain, la_balle)

if __name__ == '__main__':
    boucle_de_jeu()
