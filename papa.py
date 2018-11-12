import pygame

COULEUR_BLANC = (255, 255, 255)
COULEUR_NOIR = (0, 0, 0)
COULEUR_BLEUE = (50, 50, 255)

class Brique:
    def __init__(self, x, y, largeur, hauteur):
        self.x = x
        self.y = y
        self.x1 = x + largeur
        self.y1 = y + hauteur
        self.largeur = largeur
        self.hauteur = hauteur
        self.est_cassee = False

    def dessine(self, fenetre):
        if not self.est_cassee:
            pygame.draw.rect(fenetre, COULEUR_BLEUE, [self.x, self.y, self.largeur, self.hauteur])

    def reagit_rebond_balle(self, balle):
        if self.est_cassee:
            return 1, 1

        # Si la balle n'est pas arrivée dans la brique
        if balle.x < self.x or self.x1 < balle.x \
            or balle.y < self.y or self.y1 < balle.y:
            return 1, 1

        # Si la balle est dans la brique
        self.est_cassee = True

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
                    Brique(x0 + (largeur_une_brique + espacement) * i,
                           y0 + (hauteur_une_brique + espacement) * j,
                           largeur_une_brique,
                           hauteur_une_brique))

    def dessine(self, fenetre):
        for brique in self.briques:
            brique.dessine(fenetre)

    def reagit_rebond_balle(self, balle):
        for brique in self.briques:
            cvx, cvy = brique.reagit_rebond_balle(balle)
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
        self.vy = -0.4
        self.rayon = 10

    def dessine(self, fenetre):
        pygame.draw.circle(fenetre, COULEUR_NOIR, [int(self.x), int(self.y)], self.rayon)

    def bouge(self, dt, objets_rebond:[]):
        self.x_precedent = self.x
        self.y_precedent += self.y

        self.x += self.vx*dt
        self.y += self.vy*dt

        for objet in objets_rebond:
            cvx, cvy = objet.reagit_rebond_balle(self)
            self.vx *= cvx
            self.vy *= cvy

class Raquette:
    def __init__(self, largeur, largeur_fenetre, hauteur_fenetre):
        self.x = int(largeur_fenetre/2)
        self.y = int(hauteur_fenetre) - 10
        self.largeur = largeur

        self.vx = 0


    def dessine(self, fenetre):
        pygame.draw.rect(fenetre, COULEUR_BLEUE, [self.x - self.largeur, self.y, self.largeur, 10])

    def reagit_rebond_balle(self, balle):
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

    def reagit_rebond_balle(self, balle):
        cvx = -1 if balle.x > self.largeur or balle.x < self.x0 else 1
        cvy = -1 if balle.y < self.x0 else 1

        if balle.y > self.hauteur:
            balle.y = 300 # todo: implémenter balle sortie

        return  cvx, cvy

    def dessine(self, fenetre):
        pass # todo: dessiner


class MoteurDeJeu(object):
    def __init__(self, titre, largeur_fenetre, hauteur_fenetre):
        pygame.init()

        self.FPS = 120

        self.fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
        pygame.display.set_caption(titre)
        self.horloge = pygame.time.Clock()

    def fais_ton_travail(self, la_balle:Balle, la_raquette:Raquette, les_objets_de_rebond:[]):
        le_jeu_tourne = True

        while le_jeu_tourne:
            dt = self.horloge.tick(self.FPS) # Retourne combien de ms se sont écoulées depuis le dernier appel
            tous_les_evenements = pygame.event.get()

            for evenement in tous_les_evenements:
                if evenement.type == pygame.QUIT: # C'est le bouton X sur la fenêtre
                    pygame.quit()
                    quit()

                elif evenement.type in (pygame.KEYDOWN, pygame.KEYUP):
                    la_raquette.reagit_au_clavier(evenement.type, evenement.key)

            self.fenetre.fill(COULEUR_BLANC)


            la_raquette.bouge(dt)

            la_balle.bouge(dt, les_objets_de_rebond)

            la_balle.dessine(fenetre=self.fenetre)
            for un_objet in les_objets_de_rebond:
                un_objet.dessine(fenetre=self.fenetre)

            pygame.display.update()


def boucle_de_jeu():
    largeur_fenetre = 800
    hauteur_fenetre = 600

    le_moteur = MoteurDeJeu('Casse brique', largeur_fenetre = 800, hauteur_fenetre = 600)

    la_balle = Balle(largeur_fenetre / 2, hauteur_fenetre / 2)
    le_terrain = Terrain(0, 0, largeur_fenetre, hauteur_fenetre)
    le_mur_de_briques = MurDeBriques(0, 0, 12, 4, 50, 30)
    la_raquette = Raquette(largeur=largeur_fenetre/5, largeur_fenetre=largeur_fenetre, hauteur_fenetre=hauteur_fenetre)

    les_objets_de_rebond = [le_terrain, le_mur_de_briques, la_raquette]

    le_moteur.fais_ton_travail(la_balle, la_raquette, les_objets_de_rebond)

if __name__ == '__main__':
    boucle_de_jeu()
