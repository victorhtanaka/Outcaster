"""NPC entity with dialogue interactions."""
import pygame
from src.entities.entity import Entity
from config.settings import HITBOX_OFFSET, INTERACTION_DISTANCE
from src.core.utils import import_folder
from typing import List, Optional


class NPC(Entity):
    """Non-player character with dialogue capability."""
    
    def __init__(self, pos, groups, obstacle_sprites, npc_id: str, 
                 sprite_path: str = None, dialogues: List[str] = None):
        super().__init__(groups)
        
        # Basic setup
        self.npc_id = npc_id
        self.obstacle_sprites = obstacle_sprites
        
        # Load sprite
        if sprite_path:
            self.image = pygame.image.load(sprite_path).convert_alpha()
        else:
            # Default NPC sprite
            self.image = pygame.Surface((64, 64))
            self.image.fill((100, 100, 200))
        
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, HITBOX_OFFSET.get('player', -26))
        
        # Dialogue setup
        self.dialogues = dialogues or ["Olá, viajante!", "Como posso ajudar?"]
        self.can_interact = True
        self.is_interacting = False
        
        # Animation (if using animated sprites)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animations = {}
        
        # Status
        self.status = 'idle'
    
    def import_npc_assets(self, base_path: str):
        """Import NPC animation assets."""
        self.animations = {
            'idle': import_folder(f'{base_path}/idle'),
            'talk': import_folder(f'{base_path}/talk') if True else []
        }
        
        if self.animations['idle']:
            self.image = self.animations['idle'][0]
    
    def check_player_proximity(self, player_pos) -> bool:
        """Check if player is close enough to interact."""
        distance = pygame.math.Vector2(player_pos).distance_to(self.rect.center)
        return distance < INTERACTION_DISTANCE
    
    def get_screen_position(self, offset):
        """Get NPC position on screen with camera offset."""
        return (self.rect.centerx - offset.x, self.rect.centery - offset.y)
    
    def animate(self):
        """Animate NPC sprite."""
        if self.status in self.animations and self.animations[self.status]:
            self.frame_index += self.animation_speed
            
            if self.frame_index >= len(self.animations[self.status]):
                self.frame_index = 0
            
            self.image = self.animations[self.status][int(self.frame_index)]
    
    def update(self):
        """Update NPC state."""
        self.animate()