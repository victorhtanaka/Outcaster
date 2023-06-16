import pygame
from settings import *
from support import *

class NPC1(pygame.sprite.Sprite):
    npc_rect = None
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("gameinfo/graphics/NPC's/NPC_editado.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.npc_rect = self.rect
        NPC1.npc_rect = self.rect

        # hitbox 
        self.hitbox = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        self.hitbox.topleft = self.rect.topleft

    def update(self):
        self.hitbox.topleft = self.rect.topleft
