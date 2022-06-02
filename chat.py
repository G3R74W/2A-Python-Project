#-*- coding: UTF-8 -*-

import pygame
from pygame import*
import Button
from Button import*
import InputBox
from InputBox import*
import time

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

def message_content():
    """permet l'attribution du contenu du fichier.txt contenant l'entièreté des messages"""
    AllMessages = open('messages.txt', 'r')
    content = AllMessages.readlines()
    AllMessages.close()
    return content

def message_display(window, content):
    """permet d'afficher les messages précédents dans le chat"""
    xPos = 600
    nbr_message = len(content)

    #on peut afficher maximum 12 messages sur l'écran
    #on test si il y a plus de 12 messages dans le fichiers
    if nbr_message > 12:
        depassement = nbr_message - 12
        yPos = 50 - depassement*50
    else:
        yPos = 50
    for i in range(len(content)):
        text = font.render(content[i], 1, (0, 0, 0))
        window.blit(text, (xPos, yPos))
        yPos += 50



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

        content = message_content()

        pygame.draw.rect(window, white, (0, 0, 800, 650))
        button2.draw(window)

        if button1.pressed == True:
            print('back to main menu')
            button1.pressed = False
            run = False

        for event in pygame.event.get():
            for box in boxlist:
                message = box.handle_event(event, window)
                if message != '':
                    AllMessage = open('messages.txt', 'a')
                    AllMessage.write('\n' + message)
                    box.message = ''
                    AllMessage.close()


            # permet à l'utilisateur de quitter le jeu --> retour au menu principal
            if event.type == pygame.QUIT:
                run = False
        content = message_content()

        message_display(window, content)

        pygame.display.update()
        inputBox.update()
        window_refresh(window)
        inputBox.draw(window)
