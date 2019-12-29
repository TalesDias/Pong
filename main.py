#!/usr/bin/python3

"""
    Pong Game
"""


#Imports from pygame
import os, pygame, math, sys, time, random
from pygame.locals import *

#Imports from PyQt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

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

def game(mode):
    #Should Always be the first to prevent bugs
    pygame.init()

    #Initialize the keyboard handler
    kb = Keyboard(pygame.event)

    #set up the display
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))

    paused = False
    def pause():
        nonlocal paused
        paused = not paused

    #inits the ball with random velocity
    def rand_vel_ball(ball):
        rand = int(random.random()*100)
        ball.vel_x = int(ball.max_speed/5 if rand%2 else -ball.max_speed/5)
        ball.vel_y = int(rand%(ball.max_speed) - ball.max_speed/2)

    #paints the background black
    screen.fill((0, 0, 0))

    #game HUD
    lives_l = 10
    lives_r = 10 
    font_score = pygame.font.SysFont(pygame.font.get_default_font(), 30, True,False)

    #creates the ball
    ball = Ball(screen, (255, 255, 255), screen.get_rect().center, 8)
    rand_vel_ball(ball)

    #creates the left bar
    bar_l = Bar(screen,(255, 255, 255), Rect(30, height/2-75, 25, 150))

    #control for the left bar
    kb.while_key_pressed(pygame.K_w, bar_l.move_up)
    kb.on_key_released(pygame.K_w, bar_l.stop)

    kb.while_key_pressed(pygame.K_s, bar_l.move_down)
    kb.on_key_released(pygame.K_s, bar_l.stop)

    #creates the right bar
    bar_r = Bar(screen,(255, 255, 255), Rect(width-25-30, height/2-75, 25, 150))
    
    #setup the controls for the rigth bar, depending on the game mode
    if mode == game_mode.VERSUS:
        #controls the right bar
        kb.while_key_pressed(pygame.K_UP, bar_r.move_up)
        kb.on_key_released(pygame.K_UP, bar_r.stop)

        kb.while_key_pressed(pygame.K_DOWN, bar_r.move_down)
        kb.on_key_released(pygame.K_DOWN, bar_r.stop)
    
    elif mode == game_mode.COMPUTER_EASY:
        ia = IA_easy(bar_r, ball)


    #key p pauses the game
    kb.on_key_pressed(pygame.K_p, pause)

    #key p pauses the game
    kb.on_key_pressed(pygame.K_k, pygame.quit)

    #main loop:
    while True:
        #check if the game is paused
        if paused:
            time.sleep(0.01)
            continue

        #clear screen
        screen.fill((0, 0, 0))

        #update the score
        score = font_score.render(str(lives_l)+" - "+str(lives_r),True,(255,255,255))
        screen.blit(score, (width/2, 10))
        
        #check if any of the sides lost a life
        if (ball.rect.left <= 0 or ball.rect.right >= width):
            if(ball.rect.left <= 0):
                lives_l -=1
                if lives_l<=0:
                    pygame.quit()
                    return 1
            else:
                lives_r -=1
                if lives_r<=0:   
                    pygame.quit()                 
                    return 2

            #reset bar position
            bar_l.rect.y = height/2-75
            bar_r.rect.y = height/2-75

            #reset ball position
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
            ball.vel_y -= int(diff)

        if(ball.rect.colliderect(bar_r.rect)):
            if ball.vel_x > 0:
                ball.vel_x = -ball.max_speed
            else: 
                ball.vel_x = ball.max_speed
            delta = bar_r.rect.centery -  ball.center_y
            diff = delta//(bar_r.rect.height/8)
            ball.vel_y -= int(diff)


        #register moves
        ball.move()
        bar_l.move()
        bar_r.move()
        #print("inner"+str(bar_r.rect.centerx))

        #update everything and slows the thread
        pygame.display.update()
        time.sleep(0.01)

#class for the menu
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.title = 'Pong Game'
        self.width = 700
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #title label
        lbl_title = QLabel("PONG", self)
        lbl_title.move(self.width/2 - lbl_title.width()/2, 50)

        #buttons
        btn_human = QPushButton('Against Human', self)
        btn_human.move(self.width/2 - btn_human.width() -10,200)
        btn_human.clicked.connect(self.on_btn_human_click)

        btn_ia = QPushButton('Against IA', self)
        btn_ia.move(self.width/2 +10,200)
        btn_ia.clicked.connect(self.on_btn_ia_click)
        
        self.show()

    @pyqtSlot()
    def on_btn_human_click(self):
        #hides the menu during the game
        self.setVisible(False)
        
        #starts the game and wait until the user wants to exit
        while(True):
            win = game(game_mode.VERSUS)
            win_msg = "LEFT SIDE WINS" if win==2 else "RIGHT SIDE WINS"

            buttonReply = QMessageBox.question(self, win_msg, "Do you want to play again?", QMessageBox.Yes | QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                pass
            if buttonReply == QMessageBox.No:
                break

        self.setVisible(True)
            
    @pyqtSlot()
    def on_btn_ia_click(self):
        #hides the menu during the game
        self.setVisible(False)
        
        #starts the game and wait until the user wants to exit
        while(True):
            win = game(game_mode.COMPUTER_EASY)
            win_msg = "LEFT SIDE WINS" if win==2 else "RIGHT SIDE WINS"

            buttonReply = QMessageBox.question(self, win_msg, "Do you want to play again?", QMessageBox.Yes | QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                pass
            if buttonReply == QMessageBox.No:
                break

        self.setVisible(True)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
