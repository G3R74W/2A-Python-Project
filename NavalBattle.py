#-*- coding: UTF-8 -*-

import pygame
from pygame import*
import Button
from Button import*
import time

class piece:
    def __init__(self, type):
        color = (102, 95, 122)
        if type == "porte avion":
            self.size = 5

        elif type == "croiseur":
            self.size = 4
        elif type == "contre torpilleur":
            self.size = 3
        elif type == "torpilleur":
            self.size = 2

def window_init():
    # initialisation pygame
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("THE NAVAL BATTLE")
    bg_image = pygame.image.load('img/blue.jpg')
    window.blit(bg_image, (0, 0))
    return window

def Button_creation():
    button1 = Button('Back to menu', 200, 40, (290, 540), 5)
    button2 = Button('Play', 200, 40, (290, 400), 5)
    button3 = Button('How to play', 200, 40, (290, 470), 5)
    return button1, button2, button3

def main_NavalBattle():

    window = window_init()

    #intialisation de la fenetre
    window_init()

    #creation du boutton de retour au menu
    button1, button2, button3 = Button_creation()

    run = True
    menu = True
    clock = pygame.time.Clock()
    logo = pygame.image.load('img/logoNV.PNG')
    while run:
        while menu:
            window.blit(logo, (245, 70))
            #affichage du boutton sur la fenetre
            button1.draw(window)
            button2.draw(window)
            button3.draw(window)

            if button1.pressed == True :
                print("back to main menu")
                time.sleep(0.2)
                button1.pressed = False
                run = False
                menu = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    menu = False

            pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
