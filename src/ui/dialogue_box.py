"""Dialogue box UI for NPC interactions."""
import pygame
from config.settings import UI_FONT, WIDTH, HEIGHT, UI_BG_COLOR, UI_BORDER_COLOR, TEXT_COLOR


class DialogueBox:
    """Displays dialogue boxes for NPC conversations."""
    
    # Constants
    DIALOGUE_BOX_IMAGE = 'gameinfo/graphics/ui/dialogue_box.png'
    DEFAULT_FONT_SIZE = 45
    DEFAULT_TEXT_COLOR = 'white'
    
    # Box dimensions and positioning
    BOX_WIDTH = 1400
    BOX_HEIGHT = 250
    BOX_Y_OFFSET = 150
    TEXT_PADDING = 40
    
    # Button settings
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50
    BUTTON_Y_OFFSET = 80
    
    def __init__(self):
        self.display = pygame.display.get_surface()
        self._dialogue_box_image = None
        self.font_large = pygame.font.Font(UI_FONT, 45)
        self.font_medium = pygame.font.Font(UI_FONT, 35)
        self.font_small = pygame.font.Font(UI_FONT, 28)
    
    def _get_dialogue_box_image(self):
        """Lazy load dialogue box image."""
        if not self._dialogue_box_image:
            try:
                self._dialogue_box_image = pygame.image.load(self.DIALOGUE_BOX_IMAGE)
            except:
                # Create a default box if image not found
                self._dialogue_box_image = pygame.Surface((self.BOX_WIDTH, self.BOX_HEIGHT))
                self._dialogue_box_image.fill(UI_BG_COLOR)
        return self._dialogue_box_image
    
    def _draw_text_wrapped(self, text, rect, font, color):
        """Draw text with word wrapping."""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, color)
            
            if test_surface.get_width() <= rect.width - self.TEXT_PADDING * 2:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines
        y_offset = rect.top + self.TEXT_PADDING
        line_height = font.get_height()
        
        for line in lines:
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(
                centerx=rect.centerx,
                top=y_offset
            )
            self.display.blit(text_surface, text_rect)
            y_offset += line_height + 5
    
    def draw_dialogue(self, speaker, text, show_continue=True):
        """Draw complete dialogue box with speaker and text."""
        # Calculate box position
        box_x = WIDTH // 2
        box_y = HEIGHT - self.BOX_Y_OFFSET
        
        # Draw dialogue box background
        box_surface = self._get_dialogue_box_image()
        box_rect = box_surface.get_rect(center=(box_x, box_y))
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        self.display.blit(overlay, (0, 0))
        
        # Draw box
        self.display.blit(box_surface, box_rect)
        pygame.draw.rect(self.display, UI_BORDER_COLOR, box_rect, 4)
        
        # Draw speaker name
        speaker_surface = self.font_medium.render(speaker, True, 'gold')
        speaker_rect = speaker_surface.get_rect(
            centerx=box_rect.centerx,
            top=box_rect.top + 15
        )
        self.display.blit(speaker_surface, speaker_rect)
        
        # Draw dialogue text
        text_rect = pygame.Rect(
            box_rect.left + self.TEXT_PADDING,
            speaker_rect.bottom + 20,
            box_rect.width - self.TEXT_PADDING * 2,
            box_rect.height - 100
        )
        self._draw_text_wrapped(text, text_rect, self.font_small, TEXT_COLOR)
        
        # Draw continue button
        if show_continue:
            self._draw_continue_button(box_rect)
    
    def _draw_continue_button(self, box_rect):
        """Draw continue/next button."""
        button_rect = pygame.Rect(
            box_rect.right - self.BUTTON_WIDTH - 20,
            box_rect.bottom - self.BUTTON_HEIGHT - 15,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        
        # Draw button background
        pygame.draw.rect(self.display, (60, 60, 80), button_rect)
        pygame.draw.rect(self.display, 'gold', button_rect, 3)
        
        # Draw button text
        button_text = self.font_small.render("Continuar [ESPAÇO]", True, 'white')
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.display.blit(button_text, button_text_rect)
    
    def draw_interaction_prompt(self, npc_pos, text="Pressione [E] para falar"):
        """Draw interaction prompt above NPC."""
        # Create prompt surface
        prompt_surface = self.font_small.render(text, True, 'white')
        prompt_rect = prompt_surface.get_rect()
        
        # Position above NPC
        prompt_rect.centerx = npc_pos[0]
        prompt_rect.bottom = npc_pos[1] - 80
        
        # Draw background
        bg_rect = prompt_rect.inflate(20, 10)
        pygame.draw.rect(self.display, (0, 0, 0, 180), bg_rect)
        pygame.draw.rect(self.display, 'gold', bg_rect, 2)
        
        # Draw text
        self.display.blit(prompt_surface, prompt_rect)
    
    def draw_box(self, x, y):
        """Legacy method for backward compatibility."""
        box_surface = self._get_dialogue_box_image()
        icon_rect = box_surface.get_rect(center=(x, y))
        self.display.blit(box_surface, icon_rect)
    
    def draw_text(self, text, size, x, y):
        """Legacy method for backward compatibility."""
        font = pygame.font.Font(UI_FONT, size)
        text_surface = font.render(text, False, self.DEFAULT_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x, y))
        self.display.blit(text_surface, text_rect)
    
    def execute_dialogue(self, text=None, pos=(500, 500), font_size=None):
        """Legacy method for backward compatibility."""
        x, y = pos
        size = font_size or self.DEFAULT_FONT_SIZE
        text = text or 'rapaaaazzz'
        
        self.draw_box(x, y)
        self.draw_text(text, size, x, y)