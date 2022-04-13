#-*- coding: UTF-8 -*-

import pygame
from pygame import*
def main () :
    print("main")



if __name__ == "__main__":
    main()
pygame.init()
window = pygame.display.set_mode((800,800))
pygame.display.set_caption("Projet 2A") #a changer

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()