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

    def dessine(self, fenetre):
        pygame.draw.rect(fenetre, COULEUR_BLEUE, [self.x, self.y, self.largeur, self.hauteur])

class Mur:
    def __init__(self, x0, y0, nombre_x, nombre_y, largeur_brique, hauteur_brique):
        self.briques = []
        inter = 2
        for i in range(nombre_x):
            for j in range(nombre_y):
                self.briques.append(Brique(x0 + (largeur_brique + inter) * i, y0 + (hauteur_brique + inter) * j, largeur_brique, hauteur_brique))

    def dessine(self, fenetre):
        for brique in self.briques:
            brique.dessine(fenetre)

class Balle:
    def __init__(self, x0, y0):
        self.vitesse_x = 1
        self.vitesse_y = 1
        self.position_x = int(x0)
        self.position_y = int(y0)
        self.rayon = 10

    def dessine(self, fenetre):
        pygame.draw.circle(fenetre, COULEUR_NOIR, [self.position_x, self.position_y], self.rayon)

    def bouge(self, largeur_fenetre, hauteur_fenetre):
        self.position_x += self.vitesse_x
        self.position_y += self.vitesse_y

        if self.position_x > largeur_fenetre or self.position_x < 0:
            self.vitesse_x = -self.vitesse_x

        if self.position_y > hauteur_fenetre or self.position_y < 0:
            self.vitesse_y = -self.vitesse_y


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

class CasseBrique:
    def __init__(self):
        pass

def game_loop():
    pygame.init()

    largeur_fenetre = 800
    hauteur_fenetre = 600

    FPS = 120

    fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
    pygame.display.set_caption("Jeu: ")
    horloge = pygame.time.Clock()

    tourne = True

    balle = Balle(largeur_fenetre / 2, hauteur_fenetre / 2)
    mur = Mur(0, 0, 10, 3, 40, 20)

    raquette = Raquette(largeur=50, largeur_fenetre=largeur_fenetre, hauteur_fenetre=hauteur_fenetre)

    while tourne:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # C'est le bouton X sur la fenêtre
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    raquette.bouge_a_droite()
                if event.key == pygame.K_LEFT:
                    raquette.bouge_a_gauche()

        balle.bouge(largeur_fenetre, hauteur_fenetre)

        # DRAW
        fenetre.fill(COULEUR_BLANC)

        mur.dessine(fenetre=fenetre)
        balle.dessine(fenetre=fenetre)
        raquette.dessine(fenetre=fenetre)

        pygame.display.update()
        horloge.tick(FPS)

if __name__ == '__main__':
    game_loop()
