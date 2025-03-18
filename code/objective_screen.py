import pygame
from settings import *
from time import sleep

class ObjectiveScreen():
    def __init__(self):
        self.display = pygame.display.get_surface()

        self.mid_w, self.mid_h = WIDTH / 2, HEIGHT / 2

    def blit_screen(self):
        pygame.display.update()

    def draw_text(self, text,size, x, y ):
        font = pygame.font.Font(UI_FONT,size)
        text_surface = font.render(text, True, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def draw_background(self,image):
        self.display.blit(pygame.image.load(image), [0,0])

class ObjectiveScreenOp(ObjectiveScreen):
    def __init__(self):
        ObjectiveScreen.__init__(self)
        self.startx, self.starty = self.mid_w, self.mid_h - 80
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 80

    def display_objective(self):
        self.draw_background('gameinfo/graphics/ui/escape.png')
        self.draw_text("Objetivo", 70, self.startx, self.starty)
        self.draw_text("Mate todos os inimigos", 50, self.optionsx, self.optionsy)
        pygame.display.update()
        sleep(4)