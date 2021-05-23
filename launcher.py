# Controla o jogo no geral por meio de um state machine. Melhor evitar botar muito código aqui

import pygame
from file_config import SCR_HEIGHT, SCR_WIDTH, FPS, QUIT, INGAME, TITLE, GAME_OVER, create_window
from assets import load_assets, IMG_TEST
from game import game_screen

pygame.init()
pygame.mixer.init()

window = create_window(SCR_WIDTH,SCR_HEIGHT)
assets = load_assets()

window.blit(assets[IMG_TEST],(0,0))
pygame.display.update()

global_state = TITLE
while global_state != QUIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global_state = QUIT
        elif event.type == pygame.KEYDOWN:
            global_state = INGAME
    if global_state == INGAME:
        game_screen(window)
        global_state = QUIT

pygame.quit()