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
    # Adiciona a imagem do avião do jogador:
    assets[IMG_PLAYER_TEST] = pygame.image.load(path.join(IMG,'aviao2.png')).convert_alpha()
    # Define o tamanho do avião do jogador:
    assets[IMG_PLAYER_TEST] = pygame.transform.scale(assets[IMG_PLAYER_TEST], (194, 110))
    # Adiciona a imagem do "tiro":
    assets[IMG_BULLET_TEST] = pygame.image.load(path.join(IMG,'bullet.png')).convert_alpha()
    # Define o tamanho do "tiro":
    assets[IMG_BULLET_TEST] = pygame.transform.scale(assets[IMG_BULLET_TEST], (40, 12))
    # Adiciona a imagem do avião inimigo:
    assets[IMG_ENEMY_TEST] = pygame.image.load(path.join(IMG,'aviao3.png')).convert_alpha()
    # Define o tamanho do avião inimigo:
    assets[IMG_ENEMY_TEST] = pygame.transform.scale(assets[IMG_ENEMY_TEST], (118, 42))
    # Adiciona uma imagem transparente para a "animação" de "piscar" o avião:
    assets['blink'] = pygame.image.load(path.join(IMG,'img_blink.png')).convert_alpha()
    # Adiciona a imagem da nuvem:
    assets['nuvem'] = pygame.image.load(path.join(IMG,'Nuvem.png')).convert_alpha()
    # Define o tamanho da nuvem:
    assets['nuvem'] = pygame.transform.scale(assets['nuvem'], (300, 165))
    # Adiciona o background da loja:
    assets['BGLoja'] = pygame.image.load(path.join(IMG,'Backgroundloja.png')).convert()
    # Define o tamanho do background da loja:
    assets['BGLoja'] = pygame.transform.scale(assets['BGLoja'], (1280, 720))
    
    assets['BGTitle'] = pygame.image.load(path.join(IMG,'Titletransparentbg.png')).convert_alpha()
    assets['BGTitle'] = pygame.transform.scale(assets['BGTitle'], (1280, 720))
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

    # Adiciona música ao jogo
    pygame.mixer.music.load(path.join(SND, 'Gamemusic.mp3'))
    pygame.mixer.music.set_volume(0.03)

    return assets