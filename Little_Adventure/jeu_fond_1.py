import pygame
import time
import random
from math import pi
import os
from pygame.locals import *

dimensions = (1024, 574)
dimensions2 = (800, 800)


# main_dir = os.path.split(os.path.abspath(__file__))[0]

class Button:
    def __init__(self, text, width, height, pos, elevation):

        gui_font = pygame.font.Font(None, 30)
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, fenetre):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(fenetre, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(fenetre, self.top_color, self.top_rect, border_radius=12)
        fenetre.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    print('click')
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'


def load_image(name, scalex, scaley, colorkey=None):
    image = pygame.image.load("img/%s"%(name))
    image = image.convert()
    print("image <%s> rect %s" % (name, image.get_rect()))
    bx, by, dimx, dimy = image.get_rect()
    ratiox, ratioy = scalex / dimx, scaley / dimy
    ratiom = min(ratiox, ratioy)
    scalex, scaley = int(dimx * ratiom), int(dimy * ratiom)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    image = pygame.transform.scale(image, (scalex, scaley))
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    # print("main_dir = %s"%(main_dir))
    # fullname = os.path.join(main_dir, name)
    # print("fullname=%s"%(fullname))
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error:
        print('Cannot load sound: %s' % name)
        raise SystemExit(str(pygame.get_error()))
    return sound


class Perso(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_1, self.rect_1 = load_image(name='perso_3.png', scalex=100, scaley=100, colorkey=-1)
        self.image_2, self.rect_2 = load_image(name='perso_1.png', scalex=100, scaley=100, colorkey=-1)
        self.image, self.rect = self.image_1, self.rect_1
        #  print ("image <%s> rect %s" %('perso_3.png',self.rect))
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

    def update(self):
        if self.ay > .015:
            self.ay = self.ay - .01
        elif self.ay < -.015:
            self.ay = self.ay + .01
        else:
            self.ay = 0

        if self.ax > .075:
            self.ax = self.ax - .05
        elif self.ax < -.075:
            self.ax = self.ax + .05
        else:
            self.ax = 0

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

        if self.c_top and self.ay < 0:
            self.ay = 0
        elif self.c_right and self.ax > 0:
            self.ax = 0
        elif self.c_left and self.ax < 0:
            self.ax = 0
        #  print("update xy=%6.2lf/%6.2lf ax/ay=%6.2lf/%6.2lf"%(self.x,self.y,self.ax,self.ay))
        self.y -= self.ay
        self.x += self.ax
        if not self.ay == 0:
            self.ay -= 0.5
        if self.ay > 30:
            self.ay = 30
        elif self.ay < -30:
            self.ay = -30

        if self.ax > 6:
            self.ax = 6
        elif self.ax < -6:
            self.ax = -6
            # if self.y < 451:
        #  self.ay-=.5
        # elif self.y == 451 and self.ay<=0:
        #  self.ay = 0
        # elif self.y > 451:
        #  self.y = 451
        #  self.ay = 0
        if self.y < 0:
            self.ay -= 1.5
        if self.x < 0:
            self.x = 0
            self.ax = -self.ax
        elif self.x > 1024:
            self.x = 1024
            self.ax = -self.ax

        # print("h=%s l=%s"%(str(self.h),str(self.l)))

        if self.ax < 0 and self.flip == False:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flip = True
        elif self.ax > 0 and self.flip == True:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flip = False

        if self.compteur == 10:
            self.compteur = 0
            if not self.ax == 0:
                if self.image_mem == self.image_1:
                    self.image = self.image_2
                    self.flip = False
                    self.image_mem = self.image_2
                elif self.image_mem == self.image_2:
                    self.image = self.image_1
                    self.image_mem = self.image_1
                    self.flip = False
        self.compteur += 1
        #  print("le compteur est a %s"%(self.compteur))

        self.pos = (self.x, self.y)
        self.rect.midtop = self.pos
        # print("le sol est :%s"%(self.sol))

    def setpos(self, pos=(500, 0)):
        self.ax = self.ay = 0
        self.x, self.y = pos
        self.pos = pos
        self.rect.midtop = self.pos

    #  print("setpos xy=%6.2lf/%6.2lf ax/ay=%6.2lf/%6.2lf"%(self.x,self.y,self.ax,self.ay))

    def colision(self, cible):
        hitbox = self.rect  # .inflate(-100, -100)
        mort = False
        collision = False
        fin = False
        ciblex = cible.rect[0]
        cibley = cible.rect[1]
        ciblelong = cible.rect[2]
        ciblehaut = cible.rect[3]

        # self.c_right = self.c_left = self.c_top = False

        if self.rect[0]:
            rect2 = cible.rect
            # print ("ciblex=%s,cibley=%s,ciblelong=%s,ciblehaut=%s,self.l=%s,self.h=%s"%(str(ciblex),str(cibley),str(ciblelong),str(ciblehaut),str(self.l-62.5),str(self.h-62.5)))
            self.c = hitbox.colliderect(cible.rect)
            # print ("coll (%s) vs. (%s) : %s" %(str(hitbox),str(cible.rect),str(self.c)))
            # print("test colision avec %s:%s"%(str(hitbox),str(rect2)))
            if not self.c:
                rect2 = rect2.inflate(1, 1)
                r2 = hitbox.colliderect(rect2)
                # print("+new colision avec %s:%s :%s"%(str(hitbox),str(rect2),str(r2)))
                if r2:
                    #        print("CONTACT")
                    collision = True
            else:
                collision = True
                # print("colision avec %s"%(str(cible)))
                mort = cible.mortelle()
                fin = cible.finish()
                if self.rect[0] + self.rect[2] <= ciblex + 20:
                    #        print("je suis a droite")
                    self.c_right = True
                elif self.rect[0] >= ciblex + ciblelong - 20:
                    #        print("je suis a gauche")
                    self.c_left = True
                # else :
                #  self.c_right=False
                #  self.c_left=False
                if self.rect[1] + self.rect[3] <= cibley + 20:
                    #        print("je suis au dessus")
                    self.c_top = True
                # else:
                #  self.c_top=False

                # elif self.rect[1]>=cibley:
                #  print("cas 4")
        return collision, mort, fin

    def deplacement(self, dir, val):
        if dir == "droite":
            self.ax += val
        elif dir == "gauche":
            self.ax -= val
        elif dir == "haut":
            self.ay += val
        elif dir == "bas":
            self.ay += val
        self.update()

    def plate(self):
        for seg in self.sol:
            segxdebut = seg[0][0]
            segxfin = segxdebut + seg[1][0]
            segydebut = seg[0][1]
            segyfin = segydebut + seg[1][1]
            #    print("seg= %s %s %s %s  "%(segxdebut,segxfin,segydebut,segyfin))
            self.plateforme.append((segxdebut, segxfin, segydebut, segyfin))


class Fond(pygame.sprite.Sprite):
    def __init__(self, nom):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name='%s' % (nom), scalex=dimensions[0], scaley=dimensions[1], colorkey=-1)

    def update(self):
        self.rect.midtop = self.pos

    def setpos(self, pos):
        self.pos = pos
        self.rect.midtop = self.pos

    def mortelle(self):
        return False

    def finish(self):
        return False


class Caisse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name='caisse.png', scalex=100, scaley=100, colorkey=-1)

    def update(self):
        self.rect.midtop = self.pos

    def setpos(self, pos):
        self.pos = pos
        self.rect.midtop = self.pos

    def mortelle(self):
        return False

    def finish(self):
        return False


class Flame(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name='flame.png', scalex=50, scaley=100, colorkey=-1)

    def update(self):
        self.rect.midtop = self.pos

    def setpos(self, pos):
        self.pos = pos
        self.rect.midtop = self.pos

    def mortelle(self):
        return True

    def finish(self):
        return False


class Enemies(pygame.sprite.Sprite):
    def __init__(self):
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
        # print("la vitesse en x est %s et celle en y est %s"%(self.speedx,self.speedy))
        if self.sens <= "trigo":
            # print("les coordonnes de la flame sont (%s,%s)"%(self.pos[0],self.pos[1]))
            if self.limhg[0] - 5 <= self.pos[0] <= self.limhg[0] + 5 and self.limhg[1] - 5 <= self.pos[1] <= self.limhg[
                1] + 5:
                if self.speedx < 0:
                    self.speedy = -self.speedx
                else:
                    self.speedy = self.speedx
                self.speedx = 0
                # print("la vitesse en x est %s et celle en y est %s"%(self.speedx,self.speedy))
            elif self.limbg[1] - 5 <= self.pos[1] <= self.limbg[1] + 5 and self.limbg[0] - 5 <= self.pos[0] <= \
                    self.limbg[0] + 5:
                self.speedx = self.speedy
                self.speedy = 0
                # print("la vitesse en x est %s et celle en y est %s"%(self.speedx,self.speedy))
            elif self.limbd[0] - 5 <= self.pos[0] <= self.limbd[0] + 5 and self.limbd[1] - 5 <= self.pos[1] <= \
                    self.limbd[1] + 5:
                self.speedy = -self.speedx
                self.speedx = 0
                # print("la vitesse en x est %s et celle en y est %s"%(self.speedx,self.speedy))
            elif self.limhd[1] - 5 <= self.pos[1] <= self.limhd[1] + 5 and self.limhd[0] - 5 <= self.pos[0] <= \
                    self.limhd[0] + 5:
                self.speedx = self.speedy
                self.speedy = 0
                # print("la vitesse en x est %s et celle en y est %s"%(self.speedx,self.speedy))
            elif self.limhg[0] + 5 <= self.pos[0] <= self.limhd[0] - 5 and self.limhg[1] + 5 <= self.pos[1] <= \
                    self.limhg[1] - 5:
                if self.speedx > 0:
                    self.speedx = -self.speedx
                self.speedy = 0
                # print("la vitesse en x est %s et celle en y est %s"%(self.speedx,self.speedy))
            elif self.limhg[1] + 5 <= self.pos[1] <= self.limbg[1] - 5 and self.limhg[0] + 5 <= self.pos[0] <= \
                    self.limhg[0] - 5:
                if self.speedy < 0:
                    self.speedy = -self.speedy
                self.speedx = 0
                # print("la vitesse en x est %s et celle en y est %s"%(self.speedx,self.speedy))
            elif self.limbg[0] + 5 <= self.pos[0] <= self.limbd[0] - 5 and self.limbd[1] + 5 <= self.pos[1] <= \
                    self.limbd[1] - 5:
                if self.speedx < 0:
                    self.speedx = -self.speedx
                self.speedy = 0
                # print("la vitesse en x est %s et celle en y est %s"%(self.speedx,self.speedy))
            elif self.limhd[1] + 5 <= self.pos[1] <= self.limbd[1] - 5 and self.limbd[0] + 5 <= self.pos[0] <= \
                    self.limbd[0] - 5:
                if self.speedy > 0:
                    self.speedy = -self.speedy
                self.speedx = 0
                # print("la vitesse en x est %s et celle en y est %s"%(self.speedx,self.speedy))


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
        return True

    def finish(self):
        return False


class Finish(pygame.sprite.Sprite):
    def __init__(self, long, largeur):
        self.finis = False
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name='finish.png', scalex=largeur, scaley=long, colorkey=-1)

    def update(self):
        self.rect.midtop = self.pos

    def setpos(self, pos):
        self.pos = pos
        self.rect.midtop = self.pos

    def mortelle(self):
        return False

    def finish(self):
        return True


class Obstacle_rebond(pygame.sprite.Sprite):
    def __init__(self, vx=10, vy=10):
        pygame.sprite.Sprite.__init__(self)
        # self.image, self.rect = load_image(name='163.jpg',scalex=50,scaley=100,colorkey=-1)
        self.image, self.rect = load_image(name='hot-fireball-60.png', scalex=60, scaley=60, colorkey=-1)
        self.ax = vx
        self.ay = vy

    def update(self):
        # self.pos[0]=self.pos[0]+ax
        # self.pos[1]=self.pos[1]+ay
        nposx, nposy = self.pos[0] + self.ax, self.pos[1] + self.ay
        if nposx <= 0:
            nposx = 0
            self.ax = -self.ax + random.randint(-1, 1)
        elif nposx > 1024:
            nposx = 1024
            self.ax = -self.ax + random.randint(-1, 1)
        if nposy <= 0:
            nposy = 0
            self.ay = -self.ay + random.randint(-1, 1)
        elif nposy > 576:
            nposy = 576
            self.ay = -self.ay + random.randint(-1, 1)
        self.pos = (nposx, nposy)
        self.rect.midtop = (nposx, nposy)

    def setpos(self, pos):
        self.pos = pos
        self.rect.midtop = self.pos

    def mortelle(self):
        return True

    def finish(self):
        return False


class Tableau():
    def __init__(self, fenetre, nom):
        self.fenetre = fenetre
        self.nom = nom
        self.perso = None
        self.obstacles = []
        self.pieges = []
        self.enemies = []
        self.sol = []
        self.sprites = []
        self.backgroundcolor = (250, 250, 250)
        self.background = pygame.Surface(self.fenetre.get_size()).convert()
        self.background.fill(self.backgroundcolor)
        self.segment = []
        self.finishbg = []
        self.finishhd = []
        self.finishhg = []
        self.finishbd = []
        self.dim_fin = []
        self.fond = []
        self.sprite_fond = []
        # bg=bas gauche hd=haut droite

    def update(self, timer, fenetre):
        pygame.display.set_caption(self.nom)
        allsprites = self.obstacles + self.pieges + self.enemies + [self.perso]
        self.sprite_fond = pygame.sprite.RenderPlain(self.fond)
        self.sprites = pygame.sprite.RenderPlain(allsprites)
        white = (50, 50, 50)
        font = pygame.font.Font(None, 20)
        text = font.render("%s  s" % (timer / 1000), 1, white)
        fenetre.blit(text, (10, 10))
        pygame.display.flip()

    def dessin(self):
        self.background.fill(self.backgroundcolor)
        self.sprites.update()
        self.perso.update()
        self.fenetre.blit(self.background, (0, 0))
        for polyline in self.sol:
            solcolor = (0, 0, 0)
            pygame.draw.lines(self.fenetre, solcolor, False, polyline)
        # Color_line=(0,0,0)
        # Color_line2=(255,0,0)
        # points = [(0, 500), (300, 500), (650, 350), (1024, 350)]
        # plat=pygame.draw.line(fenetre, Color_line2, (0, 300), (300, 300))
        # sol=pygame.draw.lines(fenetre, Color_line, False, points)
        self.sprite_fond.draw(self.fenetre)
        self.sprites.draw(self.fenetre)
        pygame.display.flip()

    def plateforme(self):
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

    def finish(self, reference_timer, actif, nombre_tableaux, son_fin):
        '''
    fin_color=(232, 191, 27)
    #fin_color=(0, 0, 0)
    print("perso.x = %s :self.finishbg[0]= %s :self.finishhd[0]= %s"%(self.perso.x,self.finishbg[0],self.finishhd[0]))
    print("perso.y = %s :self.finishbg[1]= %s :self.finishhd[1]= %s"%(self.perso.y,self.finishbg[1],self.finishhd[1]))
    for point in self.dim_fin:
      pygame.draw.lines(self.fenetre,fin_color,True,point)
    pygame.display.flip()
    if self.finishbg[0]-10<=self.perso.x<=self.finishhd[0]+10 and self.finishhd[1]-10<=self.perso.y+100<=self.finishbg[1]+10:
      actif+=1
      pygame.mixer.Channel(0).play(son_fin)
      if actif > nombre_tableaux-1 :
        actif=0
      jeu(reference_timer,actif)
      '''
        '''
    if Finish.finish == True :
      actif+=1
      pygame.mixer.Channel(0).play(son_fin)
      if actif > nombre_tableaux-1 :
        actif=0
      jeu(reference_timer,actif)
    '''


# self.finishbg
# self.finishhd

def jeu(reference_timer, actif=0):
    timer = pygame.time.get_ticks() - reference_timer
    print(
        "###########################\n###########################\n###########################\n###########################\n")
    print("le temps ecoule est %s s" % (timer / 1000))
    print(
        "###########################\n###########################\n###########################\n###########################\n")
    mort = False
    fin = False
    pygame.init()
    fenetre = pygame.display.set_mode(dimensions)
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
    # background = pygame.Surface(fenetre.get_size())
    # background = background.convert()
    # background.fill((250, 250, 250))

    # animation
    clock = pygame.time.Clock()

    # fenetre.blit(background, (0, 0))
    # pygame.display.flip()
    pygame.key.set_repeat(100, 30)

    # tableau
    tableaux = []
    tableaux.append(Tableau(fenetre, "premier tableau"))
    tableaux.append(Tableau(fenetre, "deuxieme tableau"))
    tableaux.append(Tableau(fenetre, "troisieme tableau"))
    tableaux.append(Tableau(fenetre, "quatrieme tableau"))
    nombre_tableaux = len(tableaux)

    #
    perso = Perso()
    perso.setpos()

    tableaux[0].perso = perso
    tableaux[0].enemies.append(Enemies())
    tableaux[0].enemies[0].setpos((0, 0), (0, 0), (0, 576), (1024, 576), (1024, 0), 10, "trigo")
    tableaux[0].fond.append(Fond("fond.png"))
    tableaux[0].fond[0].setpos((dimensions[0] / 2, 0))
    tableaux[0].obstacles.append(Finish(50, 50))
    tableaux[0].obstacles[0].setpos((100, 200))
    tableaux[0].dim_fin.append(((0, 576), (0, 0), (200, 0), (200, 576)))
    tableaux[0].sol.append(((0, 500), (1024, 500)))

    tableaux[1].perso = perso
    tableaux[1].fond.append(Fond("fond.png"))
    tableaux[1].fond[0].setpos((dimensions[0] / 2, 0))
    tableaux[1].obstacles.append(Finish(50, 50))
    tableaux[1].obstacles[0].setpos((100, 200))
    tableaux[1].obstacles.append(Caisse())
    tableaux[1].obstacles[1].setpos((230, 401))
    tableaux[1].pieges.append(Obstacle_rebond(vx=10, vy=7))
    tableaux[1].pieges[0].setpos((40, 40))
    tableaux[1].finishbg = (0, 576)
    tableaux[1].finishhd = (200, 0)
    tableaux[1].finishhg = (0, 0)
    tableaux[1].finishbd = (200, 576)
    tableaux[1].dim_fin.append(((0, 576), (0, 0), (200, 0), (200, 576)))
    tableaux[1].sol.append(((0, 500), (1024, 500)))

    tableaux[2].perso = perso
    tableaux[2].fond.append(Fond("fond.png"))
    tableaux[2].fond[0].setpos((dimensions[0] / 2, 0))
    tableaux[2].obstacles.append(Finish(50, 50))
    tableaux[2].obstacles[0].setpos((100, 200))
    tableaux[2].obstacles.append(Caisse())
    tableaux[2].obstacles[1].setpos((230, 401))
    tableaux[2].pieges.append(Flame())
    tableaux[2].pieges[0].setpos((800, 401))
    tableaux[2].finishbg = (824, 576)
    tableaux[2].finishhd = (1024, 0)
    tableaux[2].finishhg = (824, 0)
    tableaux[2].finishbd = (1024, 576)
    tableaux[2].dim_fin.append(((824, 576), (824, 0), (1024, 0), (1024, 576)))
    tableaux[2].sol.append(((0, 500), (1024, 500)))

    tableaux[3].perso = perso
    tableaux[3].fond.append(Fond("fond2.png"))
    tableaux[3].fond[0].setpos((dimensions[0] / 2, 0))
    tableaux[3].obstacles.append(Finish(50, 50))
    tableaux[3].obstacles[0].setpos((100, 200))
    tableaux[3].obstacles.append(Caisse())
    tableaux[3].obstacles[1].setpos((180, 201))
    # tableaux30].obstacles[1].setpos((180,476))
    tableaux[3].pieges.append(Flame())
    tableaux[3].pieges[0].setpos((900, 286))
    # tableaux30].sol.append(((0, 500), (300, 500), (400, 200), (650, 350), (1024, 350)))
    tableaux[3].sol.append(((0, 500), (300, 500), (650, 340), (1024, 340)))
    tableaux[3].sol.append(((0, 300), (300, 300)))
    tableaux[3].finishbg = (130, 201)
    tableaux[3].finishhd = (230, 0)
    tableaux[3].finishhg = (130, 0)
    tableaux[3].finishbd = (230, 201)
    tableaux[3].dim_fin.append(((130, 201), (130, 0), (230, 0), (230, 201)))

    obstacles = tableaux[actif].obstacles + tableaux[actif].pieges + tableaux[actif].enemies
    tableaux[actif].plateforme()
    perso.sol = tableaux[actif].segment
    perso.plate()
    continu = True
    space = False
    while continu:
        white = (50, 50, 50)
        font = pygame.font.Font(None, 20)
        text = font.render("%s  s" % (timer / 1000), 1, white)
        fenetre.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and space == False:
                    perso.deplacement(dir="haut", val=15)
                    space = True
                if event.key == pygame.K_SPACE and space == False:
                    pygame.mixer.Channel(0).play(son_saut)
                    perso.deplacement(dir="haut", val=15)
                    space = True
                if event.key == pygame.K_RIGHT:
                    perso.deplacement(dir="droite", val=2)
                if event.key == pygame.K_LEFT:
                    perso.deplacement(dir="gauche", val=2)
                # if event.key==pygame.K_DOWN:
                #  tableaux[actif].finish(actif,nombre_tableaux)
            if event.type == QUIT:
                continu = False

        if perso.ay == 0:
            space = False
        collision = False
        perso.c_right = perso.c_left = perso.c_top = False

        for obstacle in obstacles:
            coll, mort, finish = perso.colision(obstacle)
            print("coll,mort = %d/%d" % (coll, mort))
            if mort:
                pygame.mixer.Channel(0).play(son_mort)
                fenetre.blit(game, (0, 0))
                pygame.display.flip()
                # continuer=False
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
            perso.c_right = perso.c_left = perso.c_top = False

        if collision:
            print("aie")
            # tableaux[0].backgroundcolor=(250, 250, 250) if not tableaux[0].backgroundcolor==(250, 250, 250) else (250, 150, 150)

        timer = pygame.time.get_ticks() - reference_timer
        tableaux[actif].update(timer, fenetre)
        tableaux[actif].dessin()
        tableaux[actif].finish(reference_timer, actif, nombre_tableaux, son_fin)
        # allsprites.update()
        # perso.update()
        # fenetre.blit(background, (0, 0))
        # Color_line=(0,0,0)
        # Color_line2=(255,0,0)
        # points = [(0, 500), (300, 500), (650, 350), (1024, 350)]
        # plat=pygame.draw.line(fenetre, Color_line2, (0, 300), (300, 300))
        # sol=pygame.draw.lines(fenetre, Color_line, False, points)
        ##pygame.draw.arc(fenetre, Color_line, fenetre.get_rect(), 0, pi)
        # allsprites.draw(fenetre)
        # pygame.display.flip()
    pygame.quit()

def menu_jeu():
    pygame.init()
    fenetre = pygame.display.set_mode(dimensions2)
    Font = pygame.font.SysFont("comicsansms", 76)
    font = pygame.font.SysFont("comicsansms", 42)
    pygame.mixer.music.load("sound/musique.mp3")
    pygame.mixer.music.play(-1)
    pygame.mouse.set_visible(1)

    text = Font.render("Little Adventure", True, (0, 128, 0))
    text1 = font.render("Play", True, (0, 128, 0))
    textr1 = font.render("Play", True, (128, 0, 0))
    text2 = font.render("Quit", True, (0, 128, 0))
    textr2 = font.render("Quit", True, (128, 0, 0))
    text3 = font.render("Musique : Off", True, (0, 128, 0))
    textr3 = font.render("Musique : Off", True, (128, 0, 0))
    text4 = font.render("Musique : On", True, (0, 128, 0))
    textr4 = font.render("Musique : On", True, (128, 0, 0))
    souris_sur_play = False
    souris_sur_quit = False
    souris_sur_musique = False
    musique = True
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False

        fenetre.fill((255, 255, 255))
        fenetre.blit(text, (400 - text.get_width() // 2, 140 - text.get_height() // 2))
        if souris_sur_play and musique == False:
            fenetre.blit(textr1, (400 - textr1.get_width() // 2, 280 - textr1.get_height() // 2))
            fenetre.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            fenetre.blit(text3, (400 - text3.get_width() // 2, 360 - text3.get_height() // 2))
        elif souris_sur_play and musique == True:
            fenetre.blit(textr1, (400 - textr1.get_width() // 2, 280 - textr1.get_height() // 2))
            fenetre.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            fenetre.blit(text4, (400 - text4.get_width() // 2, 360 - text4.get_height() // 2))
        elif souris_sur_quit and musique == False:
            fenetre.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            fenetre.blit(textr2, (400 - textr2.get_width() // 2, 440 - textr2.get_height() // 2))
            fenetre.blit(text3, (400 - text3.get_width() // 2, 360 - text3.get_height() // 2))
        elif souris_sur_quit and musique == True:
            fenetre.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            fenetre.blit(textr2, (400 - textr2.get_width() // 2, 440 - textr2.get_height() // 2))
            fenetre.blit(text4, (400 - text4.get_width() // 2, 360 - text4.get_height() // 2))
        elif souris_sur_musique and musique == False:
            fenetre.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            fenetre.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            fenetre.blit(textr3, (400 - textr3.get_width() // 2, 360 - textr3.get_height() // 2))
        elif souris_sur_musique and musique == True:
            fenetre.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            fenetre.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            fenetre.blit(textr4, (400 - textr4.get_width() // 2, 360 - textr4.get_height() // 2))
        elif musique == True:
            fenetre.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            fenetre.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            fenetre.blit(text4, (400 - text4.get_width() // 2, 360 - text4.get_height() // 2))
        elif musique == False:
            fenetre.blit(text1, (400 - text1.get_width() // 2, 280 - text1.get_height() // 2))
            fenetre.blit(text2, (400 - text2.get_width() // 2, 440 - text2.get_height() // 2))
            fenetre.blit(text3, (400 - text3.get_width() // 2, 360 - text3.get_height() // 2))
        ButtonPlay = pygame.draw.rect(fenetre, (255, 255, 255),
                                      pygame.Rect(400 - text1.get_width() // 2, 280 - text1.get_height() // 2,
                                                  text1.get_width(), text1.get_height()), 1)
        ButtonQuit = pygame.draw.rect(fenetre, (255, 255, 255),
                                      pygame.Rect(400 - text2.get_width() // 2, 440 - text2.get_height() // 2,
                                                  text2.get_width(), text2.get_height()), 1)
        ButtonMusique = pygame.draw.rect(fenetre, (255, 255, 255),
                                         pygame.Rect(400 - text3.get_width() // 2, 360 - text3.get_height() // 2,
                                                     text3.get_width(), text3.get_height()), 1)
        ButtonMusique1 = pygame.draw.rect(fenetre, (255, 255, 255),
                                          pygame.Rect(400 - text4.get_width() // 2, 360 - text4.get_height() // 2,
                                                      text4.get_width(), text3.get_height()), 1)
        pygame.display.flip()

        if ButtonPlay.collidepoint(pygame.mouse.get_pos()):
            # fenetre.blit(textr1,(512 - textr1.get_width() // 2, 280 - textr1.get_height() // 2))
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
            # fenetre.blit(textr2,(512 - textr2.get_width() // 2, 360 - textr2.get_height() // 2))
            souris_sur_quit = True
            pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                run = False
        else:
            souris_sur_quit = False
    pygame.quit()


def END(timer):
    pygame.init()
    fenetre = pygame.display.set_mode(dimensions2)
    pygame.mouse.set_visible(1)

    pygame.display.set_caption("VIDE")
    Bouton_replay = Button('Rejouer ?', 200, 40, (100, 600), 5)
    Bouton_quit = Button('Fuir ?', 200, 40, (500, 600), 5)
    visionage = True
    while visionage:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                visionage = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                visionage = False

        grey = (50, 50, 50)
        white = (255, 255, 255)
        fenetre.fill(white)
        font = pygame.font.Font(None, 50)
        text1 = font.render("Bravo vous avez terminé en %s seconde " % (timer / 1000), 1, grey)
        fenetre.blit(text1, (50, 300))
        text2 = font.render("votre record est 0,000 seconde", 1, grey)
        fenetre.blit(text2, (100, 400))

        Bouton_quit.draw(fenetre)
        Bouton_replay.draw(fenetre)
        if Bouton_replay.pressed == True:
            menu_jeu()
        if Bouton_quit.pressed == True:
            visionage = False

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    # main(0)
    menu_jeu()