"""Game UI for displaying player stats and info."""
import pygame
from config.settings import *
from config.game_data import magic_data, weapon_data
from src.core.resource_manager import ResourceManager

class UI:
    """Handles in-game UI display for player stats."""
    
    # UI positioning constants
    HEALTH_BAR_POS = (300, 180)
    ENERGY_BAR_POS = (300, 204)
    COIN_POS = (1590, 880)
    MAGIC_BOX_POS = (300, 825)
    
    # Minimap
    MINIMAP_POS = (WIDTH - 250, 50)
    MINIMAP_SIZE = (200, 200)
    MINIMAP_ZOOM = 0.15

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT_THIN, UI_FONT_SIZE_THIN)
        
        # Setup stat bars
        self.health_bar_rect = pygame.Rect(*self.HEALTH_BAR_POS, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(*self.ENERGY_BAR_POS, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        
        # Minimap surface
        self.minimap_surf = pygame.Surface(self.MINIMAP_SIZE)
        self.minimap_rect = self.minimap_surf.get_rect(topleft=self.MINIMAP_POS)
        self.minimap_surf.set_alpha(200)

        # Load magic graphics
        self.magic_graphics = self._load_magic_graphics()

        # Cache for coin text
        self.last_coin_amount = -1
        self.coin_surf = None
        self.coin_rect = None
    
    def _load_magic_graphics(self):
        """Load all magic spell graphics."""
        graphics = []
        for magic in magic_data.values():
            image = ResourceManager().load_image(magic['graphic'])
            graphics.append(image)
        return graphics
    
    def show_bar(self, current, max_amount, bg_rect, color):
        """Display a stat bar (health/energy)."""
        # Draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        
        # Calculate and draw current value
        ratio = current / max_amount if max_amount > 0 else 0
        current_rect = bg_rect.copy()
        current_rect.width = int(bg_rect.width * ratio)
        
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
    
    def show_coin(self, coin):
        """Display player coin count."""
        coin = int(coin)
        if coin != self.last_coin_amount:
            self.last_coin_amount = coin
            self.coin_surf = self.font.render(str(coin), False, TEXT_COLOR)
            self.coin_rect = self.coin_surf.get_rect(center=self.COIN_POS)
            
        # Draw background box
        bg_rect = self.coin_rect.inflate(20, 20)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        
        # Draw text and border
        self.display_surface.blit(self.coin_surf, self.coin_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
    
    def _draw_selection_box(self, has_switched):
        """Draw magic selection box."""
        bg_rect = pygame.Rect(*self.MAGIC_BOX_POS, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        
        border_color = UI_BORDER_COLOR_ACTIVE if has_switched else UI_BORDER_COLOR
        pygame.draw.rect(self.display_surface, border_color, bg_rect, 3)
        
        return bg_rect
    
    def selection_box(self, left, top, has_switched):
        """Legacy method for backward compatibility."""
        return self._draw_selection_box(has_switched)
    
    def magic_overlay(self, magic_index, has_switched):
        """Display current magic selection."""
        bg_rect = self._draw_selection_box(has_switched)
        
        # Draw magic icon
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)
    
    def show_minimap(self, player, sprites):
        """Draw a radar-style minimap."""
        self.minimap_surf.fill(UI_BG_COLOR)
        pygame.draw.rect(self.minimap_surf, UI_BORDER_COLOR, (0, 0, *self.MINIMAP_SIZE), 2)
        
        center_x = self.MINIMAP_SIZE[0] // 2
        center_y = self.MINIMAP_SIZE[1] // 2
        
        # Draw player in center
        pygame.draw.circle(self.minimap_surf, 'white', (center_x, center_y), 4)
        
        # Draw entities
        for sprite in sprites:
            if not hasattr(sprite, 'sprite_type'): continue
            
            # Calculate relative position
            rel_x = (sprite.rect.centerx - player.rect.centerx) * self.MINIMAP_ZOOM
            rel_y = (sprite.rect.centery - player.rect.centery) * self.MINIMAP_ZOOM
            
            # Clamp to minimap bounds (optional, currently just clipping via surface)
            if abs(rel_x) < center_x and abs(rel_y) < center_y:
                color = None
                if sprite.sprite_type == 'enemy':
                    color = 'red'
                elif sprite.sprite_type == 'object':
                    color = 'gray'
                elif sprite.sprite_type == 'npc':
                    color = 'green'
                    
                if color:
                    pygame.draw.circle(self.minimap_surf, color, (int(center_x + rel_x), int(center_y + rel_y)), 3)

        self.display_surface.blit(self.minimap_surf, self.minimap_rect)

    def display(self, player, all_sprites=None):
        """Display all UI elements for player."""
        self.show_bar(player.health, player.stats['health'], 
                     self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], 
                     self.energy_bar_rect, ENERGY_COLOR)
        self.show_coin(player.coin)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
        
        if all_sprites:
            self.show_minimap(player, all_sprites)