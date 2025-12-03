"""Entity components for composition pattern."""
from abc import ABC, abstractmethod
import pygame
from math import sin
from typing import Tuple, Optional


class Component(ABC):
    """Base component class."""
    
    def __init__(self, entity):
        self.entity = entity
    
    @abstractmethod
    def update(self, dt: float = 0):
        """Update component."""
        pass


class TransformComponent(Component):
    """Handles position and movement."""
    
    def __init__(self, entity, pos: Tuple[int, int]):
        super().__init__(entity)
        self.position = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2()
    
    def update(self, dt: float = 0):
        """Update is handled by movement system."""
        pass


class SpriteComponent(Component):
    """Handles sprite rendering and animations."""
    
    def __init__(self, entity, image_path: str):
        super().__init__(entity)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.animations = {}
        self.current_animation = None
        self.frame_index = 0
        self.animation_speed = 0.15
    
    def set_animations(self, animations: dict):
        """Set animation dictionary."""
        self.animations = animations
    
    def play_animation(self, animation_name: str):
        """Play an animation."""
        if animation_name in self.animations:
            self.current_animation = animation_name
    
    def update(self, dt: float = 0):
        """Update animation."""
        if self.current_animation and self.animations:
            animation = self.animations.get(self.current_animation, [])
            if animation:
                self.frame_index += self.animation_speed
                if self.frame_index >= len(animation):
                    self.frame_index = 0
                self.image = animation[int(self.frame_index)]


class HealthComponent(Component):
    """Handles health and damage."""
    
    def __init__(self, entity, max_health: int):
        super().__init__(entity)
        self.max_health = max_health
        self.current_health = max_health
        self.vulnerable = True
        self.invulnerability_duration = 500
        self.hit_time = None
    
    def take_damage(self, amount: int):
        """Take damage."""
        if self.vulnerable and self.current_health > 0:
            self.current_health = max(0, self.current_health - amount)
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()
            return True
        return False
    
    def heal(self, amount: int):
        """Heal health."""
        self.current_health = min(self.max_health, self.current_health + amount)
    
    def is_alive(self) -> bool:
        """Check if entity is alive."""
        return self.current_health > 0
    
    def update(self, dt: float = 0):
        """Update invulnerability."""
        if not self.vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= self.invulnerability_duration:
                self.vulnerable = True


class StatsComponent(Component):
    """Handles entity stats."""
    
    def __init__(self, entity, stats: dict):
        super().__init__(entity)
        self.stats = stats.copy()
    
    def get_stat(self, stat_name: str, default=0):
        """Get a stat value."""
        return self.stats.get(stat_name, default)
    
    def set_stat(self, stat_name: str, value):
        """Set a stat value."""
        self.stats[stat_name] = value
    
    def modify_stat(self, stat_name: str, amount):
        """Modify a stat by an amount."""
        if stat_name in self.stats:
            self.stats[stat_name] += amount
    
    def update(self, dt: float = 0):
        """Stats don't need regular updates."""
        pass


class CollisionComponent(Component):
    """Handles collision detection."""
    
    def __init__(self, entity, hitbox_offset: Tuple[int, int] = (0, 0)):
        super().__init__(entity)
        self.hitbox_offset = hitbox_offset
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.obstacle_sprites = None
    
    def set_obstacles(self, obstacle_sprites):
        """Set obstacle sprites group."""
        self.obstacle_sprites = obstacle_sprites
    
    def update_hitbox(self, rect: pygame.Rect):
        """Update hitbox based on entity rect."""
        self.hitbox = rect.inflate(*self.hitbox_offset)
    
    def check_collision(self, direction: str) -> bool:
        """Check collision in a direction."""
        if not self.obstacle_sprites:
            return False
        
        for sprite in self.obstacle_sprites:
            if hasattr(sprite, 'hitbox') and sprite.hitbox.colliderect(self.hitbox):
                return True
        return False
    
    def update(self, dt: float = 0):
        """Collision is handled by collision system."""
        pass


class AIComponent(Component):
    """Handles AI behavior."""
    
    def __init__(self, entity, ai_type: str = 'aggressive'):
        super().__init__(entity)
        self.ai_type = ai_type
        self.target = None
        self.state = 'idle'
        self.attack_radius = 80
        self.notice_radius = 300
    
    def set_target(self, target):
        """Set AI target."""
        self.target = target
    
    def get_distance_to_target(self) -> float:
        """Get distance to target."""
        if not self.target or not hasattr(self.entity, 'rect'):
            return float('inf')
        
        entity_pos = pygame.math.Vector2(self.entity.rect.center)
        target_pos = pygame.math.Vector2(self.target.rect.center)
        return (target_pos - entity_pos).magnitude()
    
    def get_direction_to_target(self) -> pygame.math.Vector2:
        """Get direction to target."""
        if not self.target or not hasattr(self.entity, 'rect'):
            return pygame.math.Vector2()
        
        entity_pos = pygame.math.Vector2(self.entity.rect.center)
        target_pos = pygame.math.Vector2(self.target.rect.center)
        distance = (target_pos - entity_pos).magnitude()
        
        if distance > 0:
            return (target_pos - entity_pos).normalize()
        return pygame.math.Vector2()
    
    def update(self, dt: float = 0):
        """Update AI behavior."""
        distance = self.get_distance_to_target()
        
        if distance <= self.attack_radius:
            self.state = 'attack'
        elif distance <= self.notice_radius:
            self.state = 'chase'
        else:
            self.state = 'idle'
