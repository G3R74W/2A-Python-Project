#-*- coding: UTF-8 -*-
#@tobias_Wendl

import pygame
from pygame import*

##############
## --MENU-- ##
##############



pygame.init()
window = pygame.display.set_mode((800,800))
pygame.display.set_caption("ARCADE") #a changer ?


#variables
font = pygame.font.SysFont("comicsans", 50, True)

#booleans
run = True

#colors (RGB)
white = (255, 255, 255)
while run:
    text = font.render("ARCADE", 1, white)
    window.blit(text, (310, 100))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()

