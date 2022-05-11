#-*- coding: UTF-8 -*-

import pygame
from pygame import*
import Button
from Button import*

def window_init():
    # initialisation pygame
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("THE NAVAL BATTLE")
    bg_image = pygame.image.load('img/blue.jpg')
    window.blit(bg_image, (0, 0))
    return window

def Button_creation():
    button1 = Button('Back to menu', 200, 40, (400, 300), 5)
    return button1

def main_NavalBattle():

    window = window_init()

    #intialisation de la fenetre
    window_init()

    #creation du boutton de retour au menu
    button1 = Button_creation()

    run = True
    while run:
        #affichage du boutton sur la fenetre
        button1.draw(window)

        if button1.pressed == True :
            print("back to main menu")
            button1.pressed = False
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
