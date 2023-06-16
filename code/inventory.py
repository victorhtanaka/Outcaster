import pygame
from settings import *

class Inventory:
    def __init__(self,player):
        #setup geral
        self.display_surface = pygame.display.get_surface()
        self.player = player 
        self.attribute_nr = len(self.player.inventory_data)
        self.attribute_names = list(self.player.inventory_data.keys())
        self.values = list(self.player.inventory_data.values())
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        # Criação de itens
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        # Sistema de seleção
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            #if keys[pygame.K_SPACE]:
            #    self.can_move = False
            #    self.selection_time = pygame.time.get_ticks()
            #    self.item_list[self.selection_index].trigger(self.player)
    
    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            # Posição Horizontal
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2
            
            # Posição vertical
            top = self.display_surface.get_size()[1] * 0.1

            # Criar objeto
            item = Item(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index,item in enumerate(self.item_list):

            # Pegar Atributos
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            item.display(self.display_surface,self.selection_index,name,value)

class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font

    def display_names(self,surface,name,selected):
        color = 'white' if selected else TEXT_COLOR

		# title
        title_surf = self.font.render(name,False,color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

		# draw 
        surface.blit(title_surf,title_rect)

    def display_bar(self,surface,value,max_value,selected):

		# drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

		# bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15,bottom[1] - relative_number,30,10)

		# draw elements
        pygame.draw.line(surface,color,top,bottom,5)
        pygame.draw.rect(surface,color,value_rect)

    def display(self,surface,selection_num,name,value):
        if self.index == selection_num:
            pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
        else:
            pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
	
        self.display_names(surface,name,self.index == selection_num)
        self.display_bar(surface,value,self.index == selection_num)