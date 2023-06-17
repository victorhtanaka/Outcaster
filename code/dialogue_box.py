import pygame
from settings import *

class DialogueBox:
    def __init__(self):
        self.display = pygame.display.get_surface()
        
    def draw_box(self,x,y):
        icon_surface = pygame.image.load('gameinfo/graphics/ui/dialogue_box.png')
        icon_rect = icon_surface.get_rect()
        icon_rect.center = (x,y)
        self.display.blit(icon_surface, icon_rect)
    
    def draw_text(self, text,size, x, y ):
        font = pygame.font.Font(UI_FONT,size)
        text_surface = font.render(text, False, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    
    def execute_dialogue(self):
        self.draw_box(500,500)
        self.draw_text('rapaaaazzz',45,(500,500))