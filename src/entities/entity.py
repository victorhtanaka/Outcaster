"""Base entity class with movement and collision detection."""
import pygame
from math import sin


class Entity(pygame.sprite.Sprite):
    """Base class for all game entities with movement and collision."""
    
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.2
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = None

    def move(self, speed, dt=1.0):
        """Move entity with collision detection."""
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        # Adjust speed by delta time
        # Assuming speed is roughly pixels/frame at 60 FPS
        adjusted_speed = speed * dt * 60

        self.hitbox.x += self.direction.x * adjusted_speed
        self._handle_collision('horizontal')
        self.hitbox.y += self.direction.y * adjusted_speed
        self._handle_collision('vertical')
        self.rect.center = self.hitbox.center

    def _handle_collision(self, direction):
        """Handle collision in specific direction."""
        if not self.obstacle_sprites:
            return
            
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    self._resolve_horizontal_collision(sprite)
                else:
                    self._resolve_vertical_collision(sprite)

    def _resolve_horizontal_collision(self, sprite):
        """Resolve horizontal collision with sprite."""
        if self.direction.x > 0:
            self.hitbox.right = sprite.hitbox.left
        elif self.direction.x < 0:
            self.hitbox.left = sprite.hitbox.right

    def _resolve_vertical_collision(self, sprite):
        """Resolve vertical collision with sprite."""
        if self.direction.y > 0:
            self.hitbox.bottom = sprite.hitbox.top
        elif self.direction.y < 0:
            self.hitbox.top = sprite.hitbox.bottom

    def collision(self, direction):
        """Legacy method for backward compatibility."""
        self._handle_collision(direction)

    def wave_value(self):
        """Calculate wave effect value for visual effects."""
        return 255 if sin(pygame.time.get_ticks()) >= 0 else 0