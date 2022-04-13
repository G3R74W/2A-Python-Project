#-*- coding: UTF-8 -*-

import pygame
from pygame import*






###################################################################
## MENU
###################################################################

def menu():
    print("menu")
    pygame.init()
    window = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Projet 2A") #a changer

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

def main():
        print("main")
        menu()

if __name__ == "__main__":
    main()

print('hello')