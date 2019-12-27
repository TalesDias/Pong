#!/usr/bin/env python

"""
    Pong Game
"""


# import everything
import os, pygame, math, sys, time, random
from pygame.locals import *

#Auxiliar Class for Keyboard events
from KeyboardImpl import Keyboard

#Game Classes
from pong import *


#Working directory
main_dir = os.path.split(os.path.abspath(__file__))[0]


# quick function to load an image
def load_image(name):
    path = os.path.join(main_dir, "images", name)
    return pygame.image.load(path).convert()


# main thread
def main():

    #Should Always be the first to prevent bugs
    pygame.init()

    #Initialize the keyboard handler
    kb = Keyboard(pygame.event)

    #set up the display
    width = 900
    height = 600
    screen = pygame.display.set_mode((width, height))

    #paints the background black
    screen.fill((0, 0, 0))

    #game HUD
    lives_l = 10
    lives_r = 10  
    font_score = pygame.font.SysFont(pygame.font.get_default_font(), 30, True,False)

    rand = int(random.random()*100)
    ball = Ball(screen, (255, 255, 255), (width/2, height/2), 8)
    ball.vel_x = ball.max_speed if rand%2 else -ball.max_speed    
    ball.vel_y = 0


    bar_l = Bar(screen,(255, 255, 255), Rect(30, 30, 25, 150))


    #controls the left bar
    kb.while_key_pressed(pygame.K_w, bar_l.move_up)
    kb.on_key_released(pygame.K_w, bar_l.stop)

    kb.while_key_pressed(pygame.K_s, bar_l.move_down)
    kb.on_key_released(pygame.K_s, bar_l.stop)

    #key k exits the game
    kb.on_key_pressed(pygame.K_k, pygame.quit)

    wait = False
    #main loop
    while True:
        #clear screen
        screen.fill((0, 0, 0))

        score = font_score.render(str(lives_l)+"-"+str(lives_r),True,(255,255,255))
        screen.blit(score, (width/2, 10))
        

        if (ball.rect.left <= 0 or ball.rect.right >= width):
            
            if(ball.rect.left <= 0):
                lives_l -=1
            else:
                lives_r -=1

            ball.center_x,ball.center_y= screen.get_rect().center

            rand = int(random.random()*100)
            ball.vel_x = ball.max_speed if rand%2 else -ball.max_speed
            ball.vel_y = 0 

            wait = True


        if (ball.rect.bottom >= height or ball.rect.top <= 0):
            ball.vel_y *= -1
        
        ball.move()
        bar_l.move()
        
        #update everything and slows the thread
        pygame.display.update()
        time.sleep(0.01)


if __name__ == "__main__":
    main()