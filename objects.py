"""
Nesse arquivo definimos todas as classes usadas no resto do programa
"""

from Pystuff.Jogobackup import HEIGHT
import pygame
import random
from file_config import SCR_HEIGHT, SCR_WIDTH
from assets import IMG_BULLET_TEST, IMG_PLAYER_TEST, BG_TEST

''' o que ja tava aqui \/
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
'''

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        # Construtor da classe mãe (Sprite).

        pygame.sprite.Sprite.__init__(self)

        self.image = assets[[IMG_PLAYER_TEST]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = 90
        self.rect.centery = SCR_HEIGHT/2
        self.speedy = 0
        self.groups = groups
        self.assets = assets

        # Só será possível atirar depois do cooldown (depende da arma)
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 1000

    def update(self):
        # Atualização da posição do boomerang
        self.rect.y += self.speedy

        # Mantem dentro da tela
        if self.rect.top > HEIGHT:
            self.rect.top = HEIGHT
            self.speedy = 0
        if self.rect.bottom < 0:
            self.rect.bottom = 0
            self.speedy = 0

    def shoot(self):
        # Verifica se pode atirar
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde o último tiro.
        elapsed_ticks = now - self.last_shot

        # Se já pode atirar novamente...
        if elapsed_ticks > self.shoot_ticks:
            # Marca o tick da nova imagem.
            self.last_shot = now
            # A nova bala vai ser criada logo acima e no centro horizontal da nave
            new_bullet = Bullet(self.assets, self.rect.right, self.rect.centery)
            self.groups['all_sprites'].add(new_bullet)
            self.groups['all_bullets'].add(new_bullet)
            self.assets['shoot_sound'].play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['enemy_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + ENEMY_WIDTH   
        self.rect.y = random.randint(ENEMY_HEIGHT+10, HEIGHT-ENEMY_HEIGHT)
        self.speedx = ENEMY_SPEED

    def update(self):
        # Atualizando a posição do inimigo
        self.rect.x += self.speedx

        # Se o inimigo passar do final da tela, volta para cima e
        # sorteia novas posições
        if self.rect.right < 0:
            self.rect.x = WIDTH + ENEMY_WIDTH   
            self.rect.y = random.randint(ENEMY_HEIGHT+10, HEIGHT-ENEMY_HEIGHT)
            self.speedx = ENEMY_SPEED