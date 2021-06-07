# Controla o jogo no geral por meio de um state machine. Melhor evitar botar muito código aqui


# importando coisas
import pygame
import random
import json
from file_config import SCR_HEIGHT, SCR_WIDTH, FPS, QUIT, INGAME, TITLE, GAME_OVER, create_window
from assets import load_assets, IMG_TEST
from game import game_screen
from objects import Cloud

# tenta ler o arquivo de save, se nao houver, cria um
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

#inicializacao
pygame.init()
pygame.mixer.init()
  
#cria janela, carrega assets
window = create_window(SCR_WIDTH,SCR_HEIGHT)
assets = load_assets()

window.fill((125, 190, 215))
pygame.display.update()

#inicia timers das nuvens e grupo
cloudtimer = 0
cloudtimetocreate = 1
clouds = pygame.sprite.Group()

#arruma ticks
game_clock = pygame.time.Clock()

global_state = TITLE

#enquanto o estado nao e quit
while global_state != QUIT:
    #game tick
    game_clock.tick(FPS)

    # checa se quer fechar o jogo
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
    
    # sistema de update, criacao e deleta nuvens (tela de inicio)
    cloudtimer += 1
    if cloudtimer >= cloudtimetocreate:
        speed = random.randint(4,5)
        centery = random.randint(30, SCR_HEIGHT-30)
        new_cloud = Cloud(assets, centery, speed)
        clouds.add(new_cloud)
        cloudtimer = 0
        cloudtimetocreate = random.randint(50, 300)
    
    # updates na tela
    clouds.update()
    window.fill((125, 190, 215))
    clouds.draw(window)
    window.blit(assets['BGTitle'], (0,0))
    pygame.display.update()
        
    
pygame.quit()