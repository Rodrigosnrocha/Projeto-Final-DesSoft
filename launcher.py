# Controla o jogo no geral por meio de um state machine. Melhor evitar botar muito código aqui

import pygame
from file_config import SCR_HEIGHT, SCR_WIDTH, FPS, QUIT, INGAME, TITLE, GAME_OVER, create_window
from assets import load_assets, IMG_TEST

pygame.init()
pygame.mixer.init()

window = create_window(SCR_WIDTH,SCR_HEIGHT)
assets = load_assets()

window.blit(assets[IMG_TEST],(0,0))
pygame.display.update()

state = TITLE
while state != QUIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = QUIT
        elif event.type == pygame.KEYDOWN:
            state = INGAME

pygame.quit()