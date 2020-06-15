import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	#alien class representing a single alien.
	def __init__(self,ai_settings,screen):
		super().__init__()
		self.screen=screen
		self.ai_settings=ai_settings
		
		self.image=pygame.image.load('imagess/alien.bmp')
		self.rect=self.image.get_rect()
		
		#start each new alien near the top left of the screen.
		self.rect.x=self.rect.width
		self.rect.y=self.rect.height
		
		self.x=float(self.rect.x)
		
	def check_edges(self):
		if self.rect.right>=self.ai_settings.screen_width:
			return True
		elif self.rect.x<=0:
			return True		
		
	def update(self):
		#move the aliens right
		self.x+=(self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction)
		self.rect.x=self.x	
