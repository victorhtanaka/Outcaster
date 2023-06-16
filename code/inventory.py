import pygame
from settings import *

class Inventory:
    def __init__(self,player):
        #setup geral
        self.display = pygame.display.get_surface()
        self.run_display = False
        self.display_surface = pygame.display.get_surface()
        self.player = player 
        self.attribute_nr = len(inventory_data)
        self.attribute_names = list(inventory_data.keys())
        self.values = list(inventory_data.values())
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        self.display = pygame.Surface((WIDTH,HEIGHT))

    def draw_icon(self,x,y,icon):
        icon_surface = pygame.image.load(icon)
        icon_rect = icon_surface.get_rect()
        icon_rect.center = (x,y)
        self.display.blit(icon_surface, icon_rect)
    
    def blit_screen(self):
        self.display.blit(self.display, (0, 0))
        pygame.display.update()
        
    def display_inventory(self):
        self.run_display = True
        while self.run_display:
            self.display.fill('black')
            #self.game.check_events()
            #self.check_input()
            self.iconx = 500
            self.icony = 500
            for item_icon in inventory_data.values():
                self.draw_icon(self.iconx,self.icony,"gameinfo/graphics/items/uva (1).png")
                self.iconx += 50
                if self.iconx >= 1000:
                    self.iconx -= 500
                    self.icony += 100
            # Criar background do inventario
            # Criar exibição de itens
            # Criar cursor que quando voce move para os lados ele troca o item(numero fixo de 12 itens no inventario em formato de matriz)
            # Criar exibição de descriçao de item
            self.blit_screen()

class Map:
    pass