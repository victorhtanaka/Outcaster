from typing import Any
import pygame
from settings import *
from support import *
from entity import Entity
import math

class NPC(pygame.sprite.Sprite):
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

    def check_interaction(self, player_rect):
        distance = self.rect.distance_to(player_rect)
        if distance < INTERACTION_DISTANCE:
            self.interactable = True
            print('Hello World!')
        
    def distance_to(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance