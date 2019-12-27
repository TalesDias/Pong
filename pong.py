import pygame

class Bar:
	def __init__(self, surface, color, rect):
		self.surface = surface
		self.color = color
		self.rect = rect
		pygame.draw.rect(self.surface, self.color, rect)

		self.speed = 5
		self.vel = 0

	def move_up(self):
		self.vel = self.speed

	def move_down(self):
		self.vel = -self.speed

	def stop(self):
		self.vel = 0

	def move(self):
		self.rect.y += self.vel
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
		self.max_speed = 4

	def move(self):
		self.center_x += self.vel_x
		self.center_y += self.vel_y
		self.rect = pygame.draw.circle(self.surface, self.color, (self.center_x, self.center_y), self.radius)