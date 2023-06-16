import pygame
from settings import *
from support import *

class NPC1(pygame.sprite.Sprite):
    npc_rect = None
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("gameinfo/graphics/NPC's/NPC_editado.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(10,10)
        self.npc_rect = self.rect

        # hitbox 
        self.hitbox.topleft = self.rect.topleft

    def update(self):
        self.hitbox.topleft = self.rect.topleft