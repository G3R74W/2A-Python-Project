#-*- coding: UTF-8 -*-
#@tobias_Wendl

import pygame, sys
from pygame import*
import collision
from collision import*

class Button:
	def __init__(self,text,width,height,pos,elevation):

		gui_font = pygame.font.Font(None, 30)
		#Core attributes
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]

		# top rectangle
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#475F77'

		# bottom rectangle
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'
		#text
		self.text_surf = gui_font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self):
		# elevation logic
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(window,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(window,self.top_color, self.top_rect,border_radius = 12)
		window.blit(self.text_surf, self.text_rect)
		self.check_click()

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#D74B4B'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					print('click')
					self.pressed = False
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = '#475F77'

#initialisation pygame
pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("ARCADE")


#set background image
bg_img = pygame.image.load('img/arcade.jpg')
window.blit(bg_img, (-350, 0))

#variables
font = pygame.font.Font(None, 70)

line_width = 7

#booleans
run = True

#colors (RGB)
white = (255, 255, 255)
line_color = (179, 254, 255)
background_color = (191, 255, 107)


#creating different buttons
button1 = Button('The Square Game', 200, 40, (310, 300), 5)
button2 = Button('The naval Battle', 200, 40, (310, 370), 5)
button3 = Button('Speed Jump', 200, 40, (310, 440), 5)
button4 = Button('Piano Hero', 200, 40, (310, 510), 5)
button5 = Button('Quit', 200, 40, (310, 670), 5)


clock = pygame.time.Clock()
while run:
    text = font.render("ARCADE", 1, white)
    window.blit(text, (310, 100))

	#display buttons on the screen
    button1.draw()
    button2.draw()
    button3.draw()
    button4.draw()
    button5.draw()

    if button1.pressed == True:
        main_squareGame()

    if button5.pressed == True:
		#quit
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
    clock.tick(60)
pygame.quit()

