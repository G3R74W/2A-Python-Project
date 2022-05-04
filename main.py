#-*- coding: UTF-8 -*-
#@tobias_Wendl

import pygame, sys, collision
from pygame import*

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

"""
def menu_icons():
    """menu icons"""
    # set game icons and load images
    square_game_icon = pygame.image.load('img/square_icon.png')
    window.blit(square_game_icon, (250, 250))

    naval_battle_icon = pygame.image.load('img/ww2_ship.jpg')
    window.blit(naval_battle_icon, (200, 500))

    speed_jump_icon = pygame.image.load('img/chrono.jpg')
    window.blit(speed_jump_icon, (500, 250))
"""

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

button1 = Button('The Square Game', 200, 40, (20, 250), 5)

clock = pygame.time.Clock()
while run:
    text = font.render("ARCADE", 1, white)
    window.blit(text, (310, 100))
    button1.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
    clock.tick(60)
pygame.quit()

