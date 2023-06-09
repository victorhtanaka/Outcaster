from typing import Any
import pygame
from settings import *
from support import *
from entity import Entity
import math

class NPC1(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("gameinfo/graphics/NPC's/NPC_editado.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        # hitbox 
        self.hitbox = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        self.hitbox.topleft = self.rect.topleft

        # interação 
        self.interactable = False

    def update(self):
        self.hitbox.topleft = self.rect.topleft