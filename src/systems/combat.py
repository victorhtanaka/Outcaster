"""Combat system."""
import pygame
from src.core import event_bus, Events


class CombatSystem:
    """Handles combat mechanics."""
    
    def __init__(self):
        self.attack_sprites = pygame.sprite.Group()
    
    def create_attack(self, attacker, attack_type: str, damage: int, 
                     position: tuple, size: tuple):
        """Create an attack hitbox."""
        attack = AttackSprite(
            attack_type=attack_type,
            damage=damage,
            position=position,
            size=size,
            owner=attacker
        )
        self.attack_sprites.add(attack)
        return attack
    
    def process_attacks(self, targets: pygame.sprite.Group):
        """Process all active attacks against targets."""
        for attack in self.attack_sprites:
            hit_sprites = pygame.sprite.spritecollide(
                attack, targets, False
            )
            
            for target in hit_sprites:
                if target != attack.owner:
                    self.apply_damage(attack, target)
    
    def apply_damage(self, attack, target):
        """Apply damage from attack to target."""
        if hasattr(target, 'take_damage'):
            target.take_damage(attack.damage)
        
        # Publish damage event
        event_bus.publish(
            Events.ENEMY_DIED if hasattr(target, 'sprite_type') 
            and target.sprite_type == 'enemy' else Events.PLAYER_DAMAGED,
            damage=attack.damage,
            attack_type=attack.attack_type
        )
    
    def clear_attacks(self):
        """Clear all attack sprites."""
        self.attack_sprites.empty()


class AttackSprite(pygame.sprite.Sprite):
    """Temporary attack hitbox sprite."""
    
    def __init__(self, attack_type: str, damage: int, 
                 position: tuple, size: tuple, owner):
        super().__init__()
        self.attack_type = attack_type
        self.damage = damage
        self.owner = owner
        
        # Create invisible hitbox
        self.image = pygame.Surface(size)
        self.image.set_alpha(0)  # Invisible
        self.rect = self.image.get_rect(center=position)
        self.hitbox = self.rect.copy()
        
        # Lifetime
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 200  # milliseconds
    
    def update(self):
        """Update attack sprite."""
        # Remove after lifetime expires
        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.kill()
