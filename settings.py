class Settings():
	# a class to store all settings for alien invasion.
	
	def __init__(self):
		"""intilizing game settings"""
		# screen settings
		self.screen_width=1200
		self.screen_height=700
		self.bg_color=(230,230,230)
		#ship setting
		
		self.ship_limit=3
		#bullet setting
		self.bullet_width=3
		self.bullet_height=15
		self.bullet_color=(60,60,60)
		self.bullets_allowed=10
		
		#Alien settings
		self.fleet_drop_speed=10
		
		#how quickly the game speeds up.
		self.speedup_scale=1.1
		#how quickly the alien point values increase.
		self.score_scale = 1.5
		self.initialize_dynamic_settings()
	
	def initialize_dynamic_settings(self):
		self.ship_speed_factor=1.5
		# fleet direction of 1 represents right and -1 rep left
		self.fleet_direction=1
		self.alien_speed_factor=25
		self.bullet_speed_factor=3
		self.alien_points=50
		
	def increase_speed(self):
		"""increase speed settings"""
		self.ship_speed_factor*=self.speedup_scale
		self.bullet_speed_factor*=self.speedup_scale
		self.alien_speed_factor*=self.speedup_scale	
		self.alien_points=int(self.alien_points*self.score_scale)
		print(self.alien_points)
			
		
		
