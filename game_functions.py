import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=True
	elif event.key==pygame.K_LEFT:
		ship.moving_left=True
	elif event.key==pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()	
				
def fire_bullet(ai_settings,screen,ship,bullets):
	if len(bullets)<ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def check_keyup_events(event,ship):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
				
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
		if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
			ai_settings.initialize_dynamic_settings()
			# hide the mouse cursor.
			pygame.mouse.set_visible(False)
			stats.reset_stats()
			
			# reset the scoreboard images.
			sb.prep_score()
			sb.prep_level()
			sb.prep_ships()
			
			stats.game_active=True
			bullets.empty()
			aliens.empty()
			
			#create new fleet
			create_fleet(ai_settings,screen,ship,aliens)
			ship.center = ship.screen_rect.centerx			
								
			
def update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button,sb):			
	screen.fill(ai_settings.bg_color)
	#redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	if not stats.game_active:
		play_button.draw_button()
		
	pygame.display.flip()

def update_bullets(ai_settings,screen,ship,aliens,bullets,stats,sb):
	bullets.update()
	
	for bullet in bullets.sprites():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)
	print(len(bullets))	
	
	check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets,stats,sb)

def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets,stats,sb):
	#check whether the bullet and any aliens collide
	#if yes then remove both the bullet and alien from bullets and aliens.
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	
	# now after collision update the score.
	if collisions:
		for shot_alien in collisions.values():
			stats.score += ai_settings.alien_points*len(shot_alien)
			sb.prep_score()
		if stats.score > stats.high_score:
			stats.high_score = stats.score
			sb.prep_high_score()	
	
	if len(aliens) == 0:
		#destroy existing bullets and create a new alien fleet.
		bullets.empty()
		ai_settings.increase_speed()
		
		#Increase level.
		stats.level+=1
		sb.prep_level()
		create_fleet(ai_settings,screen,ship,aliens)

def get_number_aliens_x(ai_settings,alien_width):
	available_space_x=ai_settings.screen_width-2*alien_width
	number_aliens_x=int(available_space_x/(2*alien_width))
	return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
	#determine number of rows the aliens can fit in the screen.
	available_space_y=ai_settings.screen_height-3*alien_height-ship_height
	number_rows=int(available_space_y/(2*alien_height))
	return number_rows
		
def create_alien(ai_settings,screen,aliens,alien_number,number_row):
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=alien_width+(2*alien_width*alien_number)
	alien.rect.x=alien.x
	alien.rect.y=alien.rect.height+2*alien.rect.height*number_row
	aliens.add(alien)		

def create_fleet(ai_settings,screen,ship,aliens):
	alien=Alien(ai_settings,screen)
	number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	
	#create a alien fleet by creating new aliens and appending it to aliens.
	for number_row in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,number_row)
			
def check_fleet_edges(ai_settings,aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break			

def change_fleet_direction(ai_settings,aliens):
	for alien in aliens.sprites():
		alien.rect.y+=ai_settings.fleet_drop_speed
	ai_settings.fleet_direction*=-1	
		
	
def update_aliens(ai_settings,stats,screen,ship,aliens,bullets,sb):
	#update the position of all aliens in the fleet.
	"""check if the fleet is at an edge ,and then update the positions of all 
	aliens in the fleet"""
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)
		
	check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb)
		
def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb):
	#this function is called when any alien hits the ship.
	if stats.ships_left > 0:
		stats.ships_left-=1
		sb.prep_ships()
		bullets.empty()
		aliens.empty()
		# reduce the number of ship by 1.
		#create a new fleet of aliens on the screen.
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center=ship.screen_rect.centerx
		#sleep because the player have to know that ship has been destroyed.
		sleep(0.5)
	else:
		stats.game_active=False
		pygame.mouse.set_visible(True)
		file_name="C:\python_projects\Alien_Invasion\high_score.txt"
		with open(file_name,'w') as fl:
			fl.write(str(stats.high_score))
		
	
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb):
	#if alien touches or passes the ground then call ship_hit.
	for alien in aliens.sprites():
		if alien.rect.bottom>=ship.screen_rect.height:
			ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)
			break
	
	
			
	
