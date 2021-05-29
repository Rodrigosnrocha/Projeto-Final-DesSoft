import pygame
from os import path
from file_config import IMG, SND, TXT

# Nomes para as chaves do dicionário
# IMPORTANTE: Lembre-se de importar as chaves para os arquivos onde são necessários
IMG_TEST = 'IMG_TEST'
IMG_PLAYER_TEST = 'IMG_PLAYER_TEST'
BG_TEST = 'BG_TEST'
IMG_BULLET_TEST = 'IMG_BULLET_TEST'
IMG_ENEMY_TEST = 'IMG_ENEMY_TEST'
FONT = 'FONT'

# Glossário dos assets BG = background; IMG = imagens/sprites, SND = musica/sons; TXT = texto/fonts

def load_assets():
    """
    Carrega todos os assets do jogo e retorna como um dicionário,
    para que possam ser usados em outros arquivos,
    sem precisar importá-los um a um
    """

    # Coloque todos os assets nesse dicionário para facilitar seu uso depois
    assets = {}
    assets[IMG_TEST] = pygame.image.load(path.join(IMG,'img_test.png')).convert()
    assets[BG_TEST] = pygame.image.load(path.join(IMG,'bg_test.png')).convert()
    assets[IMG_PLAYER_TEST] = pygame.image.load(path.join(IMG,'img_playerTest.png')).convert_alpha()
    assets[IMG_BULLET_TEST] = pygame.image.load(path.join(IMG,'img_bulletTest.png')).convert_alpha()
    assets[IMG_ENEMY_TEST] = pygame.image.load(path.join(IMG,'img_bulletTest.png')).convert_alpha()
    assets[FONT] = pygame.font.Font(None,28)
    assets['FONT2'] = pygame.font.Font(None,36)
    assets['FONT3'] = pygame.font.Font(None,48)
    assets['FONT4'] = pygame.font.Font(None,70)
    coin_anim = []
    for i in range(6):
        filename = 'Coin{}.png'.format(i+1)
        img = pygame.image.load(path.join(IMG,filename)).convert_alpha()
        img = pygame.transform.scale(img, (32, 32))
        coin_anim.append(img)
    assets["coin_anim"] = coin_anim
    heart_anim = []
    for i in range(4):
        filename = 'HeartT{}.png'.format(i)
        img = pygame.image.load(path.join(IMG,filename)).convert_alpha()
        heart_anim.append(img)
    assets["heart_anim"] = heart_anim
    return assets