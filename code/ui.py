import pygame
from settings import *

class UI:
    def __init__(self):

        #geral
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT_THIN,UI_FONT_SIZE_THIN)

        #SETUP DA BARRA DE COISAS
        self.health_bar_rect = pygame.Rect(300,180,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(300,204,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        # convert weapon dictionary
		#self.weapon_graphics = []
		#for weapon in weapon_data.values():
		#	path = weapon['graphic']
		#	weapon = pygame.image.load(path).convert_alpha()
		#	self.weapon_graphics.append(weapon)

        # Converter dicionario de magica
        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)
        
    def show_bar(self,current,max_amount,bg_rect,color):
        #draw background
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

        #converter statistica para pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        #draw the bar
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

    def show_coin(self,coin):
        text_surf = self.font.render(str(int(coin)),False,TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(center = (1590,880))

        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

    def selection_box(self,left,top, has_switched):
        bg_rect = pygame.Rect(300,825,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect

    def magic_overlay(self,magic_index,has_switched):
        bg_rect = self.selection_box(80,635,has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(magic_surf,magic_rect)

    def display(self,player):
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)

        self.show_coin(player.coin)

        self.magic_overlay(player.magic_index,not player.can_switch_magic)