#-*- coding: UTF-8 -*-
#@tobias_Wendl

import pygame
from pygame import*

##############
## --MENU-- ##
##############

def menu_buttons():
    """menu buttons"""
    # set game icons
    square_game_icon = pygame.image.load('img/square_icon.png')
    window.blit(square_game_icon, (200, 250))

    naval_battle_icon = pygame.image.load('img/ww2_ship.jpg')
    window.blit(naval_battle_icon, (200, 500))

    # menu style

    # square game menu button
    pygame.draw.line(window, white, (0, 230), (330, 230), line_width)
    pygame.draw.line(window, white, (0, 370), (330, 370), line_width)
    pygame.draw.line(window, white, (330, 230), (330, 370), line_width)

    # naval battle menu button
    pygame.draw.line(window, white, (0, 480), (330, 480), line_width)
    pygame.draw.line(window, white, (0, 620), (330, 620), line_width)
    pygame.draw.line(window, white, (330, 480), (330, 620), line_width)

pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("ARCADE") #a changer ?


#variables
font = pygame.font.SysFont("comicsans", 50, True)
line_width = 7

#booleans
run = True

#colors (RGB)
white = (255, 255, 255)


while run:
    text = font.render("ARCADE", 1, white)
    window.blit(text, (310, 100))
    pygame.display.update()

    menu_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()

