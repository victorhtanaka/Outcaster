import pygame
from config.settings import *
from config.game_data import monster_data
from src.entities.entity import Entity
from src.core.utils import *
from src.core.resource_manager import ResourceManager

class Enemy(Entity):
	def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_coin):

		# Setup geral
		super().__init__(groups)
		self.sprite_type = 'enemy'

		# Setup gráfico
		self.import_graphics(monster_name)
		self.status = 'idle'
		self.image = self.animations[self.status][self.frame_index]

		# Movimento
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, -10)
		self.obstacle_sprites = obstacle_sprites

		# Stats
		self.monster_name = monster_name
		monster_info = monster_data[self.monster_name]
		self.health = monster_info['health']
		self.coin = monster_info['coin']
		self.speed = monster_info['speed']
		self.attack_damage = monster_info['damage']
		self.resistance = monster_info['resistance']
		self.attack_radius = monster_info['attack_radius']
		self.notice_radius = monster_info['notice_radius']
		self.attack_type = monster_info['attack_type']

		# Sons
		self.death_sound = ResourceManager().load_sound('gameinfo/audio/death.wav')
		self.hit_sound = ResourceManager().load_sound('gameinfo/audio/hit.wav')
		self.attack_sound = ResourceManager().load_sound(monster_info['attack_sound'])
		self.death_sound.set_volume(0.2)
		self.hit_sound.set_volume(0.2)
		self.attack_sound.set_volume(0.2)

		# Interação com player
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
		self.damage_player = damage_player
		self.trigger_death_particles = trigger_death_particles
		self.add_coin = add_coin

		# Timer de invencibilidade
		self.vulnerable = True
		self.hit_time = None
		self.invincibility_duration = 300

		# AI - Pathfinding e evasão de obstáculos
		self.stuck_time = 0
		self.stuck_threshold = 60  # frames
		self.last_pos = pygame.math.Vector2(self.rect.center)
		self.stuck_directions = []  # Direções bloqueadas
		self.ai_update_timer = 0
		self.ai_update_frequency = 10  # Atualizar IA a cada 10 frames

	def import_graphics(self,name):
		self.animations = {'idle':[],'move':[],'attack':[]}
		main_path = f'gameinfo/graphics/monsters/{name}/'
		for animation in self.animations.keys():
			self.animations[animation] = import_folder(main_path + animation)

	def get_player_distance_direction(self,player):
		enemy_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(player.rect.center)
		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance,direction)

	def get_status(self, player):
		distance = self.get_player_distance_direction(player)[0]

		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				self.frame_index = 0
			self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = 'move'
		else:
			self.status = 'idle'

	def _check_collision_ahead(self, direction, test_distance=20):
		"""Verifica se há colisão na direção indicada."""
		if direction.magnitude() == 0:
			return False
		
		normalized = direction.normalize()
		test_pos = self.hitbox.center + (normalized * test_distance)
		test_rect = self.hitbox.copy()
		test_rect.center = test_pos
		
		for sprite in self.obstacle_sprites:
			if test_rect.colliderect(sprite.hitbox):
				return True
		return False

	def _get_alternative_direction(self, player_direction):
		"""Encontra uma direção alternativa quando há obstáculo."""
		# Tentar direções perpendiculares
		perpendicular_dirs = [
			pygame.math.Vector2(-player_direction.y, player_direction.x),  # 90 graus
			pygame.math.Vector2(player_direction.y, -player_direction.x),   # -90 graus
		]
		
		# Encontrar a melhor direção alternativa que não bate em obstáculo
		for alt_dir in perpendicular_dirs:
			if alt_dir.magnitude() > 0 and not self._check_collision_ahead(alt_dir):
				return alt_dir.normalize()
		
		# Se tudo está bloqueado, tentar recuar
		return -player_direction.normalize() if player_direction.magnitude() > 0 else pygame.math.Vector2()

	def _detect_stuck(self):
		"""Detecta se o inimigo está preso/travado."""
		current_pos = pygame.math.Vector2(self.rect.center)
		distance_moved = (current_pos - self.last_pos).magnitude()
		
		if distance_moved < 1.0:  # Movimento mínimo
			self.stuck_time += 1
		else:
			self.stuck_time = 0
		
		self.last_pos = current_pos
		return self.stuck_time > self.stuck_threshold

	def actions(self,player):
		if self.status == 'attack':
			self.attack_time = pygame.time.get_ticks()
			self.damage_player(self.attack_damage,self.attack_type)
			self.attack_sound.play()
		elif self.status == 'move':
			player_direction = self.get_player_distance_direction(player)[1]
			
			# Verificar colisão frontal
			if self._check_collision_ahead(player_direction):
				# Se há obstáculo, buscar caminho alternativo
				self.direction = self._get_alternative_direction(player_direction)
			else:
				self.direction = player_direction
				self.stuck_time = 0  # Reset se conseguir se mover
		
			# Se detectar que está preso, mudar comportamento
			if self._detect_stuck():
				self.direction = self._get_alternative_direction(player_direction)
		else:
			self.direction = pygame.math.Vector2()

	def animate(self):
		animation = self.animations[self.status]
		
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True

		if not self.vulnerable:
			if current_time - self.hit_time >= self.invincibility_duration:
				self.vulnerable = True

	def get_damage(self,player,attack_type):
		if self.vulnerable:
			self.hit_sound.play()
			self.direction = self.get_player_distance_direction(player)[1]
			if attack_type == 'weapon':
				self.health -= player.get_full_weapon_damage()
			else:
				self.health -= player.get_full_magic_damage()
			self.hit_time = pygame.time.get_ticks()
			self.vulnerable = False
			return True
		return False

	def check_death(self):
		if self.health <= 0:
			self.kill()
			self.trigger_death_particles(self.rect.center,self.monster_name)
			self.add_coin(self.coin)
			self.death_sound.play()

	def hit_reaction(self):
		if not self.vulnerable:
			self.direction *= -self.resistance

	def update(self, dt=1.0):
		self.hit_reaction()
		self.move(self.speed, dt)
		self.animate()
		self.cooldowns()
		self.check_death()

	def enemy_update(self,player):
		self.get_status(player)
		self.actions(player)