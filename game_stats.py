class GameStats():
	""" Track staistics for aliens."""
	def __init__(self,ai_settings):
		self.ai_settings=ai_settings
		self.reset_stats()
		self.game_active=False
		# the high score.
		file_name="C:\python_projects\Alien_Invasion\high_score.txt"
		with open(file_name) as fobj:
			high_scores=fobj.read()
		
		self.high_score = int(high_scores)
		
	def reset_stats(self):
		self.ships_left=self.ai_settings.ship_limit
		self.score=0
		self.level=1
