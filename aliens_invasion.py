import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	pygame.init()
	ai_settings=Settings()
	screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("FP_Alien Invansion")
	ship=Ship(screen,ai_settings)
	#make a group to store bullets in.
	bullets=Group()
	#make a group to store aliens in.
	aliens=Group()
	#create first fleet of aliens on the screen.
	gf.create_fleet(ai_settings,screen,ship,aliens)
	stats=GameStats(ai_settings)
	play_button=Button(ai_settings,screen,"PLAY")
	sb=Scoreboard(ai_settings,screen,stats)
	
	while True:
		# watch for keyboard and mouse events.
		gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings,screen,ship,aliens,bullets,stats,sb)
			gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets,sb)
			
		# redraw the screen during each pass through the loop.
		gf.update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button,sb)
		
		
run_game()
				
	
	
			
			

