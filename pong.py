import pygame
import _thread, time
from enum import Enum

class game_mode(Enum):
	VERSUS = 0
	COMPUTER_EASY = 1
	COMPUTER_MEDIUM = 2
	COMPUTER_HARD = 3

class Bar:
	def __init__(self, surface, color, rect):
		self.surface = surface
		self.color = color
		self.rect = rect
		pygame.draw.rect(self.surface, self.color, rect)

		self.speed = 4
		self.vel = 0

	def move_up(self):
		self.vel = -self.speed

	def move_down(self):
		self.vel = self.speed

	def stop(self):
		self.vel = 0

	def move(self):
		self.rect.y += self.vel
		if (self.surface.get_rect().contains(self.rect)):
			pygame.draw.rect(self.surface, self.color, self.rect)
		else:
			self.rect.y -= self.vel			
			pygame.draw.rect(self.surface, self.color, self.rect)



class Ball:
	def __init__(self, surface, color, center, radius):
		self.surface = surface
		self.color = color
		self.center_x, self.center_y = center
		self.radius = radius 
		self.rect = pygame.draw.circle(surface, color, (self.center_x, self.center_y), radius)

		self.vel_x = 0
		self.vel_y = 0
		self.max_speed = 6

	def move(self):
		if self.vel_x > self.max_speed:
			self.vel_x = self.max_speed
		if self.vel_y > self.max_speed:
			self.vel_y = self.max_speed

		self.center_x += self.vel_x
		self.center_y += self.vel_y
		self.rect = pygame.draw.circle(self.surface, self.color, (self.center_x, self.center_y), self.radius)



class IA_easy:
	def __init__(self, bar, ball):
		self.bar = bar
		self.ball = ball

		_thread.start_new_thread(self.play,())

	def play(self):
		tollerance = 20
		while True:
			bar_pos = self.bar.rect.centery
			ball_pos = self.ball.center_y

			pos = bar_pos-ball_pos

			if pos - tollerance < 0:
				self.bar.move_down()
			elif pos + tollerance > 0:
				self.bar.move_up()
			else:
				self.bar.stop()
			time.sleep(0.01)