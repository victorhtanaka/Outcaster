"""Collision detection system."""
import pygame
from typing import List, Set
from .camera import SpatialHash


class CollisionSystem:
    """Handles collision detection and resolution."""
    
    def __init__(self):
        self.spatial_hash = SpatialHash(cell_size=128)
    
    def update_spatial_hash(self, sprites):
        """Rebuild spatial hash with current sprite positions."""
        self.spatial_hash.rebuild(sprites)
    
    def check_collision(self, entity, direction: str, obstacles) -> bool:
        """Check collision in a direction."""
        if not hasattr(entity, 'hitbox'):
            return False
        
        # Use spatial hash to get nearby obstacles
        nearby = self.spatial_hash.query(entity.hitbox)
        
        for obstacle in nearby:
            if obstacle == entity or not hasattr(obstacle, 'hitbox'):
                continue
            
            if obstacle.hitbox.colliderect(entity.hitbox):
                return True
        
        return False
    
    def resolve_collision(self, entity, direction: str, obstacles):
        """Resolve collision by adjusting position."""
        if not hasattr(entity, 'hitbox') or not hasattr(entity, 'direction'):
            return
        
        nearby = self.spatial_hash.query(entity.hitbox)
        
        for obstacle in nearby:
            if obstacle == entity or not hasattr(obstacle, 'hitbox'):
                continue
            
            if obstacle.hitbox.colliderect(entity.hitbox):
                if direction == 'horizontal':
                    if entity.direction.x > 0:  # Moving right
                        entity.hitbox.right = obstacle.hitbox.left
                    elif entity.direction.x < 0:  # Moving left
                        entity.hitbox.left = obstacle.hitbox.right
                
                elif direction == 'vertical':
                    if entity.direction.y > 0:  # Moving down
                        entity.hitbox.bottom = obstacle.hitbox.top
                    elif entity.direction.y < 0:  # Moving up
                        entity.hitbox.top = obstacle.hitbox.bottom
        
        # Update rect to match hitbox
        if hasattr(entity, 'rect'):
            entity.rect.center = entity.hitbox.center
    
    def get_collisions(self, rect: pygame.Rect, group: pygame.sprite.Group) -> Set:
        """Get all sprites colliding with a rect."""
        nearby = self.spatial_hash.query(rect)
        colliding = set()
        
        for sprite in nearby:
            if hasattr(sprite, 'hitbox') and sprite.hitbox.colliderect(rect):
                colliding.add(sprite)
        
        return colliding
