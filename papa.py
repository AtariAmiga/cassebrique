from random import random

import pygame
from pygame.constants import USEREVENT
from pygame.event import Event

COULEUR_BLANC = (255, 255, 255)
COULEUR_NOIR = (0, 0, 0)
COULEUR_BLEUE = (50, 50, 255)
COULEUR_ROUGE = (255, 50, 50)
COULEUR_VERT = (50, 255, 50)

def envoie_evenement(quoi, qui):
    pygame.event.post(Event(USEREVENT, {'quoi': quoi, 'qui': qui}))

class Brique:
    def __init__(self, x, y, largeur, hauteur):
        self.x = x
        self.y = y
        self.x1 = x + largeur
        self.y1 = y + hauteur
        self.largeur = largeur
        self.hauteur = hauteur
        self.armure_restante = 1 + int(random()*2)

        self.balle = Balle((self.x + self.x1)/2, (self.y + self.y1)/2) if int(random()*10) == 1 else None

    def dessine_toi(self, fenetre):
        if self.armure_restante > 0:
            couleur = COULEUR_BLEUE if self.armure_restante == 1 else COULEUR_ROUGE
            pygame.draw.rect(fenetre, couleur, [self.x, self.y, self.largeur, self.hauteur])
            if self.balle:
                self.balle.dessine_toi(fenetre)

    def reagis_rebond_balle(self, balle):
        if self.armure_restante == 0:
            return 1, 1

        # Si la balle n'est pas arrivée dans la brique
        if balle.x < self.x or self.x1 < balle.x \
            or balle.y < self.y or self.y1 < balle.y:
            return 1, 1

        # Si la balle est rentrée dans la brique
        self.armure_restante -= 1

        if self.armure_restante == 0 and self.balle is not None:
            envoie_evenement('balle_gagnée', self.balle)

        # Cherchons par quel côté elle est rentrée
        cvx = -1 if self.x > balle.x_precedent or self.x1 < balle.x_precedent else 1
        cvy = -1 if self.y > balle.y_precedent or self.y1 < balle.y_precedent else 1

        return cvx, cvy

class MurDeBriques:
    def __init__(self, x0, y0, nombre_x, nombre_y, largeur_une_brique, hauteur_une_brique):
        self.briques = []
        espacement = 2
        for i in range(nombre_x):
            for j in range(nombre_y):
                self.briques.append(
                    Brique(x0 + largeur_une_brique * i,
                           y0 + hauteur_une_brique * j,
                           (largeur_une_brique - espacement),
                           (hauteur_une_brique - espacement)))

    def dessine_toi(self, fenetre):
        for brique in self.briques:
            brique.dessine_toi(fenetre)

    def reagis_rebond_balle(self, balle):
        for brique in self.briques:
            cvx, cvy = brique.reagis_rebond_balle(balle)
            if cvx != 1 or cvy !=1:
                return cvx, cvy

        return 1, 1

class Balle:
    def __init__(self, x0, y0):
        self.x = int(x0)
        self.y = int(y0)
        self.x_precedent = self.x
        self.y_precedent = self.y
        self.vx = 0.2
        self.vy = 0.4
        self.rayon = 10

    def dessine_toi(self, fenetre):
        pygame.draw.circle(fenetre, COULEUR_NOIR, [int(self.x), int(self.y)], self.rayon)

    def bouge(self, dt, objets_rebond:[]):
        self.x_precedent = self.x
        self.y_precedent = self.y

        self.x += self.vx*dt
        self.y += self.vy*dt

        for objet in objets_rebond:
            cvx, cvy = objet.reagis_rebond_balle(self)
            self.vx *= cvx
            self.vy *= cvy

class Raquette:
    def __init__(self, largeur, largeur_fenetre, hauteur_fenetre):
        self.x = int(largeur_fenetre/2)
        self.y = int(hauteur_fenetre) - 10
        self.largeur = largeur

        self.vx = 0


    def dessine_toi(self, fenetre):
        pygame.draw.rect(fenetre, COULEUR_BLEUE, [self.x - self.largeur, self.y, self.largeur, 10])

    def reagis_rebond_balle(self, balle):
        if balle.y < self.y:
            return 1, 1

        if (self.x - self.largeur) <= balle.x and balle.x <= self.x:
            return 1, -1

        return 1, 1

    def bouge(self, dt):
        self.x += self.vx*dt

    def reagit_au_clavier(self, type, touche):
        if type == pygame.KEYDOWN:
            if touche == pygame.K_RIGHT: self.vx = 1
            if touche == pygame.K_LEFT: self.vx = -1

        elif type == pygame.KEYUP:
            if touche == pygame.K_RIGHT: self.vx = 0
            if touche == pygame.K_LEFT: self.vx = 0


class Terrain:
    def __init__(self, x0, y0, largeur, hauteur):
        self.y0 = y0
        self.x0 = x0
        self.largeur = largeur
        self.hauteur = hauteur
        self.epaisseur = 5


    def reagis_rebond_balle(self, balle):
        cvx = -1 if balle.x < (self.x0 + self.epaisseur) or (self.largeur - self.epaisseur) < balle.x else 1
        cvy = -1 if balle.y < (self.y0 + self.epaisseur) else 1

        if balle.y > self.hauteur:
            envoie_evenement('balle_perdue', balle)

        return cvx, cvy

    def dessine_toi(self, fenetre):
        pygame.draw.rect(fenetre, COULEUR_VERT, [self.x0, self.y0, self.epaisseur, self.hauteur])
        pygame.draw.rect(fenetre, COULEUR_VERT, [self.x0, self.y0, self.largeur, self.epaisseur])
        pygame.draw.rect(fenetre, COULEUR_VERT, [self.x0 + self.largeur - self.epaisseur, self.y0, self.epaisseur, self.hauteur])


class MoteurDeJeu(object):
    def __init__(self, titre, largeur_fenetre, hauteur_fenetre):
        pygame.init()

        self.FPS = 120

        self.fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
        pygame.display.set_caption(titre)
        self.horloge = pygame.time.Clock()

    def fais_ton_travail(self, le_terrain:Terrain, la_raquette:Raquette, les_objets_de_rebond:[], l_afficheur):
        le_jeu_tourne = True

        les_balles = [ Balle(le_terrain.largeur / 4, le_terrain.hauteur/ 2), ]

        while le_jeu_tourne:
            dt = self.horloge.tick(self.FPS) # Retourne combien de ms se sont écoulées depuis le dernier appel
            tous_les_evenements = pygame.event.get()

            for evenement in tous_les_evenements:
                if evenement.type == pygame.USEREVENT:
                    if evenement.quoi == 'balle_gagnée':
                        les_balles.append(evenement.qui)

                    elif evenement.quoi == 'balle_perdue':
                        les_balles.remove(evenement.qui)
                        if len(les_balles) == 0:
                            les_balles.append( Balle(le_terrain.largeur / 2, le_terrain.hauteur / 2) )

                elif evenement.type == pygame.QUIT: # C'est le bouton X sur la fenêtre
                    pygame.quit()
                    quit()

                elif evenement.type in (pygame.KEYDOWN, pygame.KEYUP):
                    la_raquette.reagit_au_clavier(evenement.type, evenement.key)

            self.fenetre.fill(COULEUR_BLANC)

            l_afficheur.dessine_toi(fenetre=self.fenetre)

            la_raquette.bouge(dt)

            for balle in les_balles:
                balle.bouge(dt, les_objets_de_rebond)
                balle.dessine_toi(fenetre=self.fenetre)

            for un_objet in les_objets_de_rebond:
                un_objet.dessine_toi(fenetre=self.fenetre)

            pygame.display.update()


class Compteur(object):
    def __init__(self, x0, y0, largeur, hauteur):
        self.x0 = x0
        self.y0 = y0
        self.largeur = largeur
        self.hauteur = hauteur

        self.balles_restantes = 5
        self.score = 0

        self.myfont = pygame.font.SysFont("monospace", 15)

    def dessine_toi(self, fenetre):
        label = self.myfont.render("Balles restantes: " + str(self.balles_restantes) + " Score: " + str(self.score), 1, COULEUR_NOIR)
        fenetre.blit(label, (0, 0))


def boucle_de_jeu():
    largeur_fenetre = 800
    hauteur_fenetre = 600

    le_moteur = MoteurDeJeu('Casse brique', largeur_fenetre = 800, hauteur_fenetre = 600)

    l_afficheur = Compteur(0, 0, largeur_fenetre, 30)
    le_terrain = Terrain(0, 30, largeur_fenetre, hauteur_fenetre)
    le_mur_de_briques = MurDeBriques(0, 80, 12, 4, largeur_fenetre/12, 30)
    la_raquette = Raquette(largeur=largeur_fenetre/5, largeur_fenetre=largeur_fenetre, hauteur_fenetre=hauteur_fenetre)

    les_objets_de_rebond = [le_terrain, le_mur_de_briques, la_raquette]

    le_moteur.fais_ton_travail(le_terrain, la_raquette, les_objets_de_rebond, l_afficheur)

if __name__ == '__main__':
    boucle_de_jeu()
