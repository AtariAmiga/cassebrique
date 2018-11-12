import pygame

COULEUR_BLANC = (255, 255, 255)
COULEUR_NOIR = (0, 0, 0)
COULEUR_BLEUE = (50, 50, 255)

class Brique:
    def __init__(self, x, y, largeur, hauteur):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.est_cassee = False

    def dessine(self, fenetre):
        if not self.est_cassee:
            pygame.draw.rect(fenetre, COULEUR_BLEUE, [self.x, self.y, self.largeur, self.hauteur])

    def reagit_rebond_balle(self, balle):
        if self.est_cassee:
            return 1, 1

        if self.x > balle.position_x or self.x + self.largeur < balle.position_x \
            or self.y > balle.position_y or self.y + self.hauteur < balle.position_y:
            return 1, 1

        self.est_cassee = True
        cx = 1
        cy = 1

        return cx, cy

class MurDeBriques:
    def __init__(self, x0, y0, nombre_x, nombre_y, largeur_brique, hauteur_brique):
        self.briques = []
        espacement = 2
        for i in range(nombre_x):
            for j in range(nombre_y):
                self.briques.append(
                    Brique( x0 + (largeur_brique + espacement) * i,
                            y0 + (hauteur_brique + espacement) * j,
                            largeur_brique,
                            hauteur_brique))

    def dessine(self, fenetre):
        for brique in self.briques:
            brique.dessine(fenetre)

    def reagit_rebond_balle(self, balle):
        for brique in self.briques:
            cx, cy = brique.reagit_rebond_balle(balle)
            if cx != 1 or cy !=1:
                return cx, cy

        return 1, 1

class Balle:
    def __init__(self, x0, y0):
        self.vitesse_x = 1
        self.vitesse_y = 1
        self.position_x = int(x0)
        self.position_y = int(y0)
        self.rayon = 10

    def dessine(self, fenetre):
        pygame.draw.circle(fenetre, COULEUR_NOIR, [self.position_x, self.position_y], self.rayon)

    def bouge(self, objets_rebond:[]):
        self.position_x += self.vitesse_x
        self.position_y += self.vitesse_y

        for objet in objets_rebond:
            cx, cy = objet.reagit_rebond_balle(self)
            self.vitesse_x *= cx
            self.vitesse_y *= cy

class Raquette:
    def __init__(self, largeur, largeur_fenetre, hauteur_fenetre):
        self.position_x = int(largeur_fenetre/2)
        self.position_y = int(hauteur_fenetre) - 10
        self.largeur = largeur

    def dessine(self, fenetre):
        pygame.draw.rect(fenetre, COULEUR_BLEUE, [self.position_x - self.largeur, self.position_y, self.largeur, 10])

    def bouge_a_droite(self):
        self.position_x += 20

    def bouge_a_gauche(self):
        self.position_x -= 20

    def reagit_rebond_balle(self, objet):
        return 1, 1 # todo: à faire


class Terrain:
    def __init__(self, x0, y0, largeur, hauteur):
        self.y0 = y0
        self.x0 = x0
        self.largeur = largeur
        self.hauteur = hauteur

    def reagit_rebond_balle(self, objet):
        cx = -1 if objet.position_x > self.largeur or objet.position_x < self.x0 else 1
        cy = -1 if objet.position_y > self.hauteur or objet.position_y < self.x0 else 1
        
        return  cx, cy

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
            tous_les_evenements = pygame.event.get()

            for evenement in tous_les_evenements:
                if evenement.type == pygame.QUIT: # C'est le bouton X sur la fenêtre
                    pygame.quit()
                    quit()
                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_RIGHT:
                        la_raquette.bouge_a_droite()
                    if evenement.key == pygame.K_LEFT:
                        la_raquette.bouge_a_gauche()

            self.fenetre.fill(COULEUR_BLANC)

            la_balle.bouge(les_objets_de_rebond)

            la_balle.dessine(fenetre=self.fenetre)
            for un_objet in les_objets_de_rebond:
                un_objet.dessine(fenetre=self.fenetre)

            pygame.display.update()
            self.horloge.tick(self.FPS)


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
