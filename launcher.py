# Controla o jogo no geral por meio de um state machine. Melhor evitar botar muito código aqui

import pygame
import json
from file_config import SCR_HEIGHT, SCR_WIDTH, FPS, QUIT, INGAME, TITLE, GAME_OVER, create_window
from assets import load_assets, IMG_TEST
from game import game_screen

try:
    with open('save.json','r') as save_json:
        x = save_json.read()
        save_data = json.loads(x)

except:
    with open('save.json','w') as save_json:
        save_data = {
            "high_score" : 0,
            "coins" : 0,
            "shoot_speed" : 0,
            "difficulty" : 6
        }
        dic_json = json.dumps(save_data)
        save_json.write(dic_json)

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
        new_save = game_screen(window,save_data)
        with open('save.json','w') as save_json:    
            new_save = json.dumps(new_save)
            save_json.write(new_save)
        global_state = QUIT
pygame.quit()