"""
Nesse arquivo definimos todas as classes usadas no resto do programa
"""

import pygame
import random
from file_config import SCR_HEIGHT, SCR_WIDTH
from assets import IMG_BULLET_TEST, IMG_PLAYER_TEST, BG_TEST

class Player(pygame.sprite.Sprite):
    def __init__(self,groups,assets):
        pygame.sprite.Sprite.__init__(self)
        self.groups = groups
        self.assets = assets

        self.image = assets[IMG_PLAYER_TEST]
        self.mask = pygame.mask.from_surface(self.image)

        self.speedx = 0
        self.speedy = 0

        self.rect = self.image.get_rect()
        self.rect.centery = SCR_HEIGHT / 2
        self.rect.left = 10