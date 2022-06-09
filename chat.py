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
    button3 = Button('^', 20, 20, (100, 670), 5)
    button4 = Button('v', 20, 20, (100, 700), 5)
    return button1, button2, button3, button4

def message_content():
    """permet l'attribution du contenu du fichier.txt contenant l'entièreté des messages"""
    AllMessages = open('messages.txt', 'r')
    content = AllMessages.readlines()
    AllMessages.close()
    return content

def message_display(window, content, counter):
    """permet d'afficher les messages précédents dans le chat"""
    xPos = 550
    nbr_message = len(content)

    #on peut afficher maximum 12 messages sur l'écran
    #on test si il y a plus de 12 messages dans le fichiers
    if nbr_message > 12:
        depassement = nbr_message - 12
        yPos = counter*50 - depassement*50
    else:
        yPos = 50

    #on fait en sorte de ne pas afficher les messages au délà du cadre prévu
    if counter > 1:
        msgRange = len(content)-counter
    else:
        msgRange = len(content)

    for i in range(msgRange):
        #on supprime le caractère de retour chariot pour qu'il ne s'affiche pas dans pygame
        msgLength = len(content[i])-1
        message = ""
        if content[i][0] == "0":
            xPos = 550
            sender = "you:"
            msgColor = (50, 168, 131)
        elif content[i][0] == "1":
            xPos = 50
            sender = "other:"
            msgColor = (162, 166, 168)

        for j in range(msgLength):
            if content[i][j] =="0" or content[i][j] == "1":
                message += ""
            else:
                message += content[i][j]
        pygame.draw.rect(window, msgColor, (xPos-10, yPos-5, 230, 30), border_radius=4)
        text = font.render(sender+message, 1, (0, 0, 0))
        window.blit(text, (xPos, yPos))
        yPos += 50

def main_chat():
    """main du chat"""
    window = window_init()
    window_init()
    clock = pygame.time.Clock()

    button1, button2, button3, button4 = button_creation()

    #colors
    white = (255,255,255)

    #input box
    inputBox = InputBox()
    boxlist = [inputBox]

    #booleans
    run = True

    counter = 1
    while run:
        #button1.draw(window)

        content = message_content()

        pygame.draw.rect(window, (99, 137, 153), (0, 0, 800, 650))
        button2.draw(window)
        button3.draw(window)
        button4.draw(window)

        if button1.pressed == True:
            print('back to main menu')
            button1.pressed = False
            run = False

        if button3.pressed == True:
            print('up')
            time.sleep(0.2)
            button3.pressed = False
            counter += 1

        if button4.pressed == True:
            print('down')
            time.sleep(0.2)
            button4.pressed = False
            counter -= 1

        for event in pygame.event.get():
            for box in boxlist:
                message = box.handle_event(event, window)
                if message != '':
                    AllMessage = open('messages.txt', 'a')
                    AllMessage.write("0"+message + '\n')
                    box.message = ''
                    AllMessage.close()


            # permet à l'utilisateur de quitter le jeu --> retour au menu principal
            if event.type == pygame.QUIT:
                run = False
        content = message_content()

        message_display(window, content, counter)

        pygame.display.update()
        inputBox.update()
        window_refresh(window)
        inputBox.draw(window)
