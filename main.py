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

def rand_vel_ball(ball):
    rand = int(random.random()*100)
    ball.vel_x = ball.max_speed/2 if rand%2 else -ball.max_speed/2    
    ball.vel_y = rand%(ball.max_speed) - ball.max_speed/2

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

    ball = Ball(screen, (255, 255, 255), screen.get_rect().center, 8)
    rand_vel_ball(ball)

    bar_l = Bar(screen,(255, 255, 255), Rect(30, height/2-75, 25, 150))
    bar_r = Bar(screen,(255, 255, 255), Rect(width-25-30, height/2-75, 25, 150))


    #controls the left bar
    kb.while_key_pressed(pygame.K_w, bar_l.move_up)
    kb.on_key_released(pygame.K_w, bar_l.stop)

    kb.while_key_pressed(pygame.K_s, bar_l.move_down)
    kb.on_key_released(pygame.K_s, bar_l.stop)

    #controls the right bar
    kb.while_key_pressed(pygame.K_UP, bar_r.move_up)
    kb.on_key_released(pygame.K_UP, bar_r.stop)

    kb.while_key_pressed(pygame.K_DOWN, bar_r.move_down)
    kb.on_key_released(pygame.K_DOWN, bar_r.stop)

    #key k exits the game
    kb.on_key_pressed(pygame.K_k, pygame.quit)

    #main loop
    while True:
        #clear screen
        screen.fill((0, 0, 0))

        #update the score
        score = font_score.render(str(lives_l)+" - "+str(lives_r),True,(255,255,255))
        screen.blit(score, (width/2, 10))
        
        #check if any of the sides lost a life
        if (ball.rect.left <= 0 or ball.rect.right >= width):
            
            if(ball.rect.left <= 0):
                lives_l -=1
            else:
                lives_r -=1

            ball.center_x,ball.center_y= screen.get_rect().center
            rand_vel_ball(ball)

        #bounce the ball on the side walls
        if (ball.rect.bottom >= height or ball.rect.top <= 0):
            ball.vel_y *= -1

        #bounce the ball on the bars
        #note that the far from the center off the ball 
        #the more the ball accelerates

        if(ball.rect.colliderect(bar_l.rect)):
            if ball.vel_x > 0:
                ball.vel_x = -ball.max_speed
            else: 
                ball.vel_x = ball.max_speed

            delta = bar_l.rect.centery -  ball.center_y
            diff = delta//(bar_l.rect.height/8)
            ball.vel_y -= diff    

        if(ball.rect.colliderect(bar_r.rect)):
            if ball.vel_x > 0:
                ball.vel_x = -ball.max_speed
            else: 
                ball.vel_x = ball.max_speed
            delta = bar_r.rect.centery -  ball.center_y
            diff = delta//(bar_r.rect.height/8)
            ball.vel_y -= diff


        #register moves
        ball.move()
        bar_l.move()
        bar_r.move()

        #update everything and slows the thread
        pygame.display.update()
        time.sleep(0.01)


if __name__ == "__main__":
    main()