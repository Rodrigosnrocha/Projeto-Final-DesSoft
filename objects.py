"""
Nesse arquivo definimos todas as classes usadas no resto do programa
"""

import pygame
import random
from file_config import SCR_HEIGHT, SCR_WIDTH, ENEMY_CONFIG
from assets import IMG_BULLET_TEST, IMG_ENEMY_TEST, IMG_PLAYER_TEST, BG_TEST

class Player(pygame.sprite.Sprite):
    """ Classe que define o personagem do jogador
    Atributos
    ---------
    rect : pygame.rect
        Retângulo das coordenadas do sprite
    speedx/speedy : int
        Velocidade no eixo x ou y
    mask : pygame.mask
        Máscara de colisão
    blink : bool
        Determina se o sprite deverá piscar ou não
    blink_timer : int
        Timer que marca quanto tempo o jogador pisca
    shoot_ticks : int
        Quantos ticks se passaram desde o último tiro
    last_shot : int
        Último tick em que atirou
    
    Métodos
    -------
    update()
        Atualiza sua posição na tela com base no input do jogador
    shoot()
        Cria uma entidade Bullet
    """

    def __init__(self, groups, assets,save_data):
        """
        Parâmetros
        ----------
        groups : dic
            Todos os sprite groups usados no jogo
            OBS: Incluir chaves 'sprites' e 'player_bullets'
        assets : dic
            Todos os assets usados no jogo
            OBS: Incluir chaves 'IMG_PLAYER_TEST', 'IMG_BULLET_TEST' e 'blink'
        save_data : dic
            Parâmetros de velocidade de tiros
        """
        pygame.sprite.Sprite.__init__(self)

        # Define a imagem do sprite, suas coordenadas, e a máscara de colisão
        self.image = assets[IMG_PLAYER_TEST]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = 90
        self.rect.centery = SCR_HEIGHT/2

        # Define a velocidade do jogador nos eixos x e y
        # Inicialmente 0 até apertar as teclas de direção
        self.speedy = 0
        self.speedx = 0

        # Salvamos todos os grupos e assets no avião para criar os tiros
        self.groups = groups 
        self.assets = assets
        self.blink = False # Esse boolean determina se o avião deve piscar
        self.blink_timer = 0 # Essa variavel conta quanto tempo se passou no estado de piscar

        # Só será possível atirar depois do cooldown
        self.shoot_ticks = 1000 - (100 * save_data['shoot_speed'])
        self.last_shot = pygame.time.get_ticks() - self.shoot_ticks
    def update(self):
        """Atualiza sua posição na tela com base no input do jogador"""
        
        # Muda sua posição com base na velocidade nos eixos
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
        
        # Pisca se tiver colidido com um inimigo nos ultimos 100 ticks
        if self.blink == True:
            if self.blink_timer >= 100:
                self.image = self.assets[IMG_PLAYER_TEST]
                self.blink = False
            elif self.blink_timer%7 == 0:
                if self.image == self.assets[IMG_PLAYER_TEST]:
                    self.image = self.assets['blink']
                else:
                    self.image = self.assets[IMG_PLAYER_TEST]
    def shoot(self):
        """Cria uma entidade Bullet"""
        
        # Verifica quanto tempo decorreu desde o último tiro
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_shot

        # Se for maior que o timer de tiro, cria uma bala
        if elapsed_ticks > self.shoot_ticks:
            self.last_shot = now # Marca o tick da nova imagem.

            # A nova bala vai ser criada logo à frente e no centro vertical do avião
            new_bullet = Bullet(self.assets, self.rect.right, self.rect.centery)
            self.groups['sprites'].add(new_bullet)
            self.groups['player_bullets'].add(new_bullet)

            shoot_sound = self.assets['shoot_sound']
            shoot_sound.set_volume(0.2)            
            pygame.mixer.Sound.play(shoot_sound)


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
        max_y = self.height*2
        min_y = SCR_HEIGHT-self.height*2
        self.rect.y = random.randint(max_y, min_y)
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
        if self.rect.left > SCR_WIDTH:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self, assets, centery, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets['nuvem']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speedx = -speed
        self.rect.left = SCR_WIDTH
        self.rect.centery = centery
        
    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()