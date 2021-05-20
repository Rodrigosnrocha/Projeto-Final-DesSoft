import pygame
from os import path
from file_config import IMG, SND, TXT

# Nomes para as chaves do dicionário
# IMPORTANTE: Lembre-se de importar as chaves para os arquivos onde são necessários
IMG_TEST = 'IMG_TEST'

def load_assets():
    """
    Carrega todos os assets do jogo e retorna como um dicionário,
    para que possam ser usados em outros arquivos,
    sem precisar importá-los um a um
    """


    # Coloque todos os assets nesse dicionário para facilitar seu uso depois
    assets = {}
    assets[IMG_TEST] = pygame.image.load(path.join(IMG,'img_test.png'))

    return assets