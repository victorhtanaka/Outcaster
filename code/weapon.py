import pygame 

class Weapon(pygame.sprite.Sprite):
	def __init__(self,player,groups):
		super().__init__(groups)
		self.sprite_type = 'weapon'
		direction = player.status.split('_')[0]

		# graphic
		full_path = f'gameinfo/graphics/weapons/{player.weapon}/{direction}.png'
		self.image = pygame.image.load(full_path).convert_alpha()
		
		# placement
		if direction == 'right':
			self.rect = self.image.get_rect(midleft = player.rect.center + pygame.math.Vector2(30,16))
		elif direction == 'left': 
			self.rect = self.image.get_rect(midright = player.rect.center + pygame.math.Vector2(-30,16))
		elif direction == 'down':
			self.rect = self.image.get_rect(midtop = player.rect.center + pygame.math.Vector2(-10,30))
		else:
			self.rect = self.image.get_rect(midbottom = player.rect.center + pygame.math.Vector2(-10,-30))