"""Inventory UI for displaying and interacting with player inventory."""
import pygame
from config.settings import *
from config.game_data import ITEM_DATA, ITEM_TYPES
from typing import Optional


class InventoryUI:
    """Visual interface for the inventory system."""
    
    # Layout constants
    SLOTS_PER_ROW = 5
    SLOTS_PER_COL = 4
    SLOT_SIZE = 100
    SLOT_PADDING = 10
    
    # Colors
    SLOT_BG_COLOR = (40, 40, 50)
    SLOT_BORDER_COLOR = (80, 80, 100)
    SLOT_SELECTED_COLOR = (200, 180, 50)
    OVERLAY_COLOR = (0, 0, 0)
    OVERLAY_ALPHA = 180
    
    # Preview panel
    PREVIEW_WIDTH = 500
    PREVIEW_PADDING = 30
    PREVIEW_IMAGE_SIZE = 200
    
    def __init__(self, inventory_system):
        self.display = pygame.display.get_surface()
        self.inventory = inventory_system
        
        # Fonts
        self.font_title = pygame.font.Font(UI_FONT, 48)
        self.font_large = pygame.font.Font(UI_FONT, 36)
        self.font_medium = pygame.font.Font(UI_FONT, 28)
        self.font_small = pygame.font.Font(UI_FONT, 20)
        
        # Calculate positions
        self._calculate_layout()
        
        # Image cache
        self._image_cache = {}
    
    def _calculate_layout(self):
        """Calculate UI layout positions."""
        # Grid dimensions
        grid_width = (self.SLOT_SIZE + self.SLOT_PADDING) * self.SLOTS_PER_ROW
        grid_height = (self.SLOT_SIZE + self.SLOT_PADDING) * self.SLOTS_PER_COL
        
        # Center the grid
        self.grid_start_x = (WIDTH - grid_width - self.PREVIEW_WIDTH) // 2
        self.grid_start_y = (HEIGHT - grid_height) // 2
        
        # Preview panel position (right side)
        self.preview_x = self.grid_start_x + grid_width + 50
        self.preview_y = self.grid_start_y
    
    def _get_slot_position(self, slot_index: int) -> tuple:
        """Get screen position for slot."""
        row = slot_index // self.SLOTS_PER_ROW
        col = slot_index % self.SLOTS_PER_ROW
        
        x = self.grid_start_x + col * (self.SLOT_SIZE + self.SLOT_PADDING)
        y = self.grid_start_y + row * (self.SLOT_SIZE + self.SLOT_PADDING)
        
        return (x, y)
    
    def _load_item_image(self, icon_path: str) -> pygame.Surface:
        """Load and cache item image."""
        if icon_path not in self._image_cache:
            try:
                image = pygame.image.load(icon_path).convert_alpha()
                # Scale to fit slot
                image = pygame.transform.scale(image, (self.SLOT_SIZE - 20, self.SLOT_SIZE - 20))
                self._image_cache[icon_path] = image
            except:
                # Create placeholder if image not found
                image = pygame.Surface((self.SLOT_SIZE - 20, self.SLOT_SIZE - 20))
                image.fill((100, 100, 100))
                self._image_cache[icon_path] = image
        
        return self._image_cache[icon_path]
    
    def _draw_slot(self, slot_index: int, is_selected: bool = False):
        """Draw a single inventory slot."""
        x, y = self._get_slot_position(slot_index)
        slot = self.inventory.get_slot(slot_index)
        
        # Draw slot background
        slot_rect = pygame.Rect(x, y, self.SLOT_SIZE, self.SLOT_SIZE)
        pygame.draw.rect(self.display, self.SLOT_BG_COLOR, slot_rect)
        
        # Draw border
        border_color = self.SLOT_SELECTED_COLOR if is_selected else self.SLOT_BORDER_COLOR
        border_width = 4 if is_selected else 2
        pygame.draw.rect(self.display, border_color, slot_rect, border_width)
        
        # Draw item if slot has one
        if not slot.is_empty():
            item_data = slot.get_item_data()
            icon_path = item_data.get('icon', '')
            
            # Draw item icon
            if icon_path:
                item_image = self._load_item_image(icon_path)
                image_rect = item_image.get_rect(center=slot_rect.center)
                self.display.blit(item_image, image_rect)
            
            # Draw quantity if stackable
            if slot.quantity > 1:
                quantity_text = self.font_small.render(str(slot.quantity), True, 'white')
                quantity_rect = quantity_text.get_rect(
                    bottomright=(slot_rect.right - 5, slot_rect.bottom - 5)
                )
                # Draw shadow
                shadow_rect = quantity_rect.copy()
                shadow_rect.x += 2
                shadow_rect.y += 2
                shadow_text = self.font_small.render(str(slot.quantity), True, 'black')
                self.display.blit(shadow_text, shadow_rect)
                self.display.blit(quantity_text, quantity_rect)
    
    def _draw_preview_panel(self):
        """Draw item preview panel on the right."""
        selected_slot = self.inventory.get_selected_slot()
        
        # Panel background
        panel_rect = pygame.Rect(
            self.preview_x,
            self.preview_y,
            self.PREVIEW_WIDTH,
            (self.SLOT_SIZE + self.SLOT_PADDING) * self.SLOTS_PER_COL
        )
        pygame.draw.rect(self.display, (30, 30, 40), panel_rect)
        pygame.draw.rect(self.display, self.SLOT_BORDER_COLOR, panel_rect, 3)
        
        if selected_slot.is_empty():
            # Show "Empty Slot" message
            empty_text = self.font_medium.render("Slot Vazio", True, (120, 120, 120))
            empty_rect = empty_text.get_rect(center=panel_rect.center)
            self.display.blit(empty_text, empty_rect)
            return
        
        # Get item data
        item_data = selected_slot.get_item_data()
        item_name = item_data.get('name', 'Unknown')
        item_type = item_data.get('type', 'normal')
        item_desc = item_data.get('description', 'No description')
        icon_path = item_data.get('icon', '')
        
        y_offset = panel_rect.top + self.PREVIEW_PADDING
        
        # Draw large item image
        if icon_path:
            try:
                large_image = pygame.image.load(icon_path).convert_alpha()
                large_image = pygame.transform.scale(
                    large_image, 
                    (self.PREVIEW_IMAGE_SIZE, self.PREVIEW_IMAGE_SIZE)
                )
                image_rect = large_image.get_rect(
                    centerx=panel_rect.centerx,
                    top=y_offset
                )
                self.display.blit(large_image, image_rect)
                y_offset = image_rect.bottom + 20
            except:
                y_offset += self.PREVIEW_IMAGE_SIZE + 20
        
        # Draw item name
        name_text = self.font_large.render(item_name, True, 'gold')
        name_rect = name_text.get_rect(
            centerx=panel_rect.centerx,
            top=y_offset
        )
        self.display.blit(name_text, name_rect)
        y_offset = name_rect.bottom + 10
        
        # Draw item type with color coding
        type_colors = {
            'weapon': (255, 100, 100),
            'spell': (100, 100, 255),
            'tool': (255, 200, 100),
            'normal': (150, 150, 150)
        }
        type_names = {
            'weapon': 'Arma',
            'spell': 'Feitiço',
            'tool': 'Ferramenta',
            'normal': 'Item'
        }
        
        type_color = type_colors.get(item_type, (150, 150, 150))
        type_name = type_names.get(item_type, 'Item')
        type_text = self.font_small.render(f"[{type_name}]", True, type_color)
        type_rect = type_text.get_rect(
            centerx=panel_rect.centerx,
            top=y_offset
        )
        self.display.blit(type_text, type_rect)
        y_offset = type_rect.bottom + 20
        
        # Draw quantity if stackable
        if selected_slot.quantity > 1:
            qty_text = self.font_medium.render(
                f"Quantidade: {selected_slot.quantity}", 
                True, 
                'white'
            )
            qty_rect = qty_text.get_rect(
                centerx=panel_rect.centerx,
                top=y_offset
            )
            self.display.blit(qty_text, qty_rect)
            y_offset = qty_rect.bottom + 15
        
        # Draw description (word wrapped)
        self._draw_wrapped_text(
            item_desc,
            panel_rect.left + self.PREVIEW_PADDING,
            y_offset,
            panel_rect.width - self.PREVIEW_PADDING * 2,
            self.font_small,
            TEXT_COLOR
        )
        
        # Draw item stats at bottom
        y_offset = panel_rect.bottom - 100
        
        if item_type == 'weapon':
            damage = item_data.get('damage', 0)
            stat_text = self.font_small.render(f"Dano: {damage}", True, (255, 100, 100))
            stat_rect = stat_text.get_rect(
                centerx=panel_rect.centerx,
                top=y_offset
            )
            self.display.blit(stat_text, stat_rect)
        
        elif item_type == 'spell':
            mana = item_data.get('mana_cost', 0)
            stat_text = self.font_small.render(f"Custo de Mana: {mana}", True, (100, 100, 255))
            stat_rect = stat_text.get_rect(
                centerx=panel_rect.centerx,
                top=y_offset
            )
            self.display.blit(stat_text, stat_rect)
        
        elif 'heal_amount' in item_data:
            heal = item_data.get('heal_amount', 0)
            stat_text = self.font_small.render(f"Cura: +{heal} HP", True, (100, 255, 100))
            stat_rect = stat_text.get_rect(
                centerx=panel_rect.centerx,
                top=y_offset
            )
            self.display.blit(stat_text, stat_rect)
        
        elif 'mana_amount' in item_data:
            mana = item_data.get('mana_amount', 0)
            stat_text = self.font_small.render(f"Mana: +{mana} MP", True, (100, 150, 255))
            stat_rect = stat_text.get_rect(
                centerx=panel_rect.centerx,
                top=y_offset
            )
            self.display.blit(stat_text, stat_rect)
    
    def _draw_wrapped_text(self, text: str, x: int, y: int, max_width: int, 
                          font: pygame.font.Font, color: tuple):
        """Draw text with word wrapping."""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, color)
            
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines
        line_height = font.get_height()
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            self.display.blit(text_surface, (x, y + i * (line_height + 5)))
    
    def draw(self):
        """Draw the complete inventory UI."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(self.OVERLAY_ALPHA)
        overlay.fill(self.OVERLAY_COLOR)
        self.display.blit(overlay, (0, 0))
        
        # Draw title
        title_text = self.font_title.render("INVENTÁRIO", True, 'gold')
        title_rect = title_text.get_rect(
            centerx=WIDTH // 2,
            top=50
        )
        self.display.blit(title_text, title_rect)
        
        # Draw all slots
        for i in range(self.inventory.MAX_SLOTS):
            is_selected = (i == self.inventory.selected_index)
            self._draw_slot(i, is_selected)
        
        # Draw preview panel
        self._draw_preview_panel()
        
        # Draw controls help
        self._draw_controls()
    
    def _draw_controls(self):
        """Draw control instructions at bottom."""
        controls = [
            "Setas: Navegar",
            "ENTER: Usar Item",
            "I/ESC: Fechar"
        ]
        
        y_pos = HEIGHT - 80
        x_start = WIDTH // 2 - 300
        
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, (200, 200, 200))
            rect = text.get_rect(left=x_start + i * 250, centery=y_pos)
            self.display.blit(text, rect)
    
    def handle_input(self, keys, key_pressed: Optional[int] = None) -> Optional[str]:
        """
        Handle keyboard input for inventory navigation.
        
        Args:
            keys: Current key states
            key_pressed: Single key that was just pressed
            
        Returns:
            Action string: 'close', 'use_item', or None
        """
        if key_pressed:
            # Navigation (no debounce for responsiveness)
            if key_pressed == pygame.K_UP:
                self.inventory.move_selection('up')
            elif key_pressed == pygame.K_DOWN:
                self.inventory.move_selection('down')
            elif key_pressed == pygame.K_LEFT:
                self.inventory.move_selection('left')
            elif key_pressed == pygame.K_RIGHT:
                self.inventory.move_selection('right')
            
            # Actions
            elif key_pressed == pygame.K_RETURN:
                return 'use_item'
            elif key_pressed == pygame.K_i:
                return 'close'
            # ESC is handled globally in Level.run()
        
        return None
