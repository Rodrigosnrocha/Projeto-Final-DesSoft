import pygame
from os import path


def create_window(WIDTH, HEIGHT):
    """
    Cria a janela do jogo, a partir de um valor de largura e altura. Também define o título da janela
    """

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('TEST') #Caption temporário, mudar quando tivermos um título final
    return window

# Determina os diretórios de assets. Melhor não mexer muito se não precisar
IMG = path.join(path.dirname(__file__), 'assets', 'img')
SND = path.join(path.dirname(__file__), 'assets', 'snd')
TXT = path.join(path.dirname(__file__), 'assets', 'txt')

# Configurações de display do jogo. Não recomendável mudar após escolhido
SCR_WIDTH = 1280 #Determina a largura da janela
SCR_HEIGHT = 720 #Determina a altura da janela
FPS = 60 #Determina a frequência de frames por segundo

# Configurações de certas de objetos no jogo
ENEMY_CONFIG = {}
ENEMY_CONFIG['HEIGHT'] = 20
ENEMY_CONFIG['WIDTH'] = 20
ENEMY_CONFIG['SPEED'] = 5



# Estados para o launcher.py controlar o jogo
QUIT = 0
INGAME = 1
TITLE = 2
GAME_OVER = 3