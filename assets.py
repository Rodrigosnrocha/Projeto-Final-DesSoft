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
    return assets