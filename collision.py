#-*- coding:UTF-8 -*-

import pygame, sys, time, random, os, math
from pygame import*
from pygame import mixer

pygame.init()
window = pygame.display.set_mode((800,800))
pygame.display.set_caption("The Square Game")

#load icon image
square_icon = pygame.image.load('img/square_icon.png')
pygame.display.set_icon(square_icon)

#load help page images
zqsd = pygame.image.load('img/zqsd2.png')
arrow = pygame.image.load('img/arrow2.png')

#load toggle sound icons
sound_on = pygame.image.load('img/sound_on1.jpg')
sound_off = pygame.image.load('img/sound_off.png')

#mixer (music settings)
pygame.mixer.set_num_channels(4)
background_music = pygame.mixer.Sound('music/background_soundtrack.mp3')
bonus_sound_effect = pygame.mixer.Sound('music/bonus_effect.mp3')
beep_effect = pygame.mixer.Sound('music/beep.mp3')
button_hoover = pygame.mixer.Sound('music/button.mp3')

canal_1 = pygame.mixer.Channel(0)
canal_2 = pygame.mixer.Channel(1)
canal_3 = pygame.mixer.Channel(2)
canal_4 = pygame.mixer.Channel(3)

class button() :
    global black
	#colours for button and text
    button_col = (255, 0, 0)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = (0,0,0)
    width = 180
    height = 70

    def __init__(self, x, y, text) :
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self) :

        global clicked
        action = False

		#get mouse position
        pos = pygame.mouse.get_pos()

		#create pygame Rect object for the button
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)   
		#check mouseover and clicked conditions
        if button_rect.collidepoint(pos) :
            canal_4.play(button_hoover)
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(window, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(window, self.hover_col, button_rect)

        else:
            pygame.draw.rect(window, self.button_col, button_rect)
            	
		#add shading to button
        pygame.draw.line(window, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(window, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(window, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(window, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

		#add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        window.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action

def move() :
    """movement function"""
    global speed, square
    keys = pygame.key.get_pressed()

    if keys[pygame.K_z] or keys[pygame.K_UP]:
        if square.y >= 1 :
            square.y -= speed 
    
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if square.y <= 800-square.height :
            square.y += speed
    
    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        if square.x >= 1 :
            square.x -= speed

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if square.x <= 800-square.width :
            square.x += speed
    
    pygame.draw.rect(window, light_color, square)

def background_animation() :
    """bg animation"""
    global obs_speed

    bg_obs_hor.x += obs_speed
    bg_obs_ver.y += obs_speed
    invert_bg_obs_hor.x -= obs_speed
    invert_bg_obs_ver.y -= obs_speed


    if bg_obs_hor.right >= 800 :
        obs_speed *= -1
        
    if bg_obs_hor.left <= 0 :
        obs_speed *= -1
    
    if you_square.x < 500 and you_square.y == 245 :
        you_square.x += 1
    if you_square.x == 500 and you_square.y < 600 :
        you_square.y += 1
    
    if you_square.y == 600 and you_square.x > 250 :
        you_square.x -= 1

    if you_square.x == 250 and you_square.y > 245 :
        you_square.y -= 1



    pygame.draw.rect(window, purple, bg_obs_hor)
    pygame.draw.rect(window, purple, bg_obs_ver)
    pygame.draw.rect(window, purple, invert_bg_obs_hor)
    pygame.draw.rect(window, purple, invert_bg_obs_ver)
    pygame.draw.rect(window, light_color, you_square)
    clock.tick(300)

def bg_animation_diff() :
    """difficulty window background animation function"""
    global obs_speed

    if you_square.x < 500 and you_square.y == 245 :
        you_square.x += 1

    if you_square.x == 500 and you_square.y < 500 :
        you_square.y += 1
    
    if you_square.y == 500 and you_square.x > 250 :
        you_square.x -= 1

    if you_square.x == 250 and you_square.y > 245 :
        you_square.y -= 1

    pygame.draw.rect(window, light_color, you_square)
    clock.tick(300)
    
def toggle_sound() :
    """setting music on and off with mouse click"""
    global Play_music
    if Play_music :
        window.blit(sound_on, (620,80))
    else :
        window.blit(sound_off, (620,80))
    Mouse_x, Mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get() :
        if event.type == pygame.MOUSEBUTTONDOWN :
            print("clicked")
            if Mouse_x >= 620 and Mouse_x <= 685 :
                if Mouse_y >= 80 and Mouse_y <= 140 :
                    print('collided')
                    if Play_music :
                        canal_1.set_volume(0)
                        canal_2.set_volume(0)
                        canal_3.set_volume(0)
                        Play_music = False
                        
                    else :
                        canal_1.set_volume(1)
                        canal_2.set_volume(1)
                        canal_3.set_volume(1)
                        Play_music = True

# booleans
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 30, True)
clicked = False
score_list = []
Play_music = True



#square properties
width = 50
height = 50
square = pygame.Rect(375,375,width, height)
speed = 5


#background rectangles properties
bg_obs_hor = pygame.Rect(0,700,70,20)
bg_obs_ver = pygame.Rect(700,0,20,70)
invert_bg_obs_hor = pygame.Rect(730,50,70,20)
invert_bg_obs_ver = pygame.Rect(100,730,20, 70)
you_square = pygame.Rect(250,245,25,25)
obs_speed = 1



#colors (R,G,B)
black = (0,0,0)
white = (255,255,255)
purple = (255,0,255)
light_red = (200,0,0)
dark_color = (30,30,30)
light_color = (220,220,220)
yellow = (255,255,0)
green = (0,255,100)

#buttons
play = button(300, 300, 'PLAY')
rules = button(300,400, 'HELP')
leave = button(300,500, 'LEAVE')
back = button(300,600, 'BACK')
easy = button(300,300,'EASY')
hard = button(300,400, 'HARD')


def main_squareGame() :
    run = True
    lost = True
    rules_tab = False
    difficulty = False
    play_Bool = False
    obs = True
    obsY = True
    food_spawn = True
    bonus_spawn = False
    blit_bonus = False
    easy_mode = False
    hard_mode = False
    obs_hard = True
    obs_hardY = True

    # bonus properties
    x_bonus = 0
    y_bonus = 0

    #score
    score = 0
    counter = 0

    #background music
    canal_1.play(background_music)
    canal_1.set_volume(1)
    print('starting to play bg music')
    while run :

    ##########################################################################################
        # main MENU
        window.fill(dark_color)
        text = font.render("THE SQUARE GAME", 1, white)
        window.blit(text, (275,100))


        i = 0


        if lost :
            show_highscore = open('highscore.txt',"r")
            content = show_highscore.read()
            if content == "":
                main_highscore = 0
            else :
                main_highscore = int(content)
            show_highscore.close()


        background_animation()
        toggle_sound()

        highscore_txt = font.render("HIGHSCORE :"+str(main_highscore),1,white)
        window.blit(highscore_txt, (300, 175))


        score_txt = font.render("SCORE :"+ str(score), 1, white)
        window.blit(score_txt, (330,225))


        if play.draw_button() :

            print("play")
            score = 0
            speed = 5
            counter = 0
            square.width = 50
            square.height = 50
            square.x = 375
            square.y = 375
            play_Bool = True
            difficulty = True
            lost = False
            #open highscore file in writting mode
            highscore_file = open('highscore.txt',"w")


        if rules.draw_button() :
            print("help")
            rules_tab = True

        if leave.draw_button() :
            print("leave")
            canal_1.set_volume(0)
            canal_2.set_volume(0)
            canal_3.set_volume(0)
            run = False

        pygame.display.update()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
    #########################################################################################
        # HELP section
        while rules_tab :
            window.fill(dark_color)

            if back.draw_button() :
                print("back to menu")
                rules_tab = False

            pygame.draw.rect(window, light_red, (200,200,20,20))
            food_txt = font.render("food",1,white)
            window.blit(food_txt, (187,230))

            pygame.draw.rect(window, purple, (400,200,20,20))
            obstacle_txt = font.render("obstacle",1, white)
            window.blit(obstacle_txt,(360,230))

            pygame.draw.rect(window, green, (600,200,20,20))
            bonus_txt = font.render("bonus",1,white)
            window.blit(bonus_txt, (580,230))

            pygame.draw.rect(window, light_color, (375,375, 50,50))
            you_txt = font.render("you",1,white)
            window.blit(you_txt, (380, 430))

            window.blit(zqsd, (100,350))
            window.blit(arrow, (500,350))

            help_txt = font.render("HOW TO PLAY",1,white)
            window.blit(help_txt,(325,100))


            pygame.display.update()
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    rules_tab = False
                    run = False

    #########################################################################################
        #choose difficulty
        while difficulty :
            window.fill(dark_color)
            bg_animation_diff()
            difficulty_txt = font.render("DIFFICULTY",1,white)
            window.blit(difficulty_txt,(325,100))

            if easy.draw_button() :
                print("easy mode")
                easy_mode = True
                difficulty = False

            if hard.draw_button() :
                print("hard mode")
                hard_mode = True
                difficulty = False

            pygame.display.update()

            #quit
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    difficulty = False
                    play_Bool = False
                    run = False

    #########################################################################################
        #play the game

        while play_Bool :
            window.fill(dark_color)

            text = font.render("SCORE :" + str(score), 1, white) #Blit score on window
            window.blit(text, (600, 50))

            #food spawning part
            if food_spawn :
                x_food = random.randint(10,790)
                y_food = random.randint(10,790)
                food_spawn = False

            food = pygame.Rect(x_food, y_food,20,20)

            pygame.draw.rect(window, light_red, food )

            if square.colliderect(food) :
                canal_3.play(beep_effect)
                food_spawn = True
                counter += 1

            if food_spawn :
                print("augmentation")
                square.width += 2
                square.height += 2
                score += 10
                print("score :", score)

            # bonus spawning part
            if counter == 10 :
                counter = 0
                bonus_spawn = True
                blit_bonus = True

            if bonus_spawn :
                x_bonus = random.randint(10,790)
                y_bonus = random.randint(10,790)
                bonus_spawn = False

            bonus = pygame.Rect(x_bonus, y_bonus,20,20)
            if blit_bonus :
                pygame.draw.rect(window, green, bonus)

            if square.colliderect(bonus) and blit_bonus :
                canal_2.play(bonus_sound_effect)
                bonus_spawn = True
                blit_bonus = False
                counter = 0


            if bonus_spawn and counter == 0: # only get bonus boost if bonus is the first to collide with square when spawned
                print("bonus")
                if square.height >= 200 :
                    square.height = 150
                    square.width = 150
                if speed >= 12 :
                    speed -= 1 #max speed set to 12

                square.width -= 10
                square.height -= 10
                speed += 1
                print("speed :", speed)


            ####################################
            #obstacle
            #
            # EASY MODE
            #
            if obs : #X axis
                x_obstacle = random.randint(30,770)
                obs_width = random.randint(20,60)
                obs_height = random.randint(20,70)
                obstacle = pygame.Rect(x_obstacle, 0, obs_width, obs_height)
                obs_move = True
                obs = False

            if square.colliderect(obstacle) :
                obs = True
                obs_move = False
                obstacle.y = -100
                play_Bool = False
                blit_bonus = False
                lost = True
                print("LOST")
                if score > main_highscore :
                    highscore_file.write(str(score))
                    highscore_file.close()
                else :
                    highscore_file.write(str(main_highscore))
                    highscore_file.close()



            if obs_move :
                obstacle.y += 5
                pygame.draw.rect(window, purple, obstacle)
                if obstacle.top <= 0 or obstacle.bottom >= 800 :
                    obs_move = False
                    obs = True

            ####################################
            if score >= 150 : #obstacle Y axis
                if obsY :
                    y_obstacle = random.randint(30,770)
                    obsY_width = random.randint(20,60)
                    obsY_height = random.randint(20,70)
                    obstacleY = pygame.Rect(0,y_obstacle, obsY_width, obsY_height)
                    obsY_move = True
                    obsY = False

                if square.colliderect(obstacleY) :
                    obsY = True
                    obsY_move = False
                    obstacleY.x = -100
                    play_Bool = False
                    blit_bonus = False
                    lost = True
                    print("LOST")
                    if score > main_highscore :
                        highscore_file.write(str(score))
                        highscore_file.close()
                    else :
                        highscore_file.write(str(main_highscore))
                        highscore_file.close()

                if obsY_move :
                    obstacleY.x += 5
                    pygame.draw.rect(window, purple, obstacleY)
                    if obstacleY.left <= 0 or obstacleY.right >= 800 :
                        obsY_move = False
                        obsY = True

            ####################################
            if score >= 200 : # becomes harder
                if obs_hard :
                    x_hard = random.randint(30,770)
                    hard_width = random.randint(20,30)
                    hard_height = random.randint(30,80)
                    obstacleH = pygame.Rect(x_hard,800,hard_width,hard_height)
                    obs_hard_move = True
                    obs_hard = False

                if square.colliderect(obstacleH) :
                    obs_hard = True
                    obs_hard_move = False
                    obstacleH.y = 1000
                    play_Bool = False
                    blit_bonus = False
                    lost = True
                    print("LOST")
                    if score > main_highscore :
                        highscore_file.write(str(score))
                        highscore_file.close()
                    else :
                        highscore_file.write(str(main_highscore))
                        highscore_file.close()

                if obs_hard_move :
                    obstacleH.y -= 5
                    pygame.draw.rect(window, purple, obstacleH)
                    if obstacleH.top <= 0 :
                        obs_hard_move = False
                        obs_hard = True

            ####################################
            if score >= 300 :
                if obs_hardY :
                    y_hard = random.randint(30,770)
                    hardY_width = random.randint(30,80)
                    hardY_height = random.randint(20,30)
                    obstacleHY = pygame.Rect(800, y_hard, hardY_width, hardY_height)
                    obs_hard_moveY = True
                    obs_hardY = False

                if square.colliderect(obstacleHY) :
                    obs_hardY = True
                    obs_hard_moveY = False
                    obstacleHY.x = 1000
                    play_Bool = False
                    blit_bonus = False
                    lost = True
                    print("LOST")
                    if score > main_highscore :
                        highscore_file.write(str(score))
                        highscore_file.close()
                    else :
                        highscore_file.write(str(main_highscore))
                        highscore_file.close()

                if obs_hard_moveY :
                    obstacleHY.x -= 5
                    pygame.draw.rect(window, purple, obstacleHY)
                    if obstacleHY.left <= 0 :
                        obs_hard_moveY = False
                        obs_hardY = True
            ####################################
            #
            # HARD MODE
            #
            ####################################
            if hard_mode and score >= 20 :
                if obs_hard :
                    x_hard = random.randint(30,770)
                    hard_width = random.randint(20,30)
                    hard_height = random.randint(30,80)
                    obstacleH = pygame.Rect(x_hard,800,hard_width,hard_height)
                    obs_hard_move = True
                    obs_hard = False

                if square.colliderect(obstacleH) :
                    obs_hard = True
                    obs_hard_move = False
                    obstacleH.y = 1000
                    play_Bool = False
                    print("LOST")
                    lost = True
                    blit_bonus = False
                    if score > main_highscore :
                        highscore_file.write(str(score))
                        highscore_file.close()
                    else :
                        highscore_file.write(str(main_highscore))
                        highscore_file.close()

                if obs_hard_move :
                    obstacleH.y -= 8
                    pygame.draw.rect(window, purple, obstacleH)
                    if obstacleH.top <= 0 :
                        obs_hard_move = False
                        obs_hard = True

            # here it gets realy hard
            if hard_mode and score >= 100 :
                if obs_hardY :
                    y_hard = random.randint(30,770)
                    hardY_width = random.randint(30,80)
                    hardY_height = random.randint(20,30)
                    obstacleHY = pygame.Rect(800, y_hard, hardY_width, hardY_height)
                    obs_hard_moveY = True
                    obs_hardY = False

                if square.colliderect(obstacleHY) :
                    obs_hardY = True
                    obs_hard_moveY = False
                    obstacleHY.x = 1000
                    play_Bool = False
                    blit_bonus = False
                    lost = True
                    print("LOST")
                    if score > main_highscore :
                        highscore_file.write(str(score))
                        highscore_file.close()
                    else :
                        highscore_file.write(str(main_highscore))
                        highscore_file.close()

                if obs_hard_moveY :
                    obstacleHY.x -= 8
                    pygame.draw.rect(window, purple, obstacleHY)
                    if obstacleHY.left <= 0 :
                        obs_hard_moveY = False
                        obs_hardY = True


            #quit game
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    play_Bool = False
                    run = False
                    highscore_file.close()



            #pygame.draw.rect(window, light_color, square )
            move()

            #update window
            pygame.display.update()


            clock.tick(60)
