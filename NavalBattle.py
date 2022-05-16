#-*- coding: UTF-8 -*-
#@tobias wendl

import pygame
from pygame import*
import Button
from Button import*
import time

class Piece:

    def __init__(self, xPos, yPos, type):

        self.player = 0     # 0-> n appartient a aucun joueur
        self.pos = (xPos, yPos)
        self.corpse = []  #corps du navire
        self.listRect = []
        self.size = 0
        self.type = type #string qui définit le type de la piece
        self.frame = False
        self.collision = False
        self.placed = False

        #permet de compter le nombre de pieces d'un type donné
        #attribut utilisé lors du placement des pieces
        self.counter = 1
        #on init la taille en fct du type
        if type == "porte avion":
            self.size = 5

        elif type == "croiseur":
            self.size = 4

        elif type == "contre torpilleur":
            self.size = 3
            self.counter = 2

        elif type == "torpilleur":
            self.size = 2

        #on init la liste qui sert de corps au navire
        #on init à 0
        #0 représente gris
        #1 représente rouge --> navire touché
        for i in range(self.size):
            self.corpse.append(0)


    def display(self, window):
        """permet d'afficher les pièces"""
        font = pygame.font.SysFont("comicsans", 30, True)
        color = (135, 138, 136)
        xPos, yPos = self.pos[0], self.pos[1]
        for i in range(self.size):
            ship = pygame.Rect(xPos, yPos, 30, 30)
            self.listRect.append(ship)
            pygame.draw.rect(window, color, ship)
            xPos += 31
        var_text = str(self.type + " : x" + str(self.counter))
        text = font.render(var_text, 1, (255, 255, 255))
        window.blit(text, (self.pos[0], self.pos[1]-50))

    def check_click(self, window):
        """permet de tester si une piece a ete cliqué"""
        mouseX, mouseY = pygame.mouse.get_pos()
        color = (53, 16, 235)
        for i in range(len(self.listRect)):
            if self.listRect[i].collidepoint((mouseX, mouseY)):
                self.collision = True
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        print("piece clicked")
                        self.frame = True

        if self.frame:
            rect_frame = pygame.Rect(self.pos[0], self.pos[1], self.size * 30 + self.size, 32)
            #place un cadre autour de la piece cliquée
            pygame.draw.rect(window, color, rect_frame, 2)

class Grid:
    def __init__(self, xPos, yPos):
        self.size = (10, 10)
        self.grid = []
        for i in range(self.size[0]):
            self.grid.append([])
            for j in range(self.size[1]):
                self.grid[i].append(0)
        self.pos = (xPos, yPos)
        self.listRect = []

    def display(self, window):
        """affichage de la grille de jeu
            Les 0 représentent une case vide
            Les 1 représente une case avec un navire
            Les 2 représentent une case vide touchée
            Les 3 representent une case avec un navire touchée"""

        q = 0
        yPos = self.pos[1]
        for j in range(self.size[0]):
            xPos = self.pos[0]
            for k in range(self.size[1]):
                switcher = {
                    0: (255, 255, 255),
                    1: (135, 138, 136),
                    2: (0, 0, 0),
                    3: (255, 0, 0)
                }
                self.listRect.append(pygame.Rect(xPos, yPos, 30, 30))
                color = switcher.get(self.grid[j][k], (0, 255, 0))
                pygame.draw.rect(window, color, self.listRect[q])
                xPos += 31
                q += 1
            yPos += 31
        return color

    def placement(self, window, size):
        """permet de placer les navires sur la grille"""
        mouseX, mouseY = pygame.mouse.get_pos()
        placed = False
        for i in range(len(self.listRect)):
            if self.listRect[i].collidepoint((mouseX, mouseY)):
                #on sauvegarde la variable i en utilisant une variable m
                m = i

                for j in range(size):

                    if m < len(self.listRect):
                        pygame.draw.rect(window, (59, 199, 44), self.listRect[m], 2)
                        m += 1
                    else:
                        pygame.draw.rect(window, (59, 199, 44), self.listRect[m-size], 2)
                        m -= size-1
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        #la boucle for suivante permet de changer la couleur de tous les rect sélectionnés
                        #ex: torpilleur sélectionné --> 2 cases coloriées
                        for l in range(size):
                            if i < len(self.listRect):
                                j = i // 10
                                k = i % 10
                                if self.grid[j][k] == 0:
                                    self.grid[j][k] = 1
                                    print(self.grid)
                                    i += 1
                                    placed = True
                            else:
                                j = (i-size) // 10
                                k = (i-size) % 10
                                if self.grid[j][k] == 0:
                                    self.grid[j][k] = 1
                                    print(self.grid)
                                    i -= size-1
                                    placed = True
                        if placed:
                            return True

def window_refresh(window):
    bg_image = pygame.image.load('img/blue.jpg')
    window.blit(bg_image, (0, 0))

def window_init():
    # initialisation pygame
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("THE NAVAL BATTLE")
    window_refresh(window)
    return window

def Button_creation():
    """creation des bouttons"""
    button1 = Button('Play', 200, 40, (290, 400), 5)
    button2 = Button('How to play', 200, 40, (290, 470), 5)
    button3 = Button('Back to menu', 200, 40, (290, 540), 5)
    button4 = Button('Ready', 200, 40, (290, 600), 5)
    button5 = Button('Back to menu', 200, 40, (290, 670), 5)
    return button1, button2, button3, button4, button5

def grid_creation(xPos, yPos):
    """creation de la grille"""
    grid = Grid(xPos, yPos)
    return grid

def piece_creation(xPos, yPos, type):
    piece = Piece(xPos, yPos, type)
    return piece

def main_NavalBattle():

    window = window_init()

    #intialisation de la fenetre
    window_init()

    #creation du boutton de retour au menu
    button1, button2, button3, button4, button5 = Button_creation()


    #creation des grilles
    #gridB --> grille du joueur adverse
    gridA = grid_creation(50, 200)
    gridB = grid_creation(450, 200)

    #creation des pieces
    torpilleur = piece_creation(400, 200, 'torpilleur')
    contre_torpilleur = piece_creation(400,300, 'contre torpilleur')
    croiseur = piece_creation(400, 400, 'croiseur')
    porte_avion = piece_creation(400, 500, 'porte avion')

    run = True
    menu = True
    play = False
    clock = pygame.time.Clock()
    #variable utilisée pour la méthode placement de la classe Grid
    size = 0

    #loading images
    logo = pygame.image.load('img/logoNV.PNG')
    placeShip = pygame.image.load('img/PlaceShip.PNG')

    while run:
        while menu:
            window_refresh(window)
            window.blit(logo, (245, 70))
            #affichage du boutton sur la fenetre
            button1.draw(window)
            button2.draw(window)
            button3.draw(window)

            if button1.pressed == True:
                print("Play")
                time.sleep(0.2)
                button1.pressed = False
                play = True
                menu = False

            if button2.pressed == True:
                print("how to play")
                time.sleep(0.2)

            if button3.pressed == True :
                print("back to main menu")
                time.sleep(0.2)
                button3.pressed = False
                run = False
                menu = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    menu = False

            pygame.display.update()

        while play:
            window_refresh(window)
            window.blit(placeShip, (110, 0))
            button4.draw(window)
            button5.draw(window)

            #affichage des pieces sur l'ecran
            torpilleur.display(window)
            contre_torpilleur.display(window)
            croiseur.display(window)
            porte_avion.display(window)

            #verifier si on clique les pieces
            torpilleur.check_click(window)
            contre_torpilleur.check_click(window)
            croiseur.check_click(window)
            porte_avion.check_click(window)


            if torpilleur.frame and torpilleur.collision and torpilleur.counter > 0:
                size = 2
                contre_torpilleur.frame = False
                croiseur.frame = False
                porte_avion.frame = False
                torpilleur.collision = False

            if size == 2 and torpilleur.counter == 0:
                size = 0

            if contre_torpilleur.frame and contre_torpilleur.collision:
                size = 3
                torpilleur.frame = False
                croiseur.frame = False
                porte_avion.frame = False
                contre_torpilleur.collision = False

            if size == 3 and contre_torpilleur.counter == 0:
                size = 0

            if croiseur.frame and croiseur.collision:
                size = 4
                torpilleur.frame = False
                contre_torpilleur.frame = False
                porte_avion.frame = False
                croiseur.collision = False

            if size == 4 and croiseur.counter == 0:
                size = 0

            if porte_avion.frame and porte_avion.collision:
                size = 5
                torpilleur.frame = False
                contre_torpilleur.frame = False
                croiseur.frame = False
                porte_avion.collision = False

            if size == 5 and porte_avion.counter == 0:
                size = 0

            #affichage de la grille de jeu
            gridA.display(window)

            placed = gridA.placement(window, size)
            if placed:
                if size == 2:
                    torpilleur.placed = True
                    torpilleur.counter -= 1
                if size == 3:
                    contre_torpilleur.placed = True
                    contre_torpilleur.counter -= 1
                if size == 4:
                    croiseur.placed = True
                    croiseur.counter -= 1
                if size == 5:
                    porte_avion.placed = True
                    porte_avion.counter -= 1

            pygame.display.update()

            gridA.listRect = []

            #on add tous les counter des pièces pour verifier que l'on peut lancer le jeu
            counter = torpilleur.counter + contre_torpilleur.counter + croiseur.counter + porte_avion.counter

            #button ready
            if button4.pressed == True :
                print("ready")
                time.sleep(0.2)
                button4.pressed = False
                #on verifie que tous les navires sont posés avant de lancer le jeu
                if counter == 0:
                    print("you can play")
                else:
                    print("place all your ships")

            #button back to menu
            if button5.pressed == True :
                print("back to menu")
                time.sleep(0.2)
                button5.pressed = False
                play = False
                menu = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    menu = True
            clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
