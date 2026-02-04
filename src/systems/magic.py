"""Magic system for player spells."""
import pygame
from config.settings import TILESIZE
from random import randint
from src.core.resource_manager import ResourceManager

class MagicPlayer:
    """Handles player magic spells and effects."""
    
    # Direction vectors
    DIRECTIONS = {
        'right': pygame.math.Vector2(1, 0),
        'left': pygame.math.Vector2(-1, 0),
        'up': pygame.math.Vector2(0, -1),
        'down': pygame.math.Vector2(0, 1)
    }
    
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': ResourceManager().load_sound('gameinfo/audio/heal.wav'),
            'flame': ResourceManager().load_sound('gameinfo/audio/Fire.wav')
        }

    def heal(self, player, strength, cost, groups):
        """Cast heal spell on player."""
        if not self._can_cast(player, cost):
            return
        
        self.sounds['heal'].play()
        self._apply_healing(player, strength, cost)
        self._create_heal_particles(player, groups)

    def flame(self, player, cost, groups):
        """Cast flame spell in player's direction."""
        if not self._can_cast(player, cost):
            return
        
        self.sounds['flame'].play()
        player.energy -= cost
        
        direction = self._get_player_direction(player)
        self._create_flame_particles(player, direction, groups)

    def _can_cast(self, player, cost):
        """Check if player has enough energy to cast."""
        return player.energy >= cost

    def _apply_healing(self, player, strength, cost):
        """Apply healing to player."""
        player.health = min(player.health + strength, player.stats['health'])
        player.energy -= cost

    def _create_heal_particles(self, player, groups):
        """Create heal visual effect particles."""
        self.animation_player.create_particles('aura', player.rect.center, groups)
        heal_pos = player.rect.center + pygame.math.Vector2(0, -70)
        self.animation_player.create_particles('heal', heal_pos, groups)

    def _get_player_direction(self, player):
        """Get player's facing direction as vector."""
        direction_name = player.status.split('_')[0]
        return self.DIRECTIONS.get(direction_name, pygame.math.Vector2(0, 1))

    def _create_flame_particles(self, player, direction, groups):
        """Create flame particles in direction."""
        spread = TILESIZE // 3
        
        for i in range(1, 6):
            pos = self._calculate_flame_position(player, direction, i, spread)
            self.animation_player.create_particles('flame', pos, groups)

    def _calculate_flame_position(self, player, direction, distance, spread):
        """Calculate position for flame particle."""
        offset = distance * TILESIZE
        random_offset = randint(-spread, spread)
        
        if direction.x != 0:
            x = player.rect.centerx + (direction.x * offset) + random_offset
            y = player.rect.centery + random_offset
        else:
            x = player.rect.centerx + random_offset
            y = player.rect.centery + (direction.y * offset) + random_offset
        
        return (x, y)