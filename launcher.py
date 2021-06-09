# Controla o jogo no geral por meio de um state machine


# Importando coisas
import pygame
import random
import json
from file_config import SCR_HEIGHT, SCR_WIDTH, FPS, QUIT, INGAME, TITLE, create_window
from assets import load_assets
from game import game_screen
from objects import Cloud

# Tenta ler o arquivo de save, se nao houver, cria um
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

# Inicializando o pygame e mixer
pygame.init()
pygame.mixer.init()
  
window = create_window(SCR_WIDTH,SCR_HEIGHT) # Cria janela 
assets = load_assets() # Carrega assets


window.fill((125, 190, 215))
pygame.display.update()

# Inicia timers das nuvens e cria seu sprite group
cloudtimer = 0
cloudtimetocreate = 1
clouds = pygame.sprite.Group()

# Arruma ticks
game_clock = pygame.time.Clock()


global_state = TITLE

while global_state != QUIT:
    # Definindo máximo de frames por segundo
    game_clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Se o jogador tenta fechar a tela sai do jogo
            global_state = QUIT
        elif event.type == pygame.KEYDOWN:
            # Se o jogador apertar qualquer tecla inicia o gameplay
            global_state = INGAME

    if global_state == INGAME:
        new_save = game_screen(window,save_data)
        with open('save.json','w') as save_json:
            # Atualizamos as variáveis do save 
            new_save = json.dumps(new_save)
            save_json.write(new_save)
        global_state = QUIT
    
    # Cria nuvens na tela de início
    cloudtimer += 1
    if cloudtimer >= cloudtimetocreate:
        speed = random.randint(4,5)
        centery = random.randint(30, SCR_HEIGHT-30)
        new_cloud = Cloud(assets, centery, speed)
        clouds.add(new_cloud)
        cloudtimer = 0
        cloudtimetocreate = random.randint(50, 300)
    
    # Atualiza o display
    clouds.update()
    window.fill((125, 190, 215))
    clouds.draw(window)
    window.blit(assets['BGTitle'], (0,0))
    pygame.display.update()
        
# Desativa o pygame antes de fechar o programa
pygame.quit()