#-*- coding: UTF-8 -*-

import pygame
from pygame import*
import Button
from Button import*
import time

class Piece:

    def __init__(self, xPos, yPos):
        self.size = 0
        self.player = 0
        self.xPos = xPos
        self.yPos = yPos

    def position(self, xPos, yPos):

        """
        if type == "porte avion":
            self.size = 5

        elif type == "croiseur":
            self.size = 4

        elif type == "contre torpilleur":
            self.size = 3

        elif type == "torpilleur":
            self.size = 2"""

class Grid():
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
                    1: (118, 130, 127),
                    2: (0, 0, 0),
                    3: (255, 0, 0)
                }
                self.listRect.append(pygame.Rect(xPos, yPos, 30, 30))
                color = switcher.get(self.grid[j][k], (0, 255, 0))
                pygame.draw.rect(window, color, self.listRect[q])
                xPos += 31
                q += 1
            yPos += 31
        pygame.display.update()
        return color

    def placement(self, window):
        """permet de placer les navires sur la grille"""
        mouseX, mouseY = pygame.mouse.get_pos()
        for i in range(len(self.listRect)):
            if self.listRect[i].collidepoint((mouseX, mouseY)):
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        j = i//10
                        k = i % 10
                        self.grid[j][k] = 1
                        print(self.grid)


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
    return button1, button2, button3

def grid_creation(xPos, yPos):
    """creation de la grille"""
    grid = Grid(xPos, yPos)
    return grid

def main_NavalBattle():

    window = window_init()

    #intialisation de la fenetre
    window_init()

    #creation du boutton de retour au menu
    button1, button2, button3 = Button_creation()

    gridA = grid_creation(100, 100)


    run = True
    menu = True
    play = False
    clock = pygame.time.Clock()
    logo = pygame.image.load('img/logoNV.PNG')
    while run:
        while menu:
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
            gridA.display(window)
            gridA.placement(window)
            pygame.display.update()
            gridA.listRect = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
