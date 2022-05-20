#-*- coding: UTF-8 -*-

import pygame
from pygame import*
import Button
from Button import*
import InputBox
from InputBox import*

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
    button2 = Button('Send', 200, 40, (600, 680), 5)
    return button1, button2

def main_chat():
    """main du chat"""
    window = window_init()
    window_init()
    clock = pygame.time.Clock()

    button1, button2 = button_creation()

    #colors
    white = (255,255,255)

    #input box
    inputBox = InputBox()
    boxlist = [inputBox]
    #booleans
    run = True
    while run:
        #button1.draw(window)

        pygame.draw.rect(window, white, (0, 0, 800, 650))
        button2.draw(window)


        if button1.pressed == True:
            print('back to main menu')
            button1.pressed = False
            run = False


        #permet à l'utilisateur de quitter le jeu --> retour au menu principal
        for event in pygame.event.get():
            for box in boxlist:
                message = box.handle_event(event, window)
            if event.type == pygame.QUIT:
                run = False
        text = font.render(message, 1, (0, 0, 0))
        window.blit(text, (0, 0))
        pygame.display.update()
        inputBox.update()
        window_refresh(window)
        inputBox.draw(window)
