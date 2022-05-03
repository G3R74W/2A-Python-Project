#-*- coding: UTF-8 -*-
#@tobias_Wendl

import pygame
from pygame import*
import collision

##############
## --MENU-- ##
##############

def menu_buttons():
    """menu buttons"""
    # set game icons and load images
    square_game_icon = pygame.image.load('img/square_icon.png')
    window.blit(square_game_icon, (200, 250))

    naval_battle_icon = pygame.image.load('img/ww2_ship.jpg')
    window.blit(naval_battle_icon, (200, 500))

    speed_jump_icon = pygame.image.load('img/chrono.jpg')
    window.blit(speed_jump_icon, (500, 250))
    # menu style

    # square game menu button
    pygame.draw.line(window, line_color, (0, 230), (330, 230), line_width)
    pygame.draw.line(window, line_color, (0, 370), (330, 370), line_width)
    pygame.draw.line(window, line_color, (330, 230), (330, 370), line_width)
    SquareText = font_gameName.render("The Square Game", 1, white)
    window.blit(SquareText, (10, 280))


    # naval battle menu button
    pygame.draw.line(window, line_color, (0, 480), (330, 480), line_width)
    pygame.draw.line(window, line_color, (0, 620), (330, 620), line_width)
    pygame.draw.line(window, line_color, (330, 480), (330, 620), line_width)
    NavalText = font_gameName.render("Naval Battle", 1, white)
    window.blit(NavalText, (10, 530))

    #speed jump menu button
    pygame.draw.line(window, line_color, (480, 230), (800, 230), line_width)
    pygame.draw.line(window, line_color, (480, 370), (800, 370), line_width)
    pygame.draw.line(window, line_color, (480, 230), (480, 370), line_width)
    Speed_JumpText = font_gameName.render("Speed Jump", 1, white)
    window.blit(NavalText, (670, 280))

    #piano hero menu button
    pygame.draw.line(window, line_color, (480, 480), (800, 480), line_width)
    pygame.draw.line(window, line_color, (480, 620), (800, 620), line_width)
    pygame.draw.line(window, line_color, (480, 480), (480, 620), line_width)
    Piano_HeroText = font_gameName.render("Piano Hero", 1, white)
    window.blit(Piano_HeroText, (680, 530))

pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("ARCADE") #a changer ?


#variables
font = pygame.font.SysFont("comicsans", 50, True)
font_gameName = pygame.font.SysFont("Times new Roman", 22, True)
line_width = 7

#booleans
run = True

#colors (RGB)
white = (255, 255, 255)
line_color = (179, 254, 255)
background_color = (191, 255, 107)


while run:
    text = font.render("ARCADE", 1, white)
    window.blit(text, (310, 100))
    pygame.display.update()

    menu_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()

