"""UI components."""
import pygame
from abc import ABC, abstractmethod
from typing import Optional, Callable, Tuple


class UIComponent(ABC):
    """Base UI component."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True
    
    @abstractmethod
    def render(self, surface: pygame.Surface):
        """Render the component."""
        pass
    
    def handle_event(self, event: pygame.event.Event):
        """Handle input event."""
        pass
    
    def update(self, dt: float = 0):
        """Update component."""
        pass


class Panel(UIComponent):
    """Panel component for grouping UI elements."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 bg_color: Tuple[int, int, int] = (34, 34, 34),
                 border_color: Optional[Tuple[int, int, int]] = (17, 17, 17),
                 border_width: int = 3):
        super().__init__(x, y, width, height)
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
    
    def render(self, surface: pygame.Surface):
        """Render panel."""
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw border
        if self.border_color:
            pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)


class Bar(UIComponent):
    """Progress bar component."""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 fg_color: Tuple[int, int, int] = (255, 0, 0),
                 bg_color: Tuple[int, int, int] = (34, 34, 34),
                 border_color: Tuple[int, int, int] = (17, 17, 17),
                 border_width: int = 3):
        super().__init__(x, y, width, height)
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.current = 100
        self.maximum = 100
    
    def set_value(self, current: float, maximum: float):
        """Set bar value."""
        self.current = max(0, current)
        self.maximum = max(1, maximum)
    
    def render(self, surface: pygame.Surface):
        """Render bar."""
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw foreground based on ratio
        ratio = self.current / self.maximum
        fg_width = int(self.rect.width * ratio)
        fg_rect = self.rect.copy()
        fg_rect.width = fg_width
        pygame.draw.rect(surface, self.fg_color, fg_rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)


class Text(UIComponent):
    """Text component."""
    
    def __init__(self, x: int, y: int, text: str,
                 font: Optional[pygame.font.Font] = None,
                 color: Tuple[int, int, int] = (238, 238, 238),
                 center: bool = True):
        self.text = text
        self.font = font or pygame.font.Font(None, 32)
        self.color = color
        self.center = center
        
        # Calculate size
        self.surface = self.font.render(text, True, color)
        width, height = self.surface.get_size()
        super().__init__(x, y, width, height)
        
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
    
    def set_text(self, text: str):
        """Update text."""
        self.text = text
        self.surface = self.font.render(text, True, self.color)
        old_center = self.rect.center if self.center else self.rect.topleft
        self.rect = self.surface.get_rect()
        if self.center:
            self.rect.center = old_center
        else:
            self.rect.topleft = old_center
    
    def render(self, surface: pygame.Surface):
        """Render text."""
        if not self.visible:
            return
        surface.blit(self.surface, self.rect)


class Button(UIComponent):
    """Button component."""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str,
                 callback: Optional[Callable] = None,
                 font: Optional[pygame.font.Font] = None,
                 text_color: Tuple[int, int, int] = (238, 238, 238),
                 bg_color: Tuple[int, int, int] = (34, 34, 34),
                 hover_color: Tuple[int, int, int] = (60, 60, 60),
                 border_color: Tuple[int, int, int] = (17, 17, 17)):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = font or pygame.font.Font(None, 32)
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.hovered = False
        
        # Render text
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle button events."""
        if not self.enabled:
            return
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                if self.callback:
                    self.callback()
    
    def render(self, surface: pygame.Surface):
        """Render button."""
        if not self.visible:
            return
        
        # Draw background
        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, 3)
        
        # Draw text
        surface.blit(self.text_surface, self.text_rect)


class Image(UIComponent):
    """Image component."""
    
    def __init__(self, x: int, y: int, image: pygame.Surface, center: bool = True):
        self.image = image
        width, height = image.get_size()
        super().__init__(x, y, width, height)
        
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
    
    def set_image(self, image: pygame.Surface):
        """Update image."""
        self.image = image
        old_center = self.rect.center
        self.rect = image.get_rect(center=old_center)
    
    def render(self, surface: pygame.Surface):
        """Render image."""
        if not self.visible:
            return
        surface.blit(self.image, self.rect)
