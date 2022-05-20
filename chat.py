#-*- coding: UTF-8 -*-

import pygame
import time
from pygame import*
import Button
from Button import*

def window_init():
    """initialisation de la fenêtre"""
    # initialisation pygame
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("CHAT")
    window_refresh(window)
    return window

def window_refresh(window):
    """permet de refresh la fenêtre"""
    window.fill((50, 90, 168))

def button_creation():
    """creation des differents bouttons"""
    button1 = Button('Back to menu', 200, 40, (290, 670), 5)
    return button1

def main_chat():
    """main du chat"""
    window = window_init()
    window_init()
    clock = pygame.time.Clock()

    button1 = button_creation()

    #booleans
    run = True
    while run:
        button1.draw(window)
        pygame.display.update()

        if button1.pressed == True:
            print('back to main menu')
            button1.pressed = False
            run = False

        #permet à l'utilisateur de quitter le jeu --> retour au menu principal
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
