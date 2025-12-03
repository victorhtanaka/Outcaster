"""Weapon sprite system."""
import pygame


class Weapon(pygame.sprite.Sprite):
    """Weapon sprite that follows player direction."""
    
    # Weapon positioning offsets for each direction
    POSITION_OFFSETS = {
        'right': ('midleft', pygame.math.Vector2(30, 16)),
        'left': ('midright', pygame.math.Vector2(-30, 16)),
        'down': ('midtop', pygame.math.Vector2(-10, 30)),
        'up': ('midbottom', pygame.math.Vector2(-10, -30))
    }
    
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        
        # Get player direction
        direction = player.status.split('_')[0]
        
        # Load weapon graphic
        self.image = self._load_weapon_image(player.weapon, direction)
        
        # Position weapon based on direction
        self.rect = self._position_weapon(player, direction)
    
    def _load_weapon_image(self, weapon_type, direction):
        """Load weapon image for specific direction."""
        path = f'gameinfo/graphics/weapons/{weapon_type}/{direction}.png'
        return pygame.image.load(path).convert_alpha()
    
    def _position_weapon(self, player, direction):
        """Position weapon relative to player."""
        anchor, offset = self.POSITION_OFFSETS.get(direction, ('midleft', pygame.math.Vector2(0, 0)))
        position = player.rect.center + offset
        return self.image.get_rect(**{anchor: position})