"""Optimized camera and rendering system."""
import pygame
from typing import List, Tuple


class Camera:
    """Optimized camera with culling."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.offset = pygame.math.Vector2()
        self.half_width = width // 2
        self.half_height = height // 2
        self.smooth_speed = 0.1
        
        # Shake
        self.shake_amount = 0
        self.shake_duration = 0

    def shake(self, intensity=5, duration=10):
        self.shake_amount = intensity
        self.shake_duration = duration

    def center_on(self, target_rect: pygame.Rect):
        """Center camera on a target with smoothing and shake."""
        target_x = target_rect.centerx - self.half_width
        target_y = target_rect.centery - self.half_height
        
        self.offset.x += (target_x - self.offset.x) * self.smooth_speed
        self.offset.y += (target_y - self.offset.y) * self.smooth_speed
        
        if self.shake_duration > 0:
            self.shake_duration -= 1
            import random
            x_offset = random.randint(-self.shake_amount, self.shake_amount)
            y_offset = random.randint(-self.shake_amount, self.shake_amount)
            self.offset.x += x_offset
            self.offset.y += y_offset
    
    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        """Apply camera offset to a rect."""
        return rect.move(-self.offset.x, -self.offset.y)
    
    def is_visible(self, rect: pygame.Rect, margin: int = 100) -> bool:
        """Check if a rect is visible in camera view."""
        return (rect.right + margin > self.offset.x and
                rect.left - margin < self.offset.x + self.width and
                rect.bottom + margin > self.offset.y and
                rect.top - margin < self.offset.y + self.height)


class YSortCameraGroup(pygame.sprite.Group):
    """Optimized Y-sort camera group with culling."""
    
    def __init__(self, floor_image_path: str = None):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.camera = Camera(
            self.display_surface.get_width(),
            self.display_surface.get_height()
        )
        
        # Floor
        self.floor_surf = None
        self.floor_rect = None
        if floor_image_path:
            try:
                self.floor_surf = pygame.image.load(floor_image_path).convert()
                self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
            except pygame.error as e:
                print(f"Error loading floor: {e}")
    
    def custom_draw(self, player):
        """Draw sprites with Y-sorting and culling."""
        # Center camera on player
        self.camera.center_on(player.rect)
        
        # Draw floor if exists
        if self.floor_surf and self.floor_rect:
            floor_offset_pos = self.floor_rect.topleft - self.camera.offset
            self.display_surface.blit(self.floor_surf, floor_offset_pos)
        
        # Get visible sprites and sort by Y position
        visible_sprites = [
            sprite for sprite in self.sprites()
            if self.camera.is_visible(sprite.rect)
        ]
        
        sorted_sprites = sorted(visible_sprites, key=lambda s: s.rect.centery)
        
        # Draw sprites
        for sprite in sorted_sprites:
            offset_pos = sprite.rect.topleft - self.camera.offset
            self.display_surface.blit(sprite.image, offset_pos)
    
    def enemy_update(self, player):
        """Update enemies that see the player."""
        for sprite in self.sprites():
            if (hasattr(sprite, 'sprite_type') and 
                sprite.sprite_type == 'enemy' and
                hasattr(sprite, 'enemy_update')):
                sprite.enemy_update(player)


class SpatialHash:
    """Spatial hash for efficient collision detection."""
    
    def __init__(self, cell_size: int = 128):
        self.cell_size = cell_size
        self.cells = {}
    
    def _get_cell(self, x: int, y: int) -> Tuple[int, int]:
        """Get cell coordinates for a position."""
        return (x // self.cell_size, y // self.cell_size)
    
    def _get_cells_for_rect(self, rect: pygame.Rect) -> List[Tuple[int, int]]:
        """Get all cells that a rect occupies."""
        cells = []
        min_cell = self._get_cell(rect.left, rect.top)
        max_cell = self._get_cell(rect.right, rect.bottom)
        
        for x in range(min_cell[0], max_cell[0] + 1):
            for y in range(min_cell[1], max_cell[1] + 1):
                cells.append((x, y))
        
        return cells
    
    def insert(self, sprite):
        """Insert a sprite into the hash."""
        if not hasattr(sprite, 'rect'):
            return
        
        cells = self._get_cells_for_rect(sprite.rect)
        for cell in cells:
            if cell not in self.cells:
                self.cells[cell] = []
            if sprite not in self.cells[cell]:
                self.cells[cell].append(sprite)
    
    def query(self, rect: pygame.Rect) -> set:
        """Query sprites near a rect."""
        cells = self._get_cells_for_rect(rect)
        nearby = set()
        
        for cell in cells:
            if cell in self.cells:
                nearby.update(self.cells[cell])
        
        return nearby
    
    def clear(self):
        """Clear the hash."""
        self.cells.clear()
    
    def rebuild(self, sprites):
        """Rebuild hash with new sprite positions."""
        self.clear()
        for sprite in sprites:
            self.insert(sprite)
