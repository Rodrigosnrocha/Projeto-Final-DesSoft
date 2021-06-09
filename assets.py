import pygame
from os import path
from file_config import IMG, SND, TXT

# Nomes para as chaves do dicionário
# IMPORTANTE: Lembre-se de importar as chaves para os arquivos onde são necessários
IMG_TEST = 'IMG_TEST'
BG_TEST = 'BG_TEST'
IMG_PLAYER = 'IMG_PLAYER'
IMG_BULLET = 'IMG_BULLET'
IMG_ENEMY = 'IMG_ENEMY'
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

    # Imagens dos sprites
    assets[IMG_PLAYER] = pygame.image.load(path.join(IMG,'aviao2.png')).convert_alpha() # Adiciona a imagem do avião do jogador
    assets[IMG_PLAYER] = pygame.transform.scale(assets[IMG_PLAYER], (194, 110)) # Define o tamanho do avião do jogador
    assets[IMG_BULLET] = pygame.image.load(path.join(IMG,'bullet.png')).convert_alpha() # Adiciona a imagem do "tiro"
    assets[IMG_BULLET] = pygame.transform.scale(assets[IMG_BULLET], (40, 12)) # Define o tamanho do "tiro"
    assets[IMG_ENEMY] = pygame.image.load(path.join(IMG,'aviao3.png')).convert_alpha() # Adiciona a imagem do avião inimigo
    assets[IMG_ENEMY] = pygame.transform.scale(assets[IMG_ENEMY], (118, 42)) # Define o tamanho do avião inimigo
    assets['blink'] = pygame.image.load(path.join(IMG,'img_blink.png')).convert_alpha() # Adiciona uma imagem transparente para a "animação" de "piscar" o avião
    assets['nuvem'] = pygame.image.load(path.join(IMG,'Nuvem.png')).convert_alpha() # Adiciona a imagem da nuvem
    assets['nuvem'] = pygame.transform.scale(assets['nuvem'], (300, 165)) # Define o tamanho da nuvem
    assets['BGLoja'] = pygame.image.load(path.join(IMG,'Backgroundloja.png')).convert() # Adiciona o background da loja
    assets['BGLoja'] = pygame.transform.scale(assets['BGLoja'], (1280, 720)) # Define o tamanho do background da loja
    assets['BGTitle'] = pygame.image.load(path.join(IMG,'Titletransparentbg.png')).convert_alpha() # Plano de fundo da tela de início
    assets['BGTitle'] = pygame.transform.scale(assets['BGTitle'], (1280, 720)) # Define o tamanho do background da tela de início
    
    # Todas as fontes são iguais, mas têm tamanhos diferentes
    assets[FONT] = pygame.font.Font(None,28)
    assets['FONT2'] = pygame.font.Font(None,36)
    assets['FONT3'] = pygame.font.Font(None,48)
    assets['FONT4'] = pygame.font.Font(None,70)

    
    coin_anim = [] # Animação de moeda girando
    for i in range(6):
        filename = 'Coin{}.png'.format(i+1)
        img = pygame.image.load(path.join(IMG,filename)).convert_alpha()
        img = pygame.transform.scale(img, (32, 32))
        coin_anim.append(img)
    assets["coin_anim"] = coin_anim

    heart_anim = [] # Animação de coração girando
    for i in range(4):
        filename = 'HeartT{}.png'.format(i)
        img = pygame.image.load(path.join(IMG,filename)).convert_alpha()
        heart_anim.append(img)
    assets["heart_anim"] = heart_anim

    
    assets['shoot_sound'] = pygame.mixer.Sound(path.join(SND,'ES_Gunshot Shotgun 159.mp3')) # Som de tiros
    pygame.mixer.music.load(path.join(SND, 'Gamemusic.mp3')) # Carrega a música do jogo

    return assets