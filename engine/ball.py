import pygame
import random

class Ball(object):
	def __init__(self, x, y, width, height, speed):
		self.speed = speed
		self.rect = pygame.Rect(x, y, width, height)
		self.momentum = pygame.math.Vector2()
		self.reset(0, 0)
		self.x = x
		self.y = y	

	def reset(self, canvas_width, canvas_height):
		self.x = int(canvas_width) / 2
		self.y = int(canvas_height) / 2
		angle = random.random() * 90 - 45
		if random.random() > 0.5:
			angle = angle + 180
		self.set_orientation(angle * -1)

	def bounce(self, vertical=True):
		if vertical:
			self.momentum.x = self.momentum.x * -1
		else:
			self.momentum.y = self.momentum.y * -1
		r, angle = self.momentum.as_polar()
		self.set_orientation(angle+(random.random()-0.5)*0)

	def set_orientation(self, angle):
		self.momentum.from_polar((self.speed, angle))

	def step(self):
		self.x += self.momentum.x
		self.y += self.momentum.y

	def draw(self, surface):
		self.rect.x = self.x
		self.rect.y = self.y
		pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)