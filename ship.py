import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
	def __init__(self,screen,ai_settings):
	   super().__init__()
	   self.screen=screen
	   self.ai_settings=ai_settings
	   #load the ship image and get its rect.
	   self.image=pygame.image.load('imagess/ship.bmp.bmp')
	   self.rect=self.image.get_rect()
	   self.screen_rect=self.screen.get_rect()
	    
	   #place the ship at bottom centre of the screen.
	   self.rect.centerx=self.screen_rect.centerx
	   self.rect.bottom=self.screen_rect.bottom
	   
	   self.center=float(self.rect.centerx)
	   
	   self.moving_right=False
	   self.moving_left=False
	   
	def update(self):
		if self.moving_right and self.rect.right<self.screen_rect.right:
			self.center+=self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left>0:
			self.center-=self.ai_settings.ship_speed_factor	
			
		self.rect.centerx=self.center	
	
	def blitme(self):
		self.screen.blit(self.image,self.rect)   

