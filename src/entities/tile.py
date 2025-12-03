"""Tile entity for map objects and terrain."""
import pygame
from config.settings import TILESIZE, HITBOX_OFFSET


class Tile(pygame.sprite.Sprite):
    """Represents a tile in the game world (object, grass, boundary, etc)."""
    
    def __init__(self, pos, groups, sprite_type, surface=None):
        super().__init__(groups)
        self.sprite_type = sprite_type
        
        # Use provided surface or create default
        self.image = surface if surface else pygame.Surface((TILESIZE, TILESIZE))
        
        # Set rect position based on sprite type
        self._setup_rect(pos)
        
        # Create hitbox with offset
        self._setup_hitbox()

    def _setup_rect(self, pos):
        """Setup rectangle position based on sprite type."""
        if self.sprite_type == 'object':
            # Objects are positioned one tile higher
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

    def _setup_hitbox(self):
        """Setup hitbox with type-specific offset."""
        y_offset = HITBOX_OFFSET.get(self.sprite_type, 0)
        self.hitbox = self.rect.inflate(0, y_offset)