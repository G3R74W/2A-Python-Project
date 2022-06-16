import pygame
import time
import random
import Button
from pygame.locals import *

dimensions = (1024, 574)
dimensions2 = (800, 800)


# main_dir = os.path.split(os.path.abspath(__file__))[0]

#fonction pour charger les images
def load_image(name, scalex, scaley, colorkey=None):
    """
    cette fonction permet de charger une image avec une taille choisi et de récuperer un rectangle de la taille de l'image
    :param name: nom de l'image
    :param scalex: Ratio de l'image en x
    :param scaley: Ratio de l'image en y
    :param colorkey: couleur des pixel que l'on veut faire disparaitre
    :return : l'image et le rectangle associe a l'image
    """
    #on recupere l'image
    image = pygame.image.load("img/%s"%(name))
    #on l'afiiche
    image = image.convert()
    print("image <%s> rect %s" % (name, image.get_rect()))
    #on recupere ces dimensions
    bx, by, dimx, dimy = image.get_rect()
    #on regarde les ratio en longueur et en largeur
    #on prend le plus petit pour ne pas difformer l'image
    ratiox, ratioy = scalex / dimx, scaley / dimy
    ratiom = min(ratiox, ratioy)
    scalex, scaley = int(dimx * ratiom), int(dimy * ratiom)
    #on regarde la couleur voulu pour l'image -1 => couleur d'origine
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    # on redimensione l'image
    image = pygame.transform.scale(image, (scalex, scaley))
    #et on la renvoie avec son rectangle associe
    return image, image.get_rect()


#classe pour charger les sons
def load_sound(name):
    """
    cette fonction permet de charger un sons pour pouvoir le jouer plus tard
    :param name: nom du sons
    :return: renvoie le sons sinon renvoie un objet vide s'il y a un probleme avec pygame.mixer ou une erreur s'il ne trouve pas le sons
    """
    #classe d'objet de son pour pouvoir renvoyer un objet vide s'il y a un probleme avec pygame.mixer
    class NoneSound:
        def play(self): pass
    #on regarde si pygame.mixer et installe ou si il et initialise
    if not pygame.mixer or not pygame.mixer.get_init():
        #on revoie si il existe un objet de la classe NoneSound
        return NoneSound()
    # print("main_dir = %s"%(main_dir))
    # fullname = os.path.join(main_dir, name)
    # print("fullname=%s"%(fullname))

    #on essaye de lire le son choisi
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error:
        # sinon on leve une erreur
        print('Cannot load sound: %s' % name)
        raise SystemExit(str(pygame.get_error()))
    return sound

#classe du personage pricipale
class Perso(pygame.sprite.Sprite):
    def __init__(self):
        """
        fonction d'initialisation des variables principales
        """
        # initialisation de ses variables pricipale
        pygame.sprite.Sprite.__init__(self)
        self.image_1  , self.rect_1    = load_image(name='perso1.png', scalex=100, scaley=100, colorkey=-1 )
        self.liste_image = (load_image(name='perso1.png', scalex=100, scaley=100, colorkey=-1) ,
                            load_image(name='perso2.png', scalex=100, scaley=100, colorkey=-1) ,
                            load_image(name='perso3.png', scalex=100, scaley=100, colorkey=-1) ,
                            load_image(name='perso4.png', scalex=100, scaley=100, colorkey=-1) ,
                            load_image(name='perso5.png', scalex=100, scaley=100, colorkey=-1) ,
                            load_image(name='perso6.png', scalex=100, scaley=100, colorkey=-1) ,
                            load_image(name='perso7.png', scalex=100, scaley=100, colorkey=-1) ,
                            load_image(name='perso8.png', scalex=100, scaley=100, colorkey=-1) ,
                            load_image(name='perso9.png', scalex=100, scaley=100, colorkey=-1) ,
                            load_image(name='perso10.png', scalex=100, scaley=100, colorkey=-1),
                            load_image(name='perso11.png', scalex=100, scaley=100, colorkey=-1),
                            load_image(name='perso12.png', scalex=100, scaley=100, colorkey=-1),
                            load_image(name='perso13.png', scalex=100, scaley=100, colorkey=-1),
                            load_image(name='perso14.png', scalex=100, scaley=100, colorkey=-1),
                            load_image(name='perso15.png', scalex=100, scaley=100, colorkey=-1),
                            load_image(name='perso16.png', scalex=100, scaley=100, colorkey=-1))
        self.image, self.rect = self.image_1, self.rect_1
        self.y = 0
        self.x = 500
        self.ay = 0
        self.ax = 0
        self.h = 576 - self.y
        self.l = 1024 - self.x
        self.c_right = False
        self.c_left = False
        self.c_top = False
        self.sol = []
        self.plateforme = []
        self.y_sol = 451
        self.compteur = 0
        self.flip = False
        self.image_mem = self.image_1
        self.i = 0

    #fonction d'actualisation
    def update(self):
        """
        fonction qui met a jour la position du personnage
        :return:
        """
        #on diminue les acceleration du personnage
        if self.ay > .015:
            self.ay = self.ay - .01
        elif self.ay < -.015:
            self.ay = self.ay + .01
        else:
            self.ay = 0


        if self.ax > .075:
            if self.ay == 0:
                self.ax = self.ax - .05
        elif self.ax < -.075:
            if self.ay == 0:
                self.ax = self.ax + .05
        else:
            self.ax = 0

        #on fait en sortes que le personage marche sur le sol et les obstacles
        for sol in self.plateforme:
            # delta x delta y
            delx = sol[1] - sol[0]
            dely = sol[3] - sol[2]
            # coef directeur
            dir = dely / delx
            # on transforme le x car sinon il est trop grand
            x = self.x - sol[0]
            # print("dely=%s delx=%s dir=%s x=%s"%(dely,delx,dir,x))
            if sol[0] <= self.x < sol[1] and self.ay <= 0:
                self.y_sol = sol[2] + dir * x
                #      print("self.y_sol=%s et self.y =%s"%(self.y_sol,self.y))
                if self.y_sol - 115 <= self.y <= self.y_sol - 85:
                    self.y = self.y_sol - 100
                    self.ay = 0
                elif self.y < self.y_sol - 105:
                    self.ay -= 0.25
                if self.c_top == True:
                    self.ay = 0

        # on fait en sorte que le personnage ne rentre pas dans les obstacles
        if self.c_right and self.ax > 0 and not self.c_top:
            self.ax = 0
        elif self.c_left and self.ax < 0 and not self.c_top:
            self.ax = 0
        #  print("update xy=%6.2lf/%6.2lf ax/ay=%6.2lf/%6.2lf"%(self.x,self.y,self.ax,self.ay))
        #on actualise les position x et y
        self.y -= self.ay
        self.x += self.ax
        #on verfie que les acceleration sont en dessous de leurs valeurs maximale
        if not self.ay == 0:
            self.ay -= 0.5
        if self.ay > 30:
            self.ay = 30
        elif self.ay < -30:
            self.ay = -30

        if self.ax > 3:
            self.ax = 3
        elif self.ax < -3:
            self.ax = -3

        #inplementation de la gravite
        if self.y < 0:
            self.ay -= 1.5

        #on fait en sorte que le personnage ne sorte pas de la fenetre
        if self.x < 0:
            self.x = 0
            self.ax = -self.ax
        elif self.x > 1024:
            self.x = 1024
            self.ax = -self.ax

        # print("h=%s l=%s"%(str(self.h),str(self.l)))
        #on retourne l'image de personnage si besoin
        if self.ax < 0 and self.flip == False:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flip = True
        elif self.ax > 0 and self.flip == True:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flip = False
        #on change son image
        if self.compteur == 10:
            self.compteur = 0
            if not self.ax == 0:
                self.image, self.rect = self.liste_image[self.i]
                self.i += 1
                self.flip = False
                if self.i >= len(self.liste_image):
                    self.i = 0
        self.compteur += 1
        #  print("le compteur est a %s"%(self.compteur))

        #on met a jour sa position et sa zone de collision
        self.pos = (self.x, self.y)
        self.rect.midtop = self.pos
        # print("le sol est :%s"%(self.sol))

    #fonction qui met la l'objet a une position donne princiapalement utilise pour initialise la position d'un objet
    def setpos(self, pos=(500, 0)):
        """
        fonction qui defini la position de base du personnage
        :param pos: tuple x,y contenant la position du personnage
        :return:
        """
        self.ax = self.ay = 0
        self.x, self.y = pos
        self.pos = pos
        self.rect.midtop = self.pos

    #  print("setpos xy=%6.2lf/%6.2lf ax/ay=%6.2lf/%6.2lf"%(self.x,self.y,self.ax,self.ay))

    def colision(self, cible):
        """
        fonction qui gere les collisions
        :param cible: autre objet du tableau
        :return:
        """
        #fonction testant les collisions avec les autres objets du jeu
        #on prend le rectangle associee a l'image du personnage comme hitbox
        hitbox = self.rect  # .inflate(-100, -100)

        #on initialise les variables
        mort = False
        collision = False
        fin = False

        #on recupere les coordonnees x puis y du rectangle associee a la cible
        #puis on recupere la longueur et la hauteur de ce meme rectangle
        ciblex = cible.rect[0]
        cibley = cible.rect[1]
        ciblelong = cible.rect[2]
        ciblehaut = cible.rect[3]

        #si notre objet est initialise
        if self.rect[0]:
            #on teste la collision avec le cible
            rect2 = cible.rect
            self.c = hitbox.colliderect(cible.rect)
            if not self.c:
                #s'il n'y a pas de collision on retest on augmentant la taille de rectangle de la cible
                rect2 = rect2.inflate(10, 10)
                r2 = hitbox.colliderect(rect2)
                if r2:
                    collision = True
            else:
                #s'il y a collision
                collision = True
                #on regarde si la cible est mortelle ou si c'est la fin du niveau
                mort = cible.mortelle()
                fin = cible.finish()
                #ensuite on teste si on est a droite, a gauche, ou au dessus
                if self.rect[0] + self.rect[2] <= ciblex + 20:
                    self.c_right = True
                elif self.rect[0] >= ciblex + ciblelong - 20:
                    self.c_left = True
                if self.rect[1] + self.rect[3] <= cibley + 20:
                    print("je suis au dessus")
                    self.c_top = True


        return collision, mort, fin

    def deplacement(self, dir, val):
        """
        fonction qui gere le deplacement
        :param dir: direction de deplacement
        :param val: valeur d'acceleration
        :return:
        """
        #fonction qui augmente l'acceleration dans un direction
        if dir == "droite":
            self.ax += val
        elif dir == "gauche":
            self.ax -= val
        elif dir == "haut":
            self.ay += val
        elif dir == "bas":
            self.ay -= val
        self.update()

    def plate(self):
        """
        fonction qui gere les plateformes pour le personnage
        :return:
        """
        #fonction du gere les plateformes
        for seg in self.sol:
            segxdebut = seg[0][0]
            segxfin = segxdebut + seg[1][0]
            segydebut = seg[0][1]
            segyfin = segydebut + seg[1][1]
            self.plateforme.append((segxdebut, segxfin, segydebut, segyfin))


class Fond(pygame.sprite.Sprite):
    def __init__(self, nom):
        """
        fonction d'initialisation des parametres
        :param nom: nom de l'image
        """
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name='%s' % (nom), scalex=dimensions[0], scaley=dimensions[1], colorkey=-1)

    def update(self):
        """
        fonction qui met a jour la position de l'objet
        :return:
        """
        self.rect.midtop = self.pos

    def setpos(self, pos):
        """
        fonction qui definit la position de base de l'objet
        :param pos: tuple x,y contenant la position de l'objet
        :return:
        """
        self.pos = pos
        self.rect.midtop = self.pos

    def mortelle(self):
        """
        fonction qui retourne si l'objet est mortelle
        :return: False
        """
        return False

    def finish(self):
        """
        fonction qui retourne si l'ibjet est un fin
        :return: False
        """

        return False


class Caisse(pygame.sprite.Sprite):
    def __init__(self):
        """
        fonction d'initailisation des variables
        """
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name='caisse.png', scalex=100, scaley=100, colorkey=-1)

    def update(self):
        """
        fonction qui met a jour la position de l'objet
        :return:
        """
        self.rect.midtop = self.pos

    def setpos(self, pos):
        """
        fonction qui definit la position de base de l'objet
        :param pos: tuple x,y contenant la position de l'objet
        :return:
        """
        self.pos = pos
        self.rect.midtop = self.pos

    def mortelle(self):
        """
        fonction qui retourne si l'objet est mortelle
        :return: False
        """
        return False

    def finish(self):
        """
        fonction qui retourne si l'ibjet est un fin
        :return: False
        """
        return False


class Flame(pygame.sprite.Sprite):
    def __init__(self):
        """
        fonction d'initialisation des variables
        """
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name='flame.png', scalex=50, scaley=100, colorkey=-1)

    def update(self):
        """
        fonction qui met a jour la position de l'objet
        :return:
        """
        self.rect.midtop = self.pos

    def setpos(self, pos):
        """
        fonction qui definit la position de base de l'objet
        :param pos: tuple x,y contenant la position de l'objet
        :return:
        """
        self.pos = pos
        self.rect.midtop = self.pos

    def mortelle(self):
        """
        fonction qui retourne si l'objet est mortelle
        :return: True
        """
        return True

    def finish(self):
        """
        fonction qui retourne si l'ibjet est un fin
        :return: False
        """
        return False


class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        """
        fontcion d'initialisation des variables
        """
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name='ennemi.png', scalex=50, scaley=100, colorkey=-1)
        self.speedx = 0
        self.speedy = 0
        self.limhg = []
        self.limbg = []
        self.limbd = []
        self.limhd = []
        self.sens = "trigo"

    def update(self):
        """
        fonction qui met a jour l'objet
        :return:
        """
        if self.sens <= "trigo":
            if self.limhg[0] - 5 <= self.pos[0] <= self.limhg[0] + 5 and self.limhg[1] - 5 <= self.pos[1] <= self.limhg[
                1] + 5:
                if self.speedx < 0:
                    self.speedy = -self.speedx
                else:
                    self.speedy = self.speedx
                self.speedx = 0
            elif self.limbg[1] - 5 <= self.pos[1] <= self.limbg[1] + 5 and self.limbg[0] - 5 <= self.pos[0] <= \
                    self.limbg[0] + 5:
                self.speedx = self.speedy
                self.speedy = 0
            elif self.limbd[0] - 5 <= self.pos[0] <= self.limbd[0] + 5 and self.limbd[1] - 5 <= self.pos[1] <= \
                    self.limbd[1] + 5:
                self.speedy = -self.speedx
                self.speedx = 0
            elif self.limhd[1] - 5 <= self.pos[1] <= self.limhd[1] + 5 and self.limhd[0] - 5 <= self.pos[0] <= \
                    self.limhd[0] + 5:
                self.speedx = self.speedy
                self.speedy = 0
            elif self.limhg[0] + 5 <= self.pos[0] <= self.limhd[0] - 5 and self.limhg[1] + 5 <= self.pos[1] <= \
                    self.limhg[1] - 5:
                if self.speedx > 0:
                    self.speedx = -self.speedx
                self.speedy = 0
            elif self.limhg[1] + 5 <= self.pos[1] <= self.limbg[1] - 5 and self.limhg[0] + 5 <= self.pos[0] <= \
                    self.limhg[0] - 5:
                if self.speedy < 0:
                    self.speedy = -self.speedy
                self.speedx = 0
            elif self.limbg[0] + 5 <= self.pos[0] <= self.limbd[0] - 5 and self.limbd[1] + 5 <= self.pos[1] <= \
                    self.limbd[1] - 5:
                if self.speedx < 0:
                    self.speedx = -self.speedx
                self.speedy = 0
            elif self.limhd[1] + 5 <= self.pos[1] <= self.limbd[1] - 5 and self.limbd[0] + 5 <= self.pos[0] <= \
                    self.limbd[0] - 5:
                if self.speedy > 0:
                    self.speedy = -self.speedy
                self.speedx = 0


        elif self.sens == "horaire":
            print("le sens horaire n'a pas encore ete developpe")
            self.sens = "trigo"
        else:
            print("------------------sens non valide---------------------")
            self.sens = "trigo"
        # print("la vitesse en x est %s et celle en y est %s"%(self.speedx,self.speedy))
        # print("les coordonnes de la flame sont (%s,%s)"%(self.pos[0],self.pos[1]))
        self.pos = (self.pos[0] + self.speedx, self.pos[1] + self.speedy)
        self.rect.midtop = (self.pos[0], self.pos[1] - 50)

    def setpos(self, pos, hg, bg, bd, hd, speed, sens):
        """
        fonction la position les differents parametres de cet objet
        :param pos: tuple x,y qui represente la position de l'objet
        :param hg: bord haut gauche de l'ecran
        :param bg: bord bas gauche de l'ecran
        :param bd: bord bas droit de l'ecran
        :param hd: bord haut droit de l'ecran
        :param speed: vitesse de l'objet
        :param sens: sens de rotation
        :return:
        """
        self.pos = pos
        self.speedx = speed
        self.speedy = speed
        self.limhg = hg
        self.limbg = bg
        self.limbd = bd
        self.limhd = hd
        self.sens = sens
        self.rect.midtop = (self.pos[0], self.pos[1])

    def mortelle(self):
        """
        fonction qui renvoie si l'objet est mortelle
        :return: True
        """
        return True

    def finish(self):
        """
        fonction qui renvoie si l'objet est une fin
        :return: False
        """
        return False


class Finish(pygame.sprite.Sprite):
    def __init__(self, long, largeur):
        """
        fontion d'initialisation des vaiables
        :param long: vitesse selon l'axe X
        :param largeur: vitesse selon l'axe Y
        """
        self.finis = False
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name='finish.png', scalex=largeur, scaley=long, colorkey=-1)

    def update(self):
        """
        fonction qui met a jour cette objet
        :return:
        """
        self.rect.midtop = self.pos

    def setpos(self, pos):
        """
        fonction qui defini la position de cette objet
        :param pos: tuple x,y qui represente la position de l'objet
        :return:
        """
        self.pos = pos
        self.rect.midtop = self.pos

    def mortelle(self):
        """
        fonction qui renvoie si l'objet est mortelle
        :return: False
        """
        return False

    def finish(self):
        """
        fonction qui renvoie si l'objet est une fin
        :return: True
        """
        return True


class Obstacle_rebond(pygame.sprite.Sprite):
    def __init__(self, vx=10, vy=10):
        """
        fontion d'initialisation des vaiables
        :param vx: vitesse selon l'axe X
        :param vy: vitesse selon l'axe Y
        """
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name='hot-fireball-60.png', scalex=60, scaley=60, colorkey=-1)
        self.vx = vx
        self.vy = vy

    def update(self):
        """
        fonction qui met a jour la position de cette objet
        :return:
        """
        new_posx, new_posy = self.pos[0] + self.vx, self.pos[1] + self.vy
        if new_posx <= 0:
            new_posx = 0
            self.ax = -self.ax + random.randint(-1, 1)
        elif new_posx > 1024:
            new_posx = 1024
            self.ax = -self.ax + random.randint(-1, 1)
        if new_posy <= 0:
            new_posy = 0
            self.ay = -self.ay + random.randint(-1, 1)
        elif new_posy > 576:
            new_posy = 576
            self.ay = -self.ay + random.randint(-1, 1)
        self.pos = (new_posx, new_posy)
        self.rect.midtop = (new_posx, new_posy)

    def setpos(self, pos):
        """
        fonction qui defini la position de cette objet
        :param pos: tuple x,y qui represente la position de l'objet
        :return:
        """
        self.pos = pos
        self.rect.midtop = self.pos

    def mortelle(self):
        """
        fonction qui renvoie si l'objet est mortelle
        :return: True
        """
        return True

    def finish(self):
        """
        fonction qui renvoie si l'objet est une fin
        :return: False
        """
        return False


class Tableau():
    def __init__(self, window, nom):
        """
        fonction d'initialisation des vaiables
        :param window: fenetre pygame
        :param nom: nom de la fenetre pygame
        """
        #initialisation des differentes varibles
        self.window = window
        self.nom = nom
        self.perso = None
        self.obstacles = []
        self.pieges = []
        self.enemies = []
        self.sol = []
        self.sprites = []
        self.backgroundcolor = (250, 250, 250)
        self.background = pygame.Surface(self.window.get_size()).convert()
        self.background.fill(self.backgroundcolor)
        self.segment = []
        self.finishbg = []
        self.finishhd = []
        self.finishhg = []
        self.finishbd = []
        self.dim_fin = []
        self.fond = []
        self.sprite_fond = []

    def update(self, timer, window):
        """
        fonction qui met a jour les elements d'un tableau
        :param timer: temps depuis le debut du jeu
        :param window: fenetre pygame
        :return:
        """
        #fonction qui met a jour tous les objets du tableau
        pygame.display.set_caption(self.nom)
        allsprites = self.obstacles + self.pieges + self.enemies + [self.perso]
        self.sprite_fond = pygame.sprite.RenderPlain(self.fond)
        self.sprites = pygame.sprite.RenderPlain(allsprites)
        white = (50, 50, 50)
        font = pygame.font.Font(None, 20)
        text = font.render("%s  s" % (timer / 1000), 1, white)
        window.blit(text, (10, 10))
        pygame.display.flip()

    def dessin(self):
        """
        fonction qui dessine tous les elements d'un tableau
        :return:
        """
        #fonction qui dessine tous les objets du tableau
        self.background.fill(self.backgroundcolor)
        self.sprites.update()
        self.perso.update()
        self.window.blit(self.background, (0, 0))
        for polyline in self.sol:
            solcolor = (0, 0, 0)
            pygame.draw.lines(self.window, solcolor, False, polyline)
        self.sprite_fond.draw(self.window)
        self.sprites.draw(self.window)
        pygame.display.flip()

    def plateforme(self):
        """
        fonction qui gere les platformes dans les tableaux
        :return:
        """
        #fonction qui gere les plateformes
        for plateforme in self.sol:
            print("plateforme:%s" % ([plateforme]))
            point1 = [0, 0]
            point2 = [0, 0]
            for point in plateforme:
                point1 = point
                print("point1 =%s" % ([point1]))
                if point2[0] == 0 and point2[1] == 0:
                    point2 = point
                    print("point2 =%s" % ([point2]))
                else:
                    deplacementx = point1[0] - point2[0]
                    deplacementy = point1[1] - point2[1]
                    self.segment.append((point2, (deplacementx, deplacementy)))
                    point2 = point
                    print("point2 =%s" % ([point2]))
        print("---------------------segment:(%s)----------------------" % ([self.segment]))


def jeu(reference_timer, actif=0):
    """
    Fonction pricipale du jeu qui contient le cre   tion des niveaux ainsi que la boucle principale du jeu
    :param reference_timer: temps entre la creation de la fentre du menu et le debut du jeu
    :param actif: permet de avoir quel tableau doit être jouer
    :return:
    """
    #initialisation du timer
    timer = pygame.time.get_ticks() - reference_timer
    print(
        "###########################\n###########################\n###########################\n###########################\n")
    print("le temps ecoule est %s s" % (timer / 1000))
    print(
        "###########################\n###########################\n###########################\n###########################\n")
    mort = False
    fin = False
    pygame.init()
    window = pygame.display.set_mode(dimensions)
    pygame.display.set_caption("VIDE")
    # on charge la musique pluis on la joue
    pygame.mixer.music.load("sound/musique.mp3")
    pygame.mixer.music.play(-1)
    son_saut = pygame.mixer.Sound('sound/saut2.wav')
    son_mort = pygame.mixer.Sound('sound/mort(2).wav')
    son_fin = pygame.mixer.Sound('sound/0236.wav')
    # on cache la souris
    pygame.mouse.set_visible(0)
    # image gameover
    game = pygame.image.load('img/game.jpg')
    game = pygame.transform.scale(game, dimensions)
    # definition de l'horloge
    clock = pygame.time.Clock()

    # permission de pouvoir rester appuye sur une touche pour repeter une action
    pygame.key.set_repeat(100, 30)

    # creaation de la liste des tableaux
    tableaux = []
    tableaux.append(Tableau(window, "premier tableau"))
    tableaux.append(Tableau(window, "deuxieme tableau"))
    tableaux.append(Tableau(window, "troisieme tableau"))
    tableaux.append(Tableau(window, "quatrieme tableau"))
    nombre_tableaux = len(tableaux)

    # creation du personnage
    perso = Perso()
    perso.setpos()

    #remplissage des differents tableaux
    tableaux[0].perso = perso
    tableaux[0].enemies.append(Enemies())
    tableaux[0].enemies[0].setpos((0, 0), (0, 0), (0, 576), (1024, 576), (1024, 0), 10, "trigo")
    tableaux[0].fond.append(Fond("fond.jpg"))
    tableaux[0].fond[0].setpos((dimensions[0] / 2, 0))
    tableaux[0].obstacles.append(Finish(50, 50))
    tableaux[0].obstacles[0].setpos((100, 200))
    tableaux[0].dim_fin.append(((0, 576), (0, 0), (200, 0), (200, 576)))
    tableaux[0].sol.append(((0, 500), (1024, 500)))

    tableaux[1].perso = perso
    tableaux[1].fond.append(Fond("fond.jpg"))
    tableaux[1].fond[0].setpos((dimensions[0] / 2, 0))
    tableaux[1].obstacles.append(Finish(50, 50))
    tableaux[1].obstacles[0].setpos((100, 200))
    tableaux[1].obstacles.append(Caisse())
    tableaux[1].obstacles[1].setpos((230, 401))
    tableaux[1].pieges.append(Obstacle_rebond(vx=5, vy=3.5))
    tableaux[1].pieges[0].setpos((40, 40))
    tableaux[1].sol.append(((0, 500), (1024, 500)))

    tableaux[2].perso = perso
    tableaux[2].fond.append(Fond("fond.jpg"))
    tableaux[2].fond[0].setpos((dimensions[0] / 2, 0))
    tableaux[2].obstacles.append(Finish(50, 50))
    tableaux[2].obstacles[0].setpos((100, 200))
    tableaux[2].obstacles.append(Caisse())
    tableaux[2].obstacles[1].setpos((800, 401))
    tableaux[2].pieges.append(Flame())
    tableaux[2].pieges[0].setpos((0, 1))
    tableaux[2].sol.append(((0, 500), (1024, 500)))

    tableaux[3].perso = perso
    tableaux[3].fond.append(Fond("fond3.jpg"))
    tableaux[3].fond[0].setpos((dimensions[0] / 2, 0))
    tableaux[3].obstacles.append(Finish(50, 50))
    tableaux[3].obstacles[0].setpos((750, 350))
    tableaux[3].obstacles.append(Caisse())
    tableaux[3].obstacles[1].setpos((650, 400))
    tableaux[3].pieges.append(Flame())
    tableaux[3].pieges[0].setpos((900, 286))
    tableaux[3].sol.append(((0, 500), (300, 500), (650, 500), (1024, 500)))
    tableaux[3].sol.append(((0, 300), (300, 300)))

    #on regroupe les objets dans obstacles
    obstacles = tableaux[actif].obstacles + tableaux[actif].pieges + tableaux[actif].enemies
    #gestion des plateformes
    tableaux[actif].plateforme()
    perso.sol = tableaux[actif].segment
    perso.plate()
    continu = True
    space = False
    while continu:
        #boucle pricipale
        white = (50, 50, 50)
        font = pygame.font.Font(None, 20)

        #affichage du timer
        text = font.render("%s  s" % (timer / 1000), 1, white)
        window.blit(text, (10, 10))
        pygame.display.flip()

        clock.tick(60)

        for event in pygame.event.get():
            #gestion des evenement pygame  (touches + quit)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and space == False:
                    perso.deplacement(dir="haut", val=15)
                    space = True
                if event.key == pygame.K_SPACE and space == False:
                    pygame.mixer.Channel(0).play(son_saut)
                    perso.deplacement(dir="haut", val=15)
                    space = True
                if event.key == pygame.K_RIGHT:
                    perso.deplacement(dir="droite", val=1.3)
                if event.key == pygame.K_LEFT:
                    perso.deplacement(dir="gauche", val=1.3)
            if event.type == QUIT:
                continu = False

        if perso.ay == 0:
            space = False
        collision = False
        perso.c_right = perso.c_left = perso.c_top = False

        for obstacle in obstacles:
            #gestion de collisions avec chaque objetes du tableau
            coll, mort, finish = perso.colision(obstacle)
            print("coll,mort = %d/%d" % (coll, mort))
            if mort:
                pygame.mixer.Channel(0).play(son_mort)
                window.blit(game, (0, 0))
                pygame.display.flip()
                time.sleep(1)
                pygame.mixer.music.stop()

                perso.ax = 0
                perso.ay = 0
                perso.setpos()
                pygame.mixer.music.play(-1)
            elif finish:
                actif += 1
                pygame.mixer.Channel(0).play(son_fin)
                if actif > nombre_tableaux - 1:
                    END(timer)
                    pygame.quit()




                else:
                    print("")
                    jeu(reference_timer, actif)
            elif coll:
                collision = True

        if space:
            perso.c_right = perso.c_left  =False

        if collision:
            print("aie")


        #mise a jour du timer
        timer = pygame.time.get_ticks() - reference_timer
        #mise a jour du tableau actif
        tableaux[actif].update(timer, window)
        tableaux[actif].dessin()

    pygame.quit()

def menu_jeu():
    """
    Cette fait le menu du jeu
    :return:
    """
    #fonction qui s'occpue du menu du jeu
    #creation de la fenetre
    pygame.init()
    window = pygame.display.set_mode(dimensions2)
    #definition des polices d'ecriture
    Font = pygame.font.SysFont("comicsansms", 76)
    font = pygame.font.SysFont("comicsansms", 42)
    #gestion de la musique
    pygame.mixer.music.load("sound/musique.mp3")
    pygame.mixer.music.play(-1)
    #on cache la souris
    pygame.mouse.set_visible(1)
    #creation des textes que l'on va ecrire plus tard
    text = Font.render("Little Adventure", True, (0, 128, 0))
    text1 = font.render("Play", True, (0, 128, 0))
    textr1 = font.render("Play", True, (128, 0, 0))
    text2 = font.render("Quit", True, (0, 128, 0))
    textr2 = font.render("Quit", True, (128, 0, 0))
    text3 = font.render("Musique : Off", True, (0, 128, 0))
    textr3 = font.render("Musique : Off", True, (128, 0, 0))
    text4 = font.render("Musique : On", True, (0, 128, 0))
    textr4 = font.render("Musique : On", True, (128, 0, 0))
    #creation de quelque autres variable
    souris_sur_play = False
    souris_sur_quit = False
    souris_sur_musique = False
    musique = True
    run = True

    while run:
        for event in pygame.event.get():
            #gestion des evenements pygame
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False


        #affichage des differents texte en fonction de la souris
        window.fill((255, 255, 255))
        window.blit(text, (400 - text.get_width() // 2, 140 - text.get_height() // 2))
        if souris_sur_play and musique == False:
            window.blit(textr1, (400 - textr1.get_width() // 2, 280 - textr1.get_height() // 2))
            window.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            window.blit(text3, (400 - text3.get_width() // 2, 360 - text3.get_height() // 2))
        elif souris_sur_play and musique == True:
            window.blit(textr1, (400 - textr1.get_width() // 2, 280 - textr1.get_height() // 2))
            window.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            window.blit(text4, (400 - text4.get_width() // 2, 360 - text4.get_height() // 2))
        elif souris_sur_quit and musique == False:
            window.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            window.blit(textr2, (400 - textr2.get_width() // 2, 440 - textr2.get_height() // 2))
            window.blit(text3, (400 - text3.get_width() // 2, 360 - text3.get_height() // 2))
        elif souris_sur_quit and musique == True:
            window.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            window.blit(textr2, (400 - textr2.get_width() // 2, 440 - textr2.get_height() // 2))
            window.blit(text4, (400 - text4.get_width() // 2, 360 - text4.get_height() // 2))
        elif souris_sur_musique and musique == False:
            window.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            window.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            window.blit(textr3, (400 - textr3.get_width() // 2, 360 - textr3.get_height() // 2))
        elif souris_sur_musique and musique == True:
            window.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            window.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            window.blit(textr4, (400 - textr4.get_width() // 2, 360 - textr4.get_height() // 2))
        elif musique == True:
            window.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            window.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            window.blit(text4, (400 - text4.get_width() // 2, 360 - text4.get_height() // 2))
        elif musique == False:
            window.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            window.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            window.blit(text3, (400 - text3.get_width() // 2, 360 - text3.get_height() // 2))

        #creation des rectangle qui servent de bouttons
        ButtonPlay = pygame.draw.rect(window, (255, 255, 255),
                                      pygame.Rect(400 - text1.get_width() // 2, 280 - text1.get_height() // 2,
                                                  text1.get_width(), text1.get_height()), 1)
        ButtonQuit = pygame.draw.rect(window, (255, 255, 255),
                                      pygame.Rect(400 - text2.get_width() // 2, 440 - text2.get_height() // 2,
                                                  text2.get_width(), text2.get_height()), 1)
        ButtonMusique = pygame.draw.rect(window, (255, 255, 255),
                                         pygame.Rect(400 - text3.get_width() // 2, 360 - text3.get_height() // 2,
                                                     text3.get_width(), text3.get_height()), 1)
        ButtonMusique1 = pygame.draw.rect(window, (255, 255, 255),
                                          pygame.Rect(400 - text4.get_width() // 2, 360 - text4.get_height() // 2,
                                                      text4.get_width(), text3.get_height()), 1)
        pygame.display.flip()


        #test de collision avec les differents bouttons
        if ButtonPlay.collidepoint(pygame.mouse.get_pos()):
            # window.blit(textr1,(512 - textr1.get_width() // 2, 280 - textr1.get_height() // 2))
            souris_sur_play = True
            pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                reference_timer = pygame.time.get_ticks()
                jeu(reference_timer, 0)

        else:
            souris_sur_play = False

        if ButtonMusique.collidepoint(pygame.mouse.get_pos()) and ButtonMusique1.collidepoint(pygame.mouse.get_pos()):
            souris_sur_musique = True
            pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if musique == True:
                    musique = False
                    pygame.mixer.music.pause()  # Met la musique en pause


                else:
                    musique = True
                    pygame.mixer.music.unpause()  # Reprend la musique là où elle a été coupée
        else:
            souris_sur_musique = False

        if ButtonQuit.collidepoint(pygame.mouse.get_pos()):
            souris_sur_quit = True
            pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                run = False
        else:
            souris_sur_quit = False
    pygame.quit()


def END(timer):
    """
    Cette fonction s'occupe de la fin du jeu
    :param timer: le temps que le joueur a mis pour finir le jeu
    :return:
    """
    pygame.init()
    window = pygame.display.set_mode(dimensions2)
    pygame.mouse.set_visible(1)

    pygame.display.set_caption("VIDE")
    Bouton_replay = Button.Button('Rejouer ?', 200, 40, (100, 600), 5)
    Bouton_quit = Button.Button('Fuir ?', 200, 40, (500, 600), 5)
    visionage = True
    while visionage:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                visionage = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                visionage = False

        grey = (50, 50, 50)
        white = (255, 255, 255)
        window.fill(white)
        font = pygame.font.Font(None, 50)
        text1 = font.render("Bravo vous avez terminé en %s seconde " % (timer / 1000), 1, grey)
        window.blit(text1, (50, 300))
        text2 = font.render("votre record est 0,000 seconde", 1, grey)
        window.blit(text2, (100, 400))

        Bouton_quit.draw(window)
        Bouton_replay.draw(window)
        if Bouton_replay.pressed == True:
            menu_jeu()
        if Bouton_quit.pressed == True:
            visionage = False

        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    menu_jeu()