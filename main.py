#-*- coding: UTF-8 -*-
#@tobias Wendl

import pygame, sys
from pygame import*
import Button
from Button import*
import collision
from collision import*
import NavalBattle2
from NavalBattle2 import*
import SpeedJump
from SpeedJump import*
import chat
from chat import*
import time

def window_init():
	"""
	initializes the pygame window
	:return: None
	"""
	#pygame window initializing
	pygame.init()
	window = pygame.display.set_mode((800, 800))
	pygame.display.set_caption("ARCADE")

def window_creation():
	"""
	After the pygame window has been initialized, the background images of the main menu are being blit on the window
	:return: None
	"""
	#loading and setting the background image
	bg_img = pygame.image.load('img/arcade.jpg')
	window.blit(bg_img, (-350, 0))

	#loading and setting the frame behind the buttons
	frame = pygame.image.load('img/cadre.png')
	window.blit(frame, (40, 150))

	#loading and setting the logo
	logo = pygame.image.load('img/logo.PNG')
	window.blit(logo, (100, 0))


def button_creation():
	"""Creates the buttons objects later displayed on the screen
	:return: button object
	:rtype: object
	"""
	# creating different buttons
	button1 = Button('The Square Game', 200, 40, (310, 300), 5)
	button2 = Button('The naval Battle', 200, 40, (310, 370), 5)
	button3 = Button('Speed Jump', 200, 40, (310, 440), 5)
	button4 = Button('Piano Hero', 200, 40, (310, 510), 5)
	button5 = Button('Quit', 200, 40, (310, 580), 5)
	return button1, button2, button3, button4, button5

def mouse_collision(object):
	"""tests if the mouse is colliding with a given object
	:param object: can be a button or the chat icon
	:type object: object
	:return: returns True if collision is detected and False if not
	:rtype: bool
	"""
	mouseX, mouseY = pygame.mouse.get_pos()
	if object.collidepoint((mouseX, mouseY)):
		return True
	else:
		return False

def main():
	"""
	main function of the programm. Gives access to the main menu.
	:return: None
	"""
	#variables
	font = pygame.font.Font(None, 70)
	clock = pygame.time.Clock()

	#booleans
	run = True

	#window rectangle
	rectWindow = window.get_rect()

	#loading chat icon
	chatIcon = pygame.image.load('img/chatIcon.png')

	#getting the rectangle object of chat icon
	#this rectangle is going to be used to detect the collision of the mouse with the icon
	rectChat = chatIcon.get_rect()

	#placing the icon on the top right corner of the window
	rectChat.topright = rectWindow.topright

	#calling the window init function
	window_init()

	#using the button_creation method to create the buttons of the main menu
	button1, button2, button3, button4, button5 = button_creation()
	window_creation()

	#start of the main loop
	while run:
		#display buttons on the screen
		button1.draw(window)
		button2.draw(window)
		button3.draw(window)
		button4.draw(window)
		button5.draw(window)

		#display chat icon on the screen
		window.blit(chatIcon, rectChat)

		#testing if the buttons are being clicked
		if button1.pressed == True:
			print("starting square game")
			time.sleep(0.4)

			#starting the square game by calling main_squareGame
			main_squareGame()
			button1.pressed = False

			#after the game has been closed, we have to display the menu again
			#to do so we call the window creation method
			window_creation()

		if button2.pressed == True:
			print("starting naval battle")
			time.sleep(0.2)

			#starting the naval battle game
			main_NavalBattle()
			button2.pressed = False
			window_creation()

		if button3.pressed == True:
			print("starting speed jump")
			time.sleep(0.2)

			#starting the speed jump game
			SpeedJump.menu_jeu()
			button3.pressed = False
			window_creation()

		#piano hero hasn't been done
		#if the button is being clicked nothing happens
		if button4.pressed == True:
			print("starting piano hero")

		#if button clicked, main pygame window is closed
		if button5.pressed == True:
			#quit the main loop
			run = False

		#checking the collision between the mouse and the chat icon
		collision = mouse_collision(rectChat)

		#if a collision is detected, we also check if the user is clicking the icon
		if collision:
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN and event.button == 1:
					#if the icon has been clicked we run the chat by calling the main chat method
					print('chat icon clicked')
					main_chat()
					window_creation()

		#if the user wants to exit the programm, we check if has clicked on the red cross on the top right corner
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		#we update our window
		#makes the programm more dynamic and we see the changes
		#for example if the mouse goes over a button, it will change its color.
		pygame.display.update()
		clock.tick(60)
	#quit the programm
	pygame.quit()

#main function being called
#starts the main menu
if __name__ == '__main__':
	main()
