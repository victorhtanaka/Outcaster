import pygame
from settings import *
from pygame.math import Vector2
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('gameinfo/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # IMPORTAR PLAYER ASSETS
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # Movimento e ataque
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # Esquiva
        self.dodging = False
        self.dodge_duration = 200
        self.dodge_time = None
        self.dodge_speed = 10  # Velocidade de esquiva
        self.dodge_distance = 10  # Distância de esquiva

        # Weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # Stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.exp = 123
        self.speed = self.stats['speed']

        # Dodge cooldown
        self.dodge_cooldown = 1000
        self.last_dodge_time = pygame.time.get_ticks()

    def import_player_assets(self):
        character_path = 'gameinfo/graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': [],
                           'right_dodge': [], 'left_dodge': [], 'up_dodge': [], 'down_dodge': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            if 'dodge' in animation:
                self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking and not self.dodging:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            if keys[pygame.K_LSHIFT] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.dodge()

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]
            print(self.status)

    def get_status(self):
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

        if self.dodging:
            self.direction.x = 0
            self.direction.y = 0
            if not 'dodge' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_dodge')
                else:
                    self.status = self.status + '_dodge'
        else:
            if 'dodge' in self.status:
                self.status = self.status.replace('_dodge', '')

        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status and not 'dodge' in self.status:
                self.status = self.status + '_idle'

    def dodge(self):
        if self.direction.length() == 0:
            return
    
        if not self.dodging and pygame.time.get_ticks() - self.last_dodge_time >= self.dodge_cooldown:
            self.dodging = True
            self.dodge_time = pygame.time.get_ticks()
            self.last_dodge_time = pygame.time.get_ticks()
            dodge_distance = self.dodge_speed * (self.dodge_duration / 1000)
            self.direction = self.direction.normalize()
            self.rect.center += self.direction * dodge_distance

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if not self.dodging:
            self.hitbox.x += self.direction.x * speed
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * speed
            self.collision('vertical')
            self.rect.center = self.hitbox.center
        else:
            dodge_distance = self.dodge_speed * (self.dodge_duration / 1000)
            self.hitbox.x += self.direction.x * dodge_distance
            self.hitbox.y += self.direction.y * dodge_distance
            self.rect.center = self.hitbox.center

    def collision(self, direction):
        if not self.dodging:
            if direction == 'horizontal':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:  # direita
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # esquerda
                            self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # baixo
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # cima
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if self.dodging:
            if current_time - self.dodge_time >= self.dodge_duration:
                self.dodging = False

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
