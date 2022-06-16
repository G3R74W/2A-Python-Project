#-*- coding: UTF-8 -*-
#@tobias_Wendl

import pygame, sys
from pygame import*
import Button
from Button import*
#import collision
#from collision import*
#import NavalBattle2
#from NavalBattle2 import*
#import SpeedJump
#from SpeedJump import*
#import chat
from chat_perso import*
import time

def window_init():
	# initialisation pygame
	pygame.init()
	window = pygame.display.set_mode((800, 800))
	pygame.display.set_caption("ARCADE")

def window_creation():

	#set background image
	bg_img = pygame.image.load('img/arcade.jpg')
	window.blit(bg_img, (-350, 0))

	#set frame
	frame = pygame.image.load('img/cadre.png')
	window.blit(frame, (40, 150))

	#set logo
	logo = pygame.image.load('img/logo.PNG')
	window.blit(logo, (100, 0))


def button_creation():
	"""function qui permet de créer les différents bouttons utilisés"""
	# creating different buttons
	button1 = Button('The Square Game', 200, 40, (310, 300), 5)
	button2 = Button('The naval Battle', 200, 40, (310, 370), 5)
	button3 = Button('Speed Jump', 200, 40, (310, 440), 5)
	button4 = Button('Piano Hero', 200, 40, (310, 510), 5)
	button5 = Button('Quit', 200, 40, (310, 580), 5)
	return button1, button2, button3, button4, button5

def mouse_collision(object):
	"""fonction qui permet de tester la collision de la souris avec un objet"""
	mouseX, mouseY = pygame.mouse.get_pos()
	if object.collidepoint((mouseX, mouseY)):
		return True
	else:
		return False

def main():
	#variables
	font = pygame.font.Font(None, 70)
	clock = pygame.time.Clock()

	#booleans
	run = True

	#colors (RGB)
	white = (255, 255, 255)
	line_color = (179, 254, 255)
	background_color = (191, 255, 107)

	#window rectangle
	rectWindow = window.get_rect()

	#chat icon
	chatIcon = pygame.image.load('img/chatIcon.png')
	rectChat = chatIcon.get_rect()
	rectChat.topright = rectWindow.topright


	window_init()
	button1, button2, button3, button4, button5 = button_creation()
	window_creation()
	#début de la boucle principale
	while run:
		#display buttons on the screen
		button1.draw(window)
		button2.draw(window)
		button3.draw(window)
		button4.draw(window)
		button5.draw(window)
		#window.blit(chatIcon, (700, 0))
		window.blit(chatIcon, rectChat)

		#on teste si les bouttons sont cliqués
		if button1.pressed == True:
			print("starting square game")
			time.sleep(0.4)
			main_squareGame()
			button1.pressed = False
			window_creation()

		if button2.pressed == True:
			print("starting naval battle")
			time.sleep(0.2)
			main_NavalBattle()
			button2.pressed = False
			window_creation()

		if button3.pressed == True:
			print("starting speed jump")
			time.sleep(0.2)
			SpeedJump.menu_jeu()
			button3.pressed = False
			window_creation()

		if button4.pressed == True:
			print("starting piano hero")

		if button5.pressed == True:
			#quit
			run = False

		#on détecte la collision de la souris avec l'icone de tchat
		collision = mouse_collision(rectChat)

		#si il y a collision on vérifie si l'utilisateur clique également
		if collision:
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN and event.button == 1:
					#si l'utilisateur clique l'icone de tchat, on lance le tchat
					print('chat icon clicked')
					main_chat()
					window_creation()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		pygame.display.update()
		clock.tick(60)
	pygame.quit()

#on appelle la fonction main
#celle-ci lance le menu principale et permet d'accéder aux différents jeux
if __name__ == '__main__':
	main()