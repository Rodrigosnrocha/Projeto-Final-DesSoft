"""
Nesse arquivo definimos todas as classes usadas no resto do programa
"""

import pygame
import random
from file_config import SCR_HEIGHT, SCR_WIDTH, ENEMY_CONFIG
from assets import IMG_BULLET_TEST, IMG_ENEMY_TEST, IMG_PLAYER_TEST, BG_TEST

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[IMG_PLAYER_TEST]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = 90
        self.rect.centery = SCR_HEIGHT/2
        self.speedy = 0
        self.speedx = 0   
        self.groups = groups # Salvamos todos os grupos e assets no avião para criar os tiros
        self.assets = assets
        self.anim_state = 0 # Vamos usar 0 para representar o estado 'idle'
        self.blink = False # Esse boolean determina se o avião deve piscar

        # Só será possível atirar depois do cooldown
        self.shoot_ticks = 600
        self.last_shot = pygame.time.get_ticks() - self.shoot_ticks

    def update(self):
        
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Mantem dentro da tela
        if self.rect.top < 1:
            self.rect.top = 1
        if self.rect.bottom > SCR_HEIGHT:
            self.rect.bottom = SCR_HEIGHT
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.right > SCR_WIDTH-10:
            self.rect.right = SCR_WIDTH-10
    def shoot(self):
        # Verifica se pode atirar
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde o último tiro.
        elapsed_ticks = now - self.last_shot

        # Se já pode atirar novamente...
        if elapsed_ticks > self.shoot_ticks:
            # Marca o tick da nova imagem.
            self.last_shot = now
            # A nova bala vai ser criada logo acima e no centro horizontal do aviao
            new_bullet = Bullet(self.assets, self.rect.right, self.rect.centery)
            self.groups['sprites'].add(new_bullet)
            self.groups['player_bullets'].add(new_bullet)
            #self.assets['shoot_sound'].play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, assets, config):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        self.config = config # Usa as variáveis definidas em file_config para criar as dimensões e velocidade do inimigo
        self.image = assets[IMG_ENEMY_TEST]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.width = self.config['WIDTH']
        self.height = self.config['HEIGHT']
        self.base_speed = self.config['SPEED']
        self.get_coords()
        

    def update(self):
        # Atualizando a posição do inimigo
        self.rect.x -= self.speedx

        if self.rect.right < 0:
            self.get_coords()

    def get_coords(self):
        self.rect.x = SCR_WIDTH + self.width   
        self.rect.y = random.randint(self.height, SCR_HEIGHT-self.height)
        self.speedx = self.base_speed
    
    def destroy(self):
        # Destruimos o inimigo com um método caso quisermos adicionar mais funcionalidade depois
        self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, assets, left, centery):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets[IMG_BULLET_TEST]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speedx = 30
        self.rect.left = left
        self.rect.centery = centery
        
    def update(self):
        self.rect.x += self.speedx