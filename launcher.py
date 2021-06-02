# Controla o jogo no geral por meio de um state machine. Melhor evitar botar muito código aqui

import pygame
import random
import json
from file_config import SCR_HEIGHT, SCR_WIDTH, FPS, QUIT, INGAME, TITLE, GAME_OVER, create_window
from assets import load_assets, IMG_TEST
from game import game_screen
from objects import Cloud

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

window.fill((125, 190, 215))
pygame.display.update()

cloudtimer = 0
cloudtimetocreate = 1
clouds = pygame.sprite.Group()
game_clock = pygame.time.Clock()

global_state = TITLE

while global_state != QUIT:
    game_clock.tick(FPS)
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
    
    cloudtimer += 1
    if cloudtimer >= cloudtimetocreate:
        speed = random.randint(4,5)
        centery = random.randint(30, SCR_HEIGHT-30)
        new_cloud = Cloud(assets, centery, speed)
        clouds.add(new_cloud)
        cloudtimer = 0
        cloudtimetocreate = random.randint(50, 300)
    
    clouds.update()
    window.fill((125, 190, 215))
    clouds.draw(window)
    window.blit(assets['BGTitle'], (0,0))
    pygame.display.update()
        
    
pygame.quit()