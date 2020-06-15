import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	# a class that manages bullets fired from the ship.
	def __init__(self,ai_settings,screen,ship):
		super().__init__()
		self.screen=screen
		#now create a bullet.
		self.rect=pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
		self.rect.centerx=ship.rect.centerx
		self.rect.top=ship.rect.top
		
		#store the bullet position as  a decimal value.
		self.y=float(self.rect.y)
		
		self.color=ai_settings.bullet_color
		self.speed_factor=ai_settings.bullet_speed_factor
		
	def update(self):
		#update the decimal position of the bullet
		self.y-=self.speed_factor
		self.rect.y=self.y
		
		
	def draw_bullet(self):
		#draw bullet to the screen.
		pygame.draw.rect(self.screen,self.color,self.rect)		
